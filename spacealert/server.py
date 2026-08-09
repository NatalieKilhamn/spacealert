# -*- coding: utf-8 -*-
# This file is part of the Space Alert Misson Player at
# https://github.com/MartinAltmayer/spacealert.
# 
# Copyright 2015 Martin Altmayer
# The Space Alert board game was created by Vlaada Chvátil.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import io, http.server, os
import json
import urllib.parse
import spacealert

htmlParts = {}


def _numbered(prefix, count, label):
    return [(prefix + str(i), '{} {}'.format(label, i)) for i in range(1, count + 1)]


# The catalogue of mission types. 'generate' names the generator mode that can
# invent a new mission of this type, or is None when the generator has no such
# mode -- those types offer only the scripted missions from the game.
MISSION_TYPES = [
    {'key': 'regular', 'label': 'Regular mission', 'generate': 'normal',
     'scripts': _numbered('mission', 8, 'Mission')},
    {'key': 'doubleAction', 'label': 'Double action', 'generate': 'double',
     'scripts': _numbered('doubleAction', 12, 'Double action mission')},
    {'key': 'doubleActionEasy', 'label': 'Double action (easier)', 'generate': None,
     'scripts': _numbered('doubleActionEasy', 6, 'Easier double action mission')},
    {'key': 'training', 'label': 'Training', 'generate': None,
     'scripts': [('firstTestRun', 'First test run'), ('secondTestRun', 'Second test run')]},
    {'key': 'simulation', 'label': 'Simulation', 'generate': None,
     'scripts': _numbered('simulation', 3, 'Simulation')},
    {'key': 'advancedSimulation', 'label': 'Advanced simulation', 'generate': None,
     'scripts': _numbered('advancedSimulation', 3, 'Advanced simulation')},
]

MISSION_TYPES_BY_KEY = {t['key']: t for t in MISSION_TYPES}
DEFAULT_TYPE = 'regular'

def run(port=8000):
    with open('player.htm', 'r') as htmlFile:
        html = htmlFile.read()
        pos1 = html.index("/* BEGIN */")
        pos2 = html.index("/* END */", pos1)
        htmlParts['header'] = html[0:pos1].encode('utf-8')
        htmlParts['body'] = html[pos2+len("/* END */"):].encode('utf-8')
        del html
    
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, RequestHandler)
    httpd.serve_forever()


