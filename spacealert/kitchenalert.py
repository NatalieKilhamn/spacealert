# -*- coding: utf-8 -*-
# Kitchen Alert service generator, built on the Space Alert mission generator in spacealert.py.
#
# Kitchen Alert is a cooperative restaurant mod of Space Alert. A service works like a mission:
# 12 rounds in three phases, planned in real time to a soundtrack. Instead of threats, orders
# come in. Each order is announced with the round it arrives (T+1 ... T+8), its size
# (regular or large, drawn from separate decks) and the dining room where the guests sit.
# Deliveries, handovers and rush hours work like incoming data, data transfer and
# communications down in Space Alert.
#
# This program is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
import itertools, random

import spacealert as sa
from spacealert import (Event, Phase, IncomingData, DataTransfer, CommunicationsDown,
                        InvalidMissionError, MAX_ITERATIONS, parseTime)


class Room:
    """One of the two dining rooms, named after its side of the board."""
    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __repr__(self):
        return self.name

ROOMS = (Room('Red', 'R'), Room('Blue', 'B'))   # red on the left, blue on the right, as in Space Alert


class Order(Event):
    """An order: the guests' marker goes on the guest track in *room* at the start of round *turn*."""
    duration = 15

    def __init__(self, start=None, turn=None, large=False, room=None, rush=False):
        super().__init__(start)
        self.turn = turn
        self.large = large
        self.room = room
        self.rush = rush        # announced late in the phase, like an ambush in Space Alert

    # spacealert.MissionGenerator.chooseThreatTimes uses the name 'ambush'
    @property
    def ambush(self):
        return self.rush

    @ambush.setter
    def ambush(self, value):
        self.rush = value

    @property
    def points(self):
        return 2 if self.large else 1

    @property
    def kind(self):
        return 'Large order' if self.large else 'New order'

    def __repr__(self):
        return '{} T+{} {} {}'.format(self.timeString, self.turn, 'L' if self.large else 'N', self.room)

    @property
    def message(self):
        return '{} - Time T+{} {}, {} dining room'.format(self.timeString, self.turn, self.kind, self.room)

    @staticmethod
    def fromString(string):
        """Parse '0:10 T+2 L Blue' (L = large, N = new/regular)."""
        time, turn, size, room = string.split()
        assert turn.startswith('T+') and size in ('N', 'L')
        room = next(r for r in ROOMS if r.name.lower() == room.lower())
        return Order(parseTime(time), int(turn[2:]), size == 'L', room)


SIZES = ('easy', 'normal', 'hard')


class KitchenOptions(sa.Options):
    """Options for a service. Use KitchenOptions.create(players, size)."""
    orderPoints = 7          # regular order = 1 point, large order = 2 points
    minCount = 6             # number of orders
    maxCount = 6
    pLarge = 0.5             # weight between the possible mixes when several fit the counts
    maxSameRoomInARow = 2
    maxRoomImbalance = 2     # e.g. 4 orders to one dining room and 2 to the other
    threatLength = 10        # names shared with spacealert.Options and its timing code
    threatDistance = 25

    @staticmethod
    def create(playerNumber, size='normal', **args):
        if playerNumber not in (4, 5):
            raise ValueError('Number of players must be 4 or 5.')
        if size not in SIZES:
            raise ValueError('Size must be one of {}.'.format(SIZES))
        # (points, min orders, max orders) for four players; five players get one point more
        table = {'easy': (6, 5, 5), 'normal': (7, 6, 6), 'hard': (8, 6, 7)}
        points, lo, hi = table[size]
        if playerNumber == 5:
            points, lo, hi = points + 1, lo + 1, hi + 1
        options = KitchenOptions(orderPoints=points, minCount=lo, maxCount=hi)
        options.update(**args)
        return options

    OPTIONS = sa.Options.OPTIONS + [('orderPoints', int), ('pLarge', float),
                                    ('maxSameRoomInARow', int), ('maxRoomImbalance', int)]


def playerEnd(event):
    """When the event ends in the browser player (player.js and kitchen.js)."""
    if isinstance(event, sa.PhaseEvent):
        return event.start + (event.duration if event.remaining == 7 else 5)
    if isinstance(event, CommunicationsDown):
        return event.start + max(5, event.duration) + 2
    return event.end


def overlaps(mission):
    """Pairs of announcements that would cut each other off in the player."""
    events = [e for e in mission.events]
    out = []
    for a, b in zip(events, events[1:]):
        if playerEnd(a) > b.start:
            out.append((a, b))
    if events and events[0].start < 7:     # the start announcement plays for 7 seconds
        out.append(('start', events[0]))
    return out


class KitchenMission(sa.Mission):
    """A Space Alert mission whose rush hours keep five seconds clear after them, so that
    "Rush is over" is never cut off by the next announcement."""
    PAD = 5

    def collides(self, event):
        def padded(e):
            return (e.start, e.end + (self.PAD if isinstance(e, CommunicationsDown) else 0))
        s1, e1 = padded(event)
        if s1 < 10:
            return True
        return any(s1 < e2 and s2 < e1 for s2, e2 in map(padded, self.events))