def getJavaScript(event):
    def b(x):
        return "true" if x else "false"
    
    if isinstance(event, spacealert.Alert):
        return 'new Alert({}, {}, {}, "{}")'.format(
                    event.start,
                    event.turn,
                    b(event.serious),
                    event.zone.name.lower() if not event.internal else "internal")
    elif isinstance(event, spacealert.PhaseEvent):
        return 'new PhaseEvent({}, {}, {}, {})'.format(event.start, event.phase.number,
                                                       event.remaining or 0, b(event.phase.number == 3))
    elif isinstance(event, spacealert.DataTransfer):
        return 'new DataTransfer({})'.format(event.start)
    elif isinstance(event, spacealert.IncomingData):
        return 'new IncomingData({})'.format(event.start)
    elif isinstance(event, spacealert.CommunicationsDown):
        return 'new CommunicationsDown({},{})'.format(event.start, event.duration)
    else:
        assert False


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Everything here is generated or read from disk on each request, and the
        # server is local. Caching gains nothing and a stale player.js or menu
        # silently breaks missions after an update.
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def isNormalFile(self, path):
        return path.startswith('/audio/') or path.startswith('/images/') \
                or path in ['/player.js']

    def serveMenu(self, head=False):
        """Serve the main menu, injecting the mission catalogue so that the page
        and the server can never disagree about which missions exist."""
        with open('index.htm', 'r') as f:
            html = f.read()
        html = html.replace('/* CATALOGUE */', json.dumps(MISSION_TYPES))
        data = html.encode('utf-8')
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if not head:
            self.wfile.write(data)

    def doHelper(self, head=True):
        url = urllib.parse.urlparse(self.path)
        print(self.path, url.path)
        if url.path != '/player.htm':
            if url.path == '/':
                self.send_response(301)
                self.send_header('Location','/index.htm')
                self.end_headers()
                return False
            if url.path == '/index.htm':
                self.serveMenu(head=head)
                return False
            if url.path == '/exit.htm':
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                # server shutdown must be called in a different thread
                import threading
                thread = threading.Thread(target=self.server.shutdown)
                thread.daemon = True
                thread.start()
                return False
            elif self.isNormalFile(url.path):
                if head:
                    super().do_HEAD()
                    return False
                else:
                    super().do_GET()
                    return False
            else:
                self.send_error(404, "File not found")
                return False
        return True
            
    def do_HEAD(self):
        if self.doHelper(head=True):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
        
    def parseGetParams(self, url):
        """Read the three menu parameters: players, mission type, and which
        mission of that type ('random', 'generate', or a script name)."""
        p = urllib.parse.parse_qs(url.query) # p maps to lists
        p = {k: v[-1] for k,v in p.items()}  # but we need each param only once

        players = p.get('players')
        if players not in ['4', '5']:
            players = '4'
        players = int(players)

        missionType = p.get('type')
        if missionType not in MISSION_TYPES_BY_KEY:
            missionType = DEFAULT_TYPE
        typeInfo = MISSION_TYPES_BY_KEY[missionType]

        mission = p.get('mission', 'random')
        names = [name for name, label in typeInfo['scripts']]
        if mission == 'generate' and typeInfo['generate'] is None:
            # This type has no generator; fall back to one of its scripts.
            print("Type '{}' cannot be generated, choosing a scripted mission.".format(missionType))
            mission = 'random'
        elif mission not in names and mission not in ['random', 'generate']:
            print("Unknown mission '{}' for type '{}', choosing randomly.".format(mission, missionType))
            mission = 'random'

        return {'players': players,
                'type': missionType,
                'typeInfo': typeInfo,
                'mission': mission,
                }

    def do_GET(self):
        if not self.doHelper(head=False):
            return

        # parse GET parameters
        url = urllib.parse.urlparse(self.path)
        params = self.parseGetParams(url)
        typeInfo = params['typeInfo']

        # Make events
        if params['mission'] == 'generate':
            try:
                if typeInfo['generate'] == 'double':
                    options = spacealert.Options.createDoubleActions(params['players'])
                else: options = spacealert.Options.create(params['players'])
                generator = spacealert.MissionGenerator(options)
                mission = generator.makeMission()
            except (RuntimeError, spacealert.InvalidMissionError) as e:
                print(e)
                self.send_error(500, "Mission could not be generated")
                return
        else:
            name = params['mission']
            if name == 'random':
                import random
                name = random.choice([n for n, label in typeInfo['scripts']])
            mission = loadScript(name, params['players'])

        javaScript = map(getJavaScript, mission.events)
        content = ',\n'.join(s for s in javaScript if len(s) > 0)
            
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(htmlParts['header'])
        self.wfile.write(b"var events = [\n");
        self.wfile.write(content.encode('utf-8'))
        self.wfile.write(b"\n];\n\n");
        self.wfile.write(htmlParts['body'])


def loadScript(name, players):
    from spacealert import Phase, Alert, IncomingData, CommunicationsDown, DataTransfer, parseTime
    from scripts import scripts

    if name not in scripts:
        print("Unknown mission name '{}', I will use a random regular mission.".format(name))
        import random
        name = 'mission{}'.format(random.randint(1, 8))

    mission = spacealert.Mission()
    lines = scripts[name].strip().split('\n')
    
    # Create phases from first line, e.g. '3:40 - 7:30 - 10:00'
    startTime = 0
    phaseTimes = [parseTime(time) for time in lines[0].split(' - ')]
    for i, endTime in enumerate(phaseTimes, start=1):
        phase = Phase(i, startTime, endTime - startTime)
        mission.addPhase(phase)
        startTime = endTime
    
    # Create events from strings like 'AL 3:30 T+4 ST Red'
    for line in lines[1:]: # skip first line, which determines phase lengths
        code, line = line[:2], line[3:] # remove two-letter code from line
        if code in ['AL', 'UA']:
            if code == 'AL' or players == 5:
                mission.addEvent(Alert.fromString(line))
        else:
            cls = {'ID': IncomingData, 'DT': DataTransfer, 'CD': CommunicationsDown}[code]
            mission.addEvent(cls.fromString(line))
    
    return mission
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run the Space Alert Mission Player server.")
    parser.add_argument('--port', type=int, help="Port where the server should run, defaults to 8000.", default=8000)

    args = vars(parser.parse_args())
    run(**args)