class ServiceGenerator(sa.MissionGenerator):
    """Generates services. Phases, deliveries, handovers and rush hours come from the Space Alert
    generator; orders replace the threats."""

    def __init__(self, options=None, **args):
        super().__init__(options if options is not None else KitchenOptions(**args))

    def makeMission(self):
        self.mission = KitchenMission()
        self.makePhases()
        self.makeThreats()
        if not self.solo:
            self.makeOtherEvents()
        if overlaps(self.mission):
            raise InvalidMissionError('Announcements overlap')
        return self.mission

    def makeThreats(self):
        orders = self.chooseOrders()
        self.assignOrdersToTurns(orders)
        for order in orders:
            order.phase = self.mission.phases[0] if order.turn <= 4 else self.mission.phases[1]
        self.chooseThreatTimes(orders, self.mission.phases)
        self.chooseRooms(orders)
        self.mission.addEvents(orders)

    def chooseOrders(self):
        """Choose how many orders are large, given the points and the allowed number of orders."""
        mixes = []
        for large in range(0, self.orderPoints // 2 + 1):
            regular = self.orderPoints - 2 * large
            if self.minCount <= regular + large <= self.maxCount:
                mixes.append(large)
        if not mixes:
            raise InvalidMissionError('No mix of orders gives {} points with {}-{} orders'
                                      .format(self.orderPoints, self.minCount, self.maxCount))
        weights = {large: self.pLarge ** k * (1 - self.pLarge) ** (len(mixes) - 1 - k)
                   for k, large in enumerate(mixes)}
        large = sa.draw(weights)
        regular = self.orderPoints - 2 * large
        return [Order(large=True) for _ in range(large)] + [Order() for _ in range(regular)]

    def assignOrdersToTurns(self, orders):
        """One order per round on T+1 ... T+8, with the points split fairly evenly between the halves."""
        lo = (self.orderPoints + 1) // 2 - 1
        hi = self.orderPoints // 2 + 1
        for _ in range(MAX_ITERATIONS):
            turns = random.sample(range(1, 9), len(orders))
            first = sum(o.points for o, t in zip(orders, turns) if t <= 4)
            second = sum(o.points for o, t in zip(orders, turns) if t > 4)
            if lo <= first <= hi and lo <= second <= hi:
                for o, t in zip(orders, turns):
                    o.turn = t
                orders.sort(key=lambda o: o.turn)
                return
        raise InvalidMissionError('Cannot assign orders to rounds')

    def chooseRooms(self, orders):
        for _ in range(MAX_ITERATIONS):
            rooms = [random.choice(ROOMS) for _ in orders]
            runs = max(len(list(g)) for _, g in itertools.groupby(rooms))
            left = sum(1 for r in rooms if r is ROOMS[0])
            if runs <= self.maxSameRoomInARow and abs(2 * left - len(rooms)) <= self.maxRoomImbalance:
                for o, r in zip(orders, rooms):
                    o.room = r
                return
        raise InvalidMissionError('Cannot choose dining rooms')


def makeService(players=4, size='normal', **args):
    """Generate a service, retrying when the random timing does not fit."""
    options = KitchenOptions.create(players, size, **args)
    for _ in range(MAX_ITERATIONS):
        try:
            return ServiceGenerator(options).makeMission()
        except InvalidMissionError:
            continue
    raise InvalidMissionError('Could not generate a service')


def loadScript(name, players):
    """Load a scripted service from kitchen_scripts.py. Lines marked '5P' only count with five players."""
    from kitchen_scripts import scripts
    mission = sa.Mission()
    lines = scripts[name].strip().split('\n')
    start = 0
    for i, end in enumerate((parseTime(t) for t in lines[0].split(' - ')), start=1):
        mission.addPhase(Phase(i, start, end - start))
        start = end
    for line in lines[1:]:
        code, rest = line[:2], line[3:]
        if code in ('OR', '5P'):
            if code == 'OR' or players == 5:
                mission.addEvent(Order.fromString(rest))
        else:
            cls = {'ID': IncomingData, 'DT': DataTransfer, 'CD': CommunicationsDown}[code]
            mission.addEvent(cls.fromString(rest))
    return mission


def scriptText(mission):
    """The service in the format of kitchen_scripts.py."""
    p = mission.phases
    lines = [' - '.join('{}:{:02}'.format(ph.end // 60, ph.end % 60) for ph in p)]
    for e in mission.events:
        t = '{}:{:02}'.format(e.start // 60, e.start % 60)
        if isinstance(e, Order):
            lines.append('OR {} T+{} {} {}'.format(t, e.turn, 'L' if e.large else 'N', e.room))
        elif isinstance(e, IncomingData):
            lines.append('ID {}'.format(t))
        elif isinstance(e, DataTransfer):
            lines.append('DT {}'.format(t))
        elif isinstance(e, CommunicationsDown):
            lines.append('CD {} - {}:{:02}'.format(t, e.end // 60, e.end % 60))
    return '\n'.join(lines)


def transcript(mission):
    """A readable script: what is announced when."""
    names = {IncomingData: 'Delivery (each player may draw one card)',
             DataTransfer: 'Handover (each player may give one card to another player)'}
    out = []
    for e in mission.events:
        if isinstance(e, Order):
            out.append(e.message)
        elif isinstance(e, sa.PhaseEvent):
            if e.remaining == 7:
                what = 'Kitchen closes' if e.phase.number == 3 else 'Phase {} ends'.format(e.phase.number)
                out.append('{} - {}'.format(sa.Event(e.start + 7).timeString, what))
        elif isinstance(e, CommunicationsDown):
            out.append('{} - Rush hour, no talking ({} seconds)'.format(e.timeString, e.duration))
        else:
            out.append('{} - {}'.format(e.timeString, names[type(e)]))
    return '\n'.join(out)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate a Kitchen Alert service.')
    parser.add_argument('-p', '--players', type=int, choices=[4, 5], default=4)
    parser.add_argument('-s', '--size', choices=SIZES, default='normal')
    parser.add_argument('--seed', type=int)
    parser.add_argument('--script', action='store_true', help='print in the format of kitchen_scripts.py')
    args = parser.parse_args()
    if args.seed is not None:
        random.seed(args.seed)
    service = makeService(args.players, args.size)
    print(scriptText(service) if args.script else transcript(service))
