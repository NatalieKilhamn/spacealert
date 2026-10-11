# Space Alert Mission Player

The Space Alert board game (http://czechgames.com/en/space-alert/) includes a CD with audio files that must be played during missions. But because players are often noisily discussing how to save their ship, it is much more comfortable to use a graphical display along with the audio. This program contains a player that runs in your browser and accompanies your missions with graphics and sound. 

## Features:
- Random mission generator. The original CD only contains eight missions. This program can randomly generate missions that are equally good as those on the CD.
- Based on HTML5 rather than e.g. Flash.
- All the scripted missions from the game: the eight regular missions, the training runs and simulations, and the double action missions from The New Frontier (12 regular and 6 easier).
- Supports missions for double action cards (for the expansion), both scripted and generated.

![Main menu](/docs/menu.png?raw=true)


## Usage

1. In the top folder of this repository, start the server with

> python3 server.py

or

> python3 server.py --port &lt;PORT&gt;

if the default port 8000 is not ok.

2. Now point your web browser at
http://localhost:8000/index.htm
and use the webpage to start either a randomly generated mission or a scripted mission from the game CD.

3. To stop the server simply use Ctrl+C or the "Exit" button at the bottom of the main menu.


## Layout of the repository

- `server.py` serves both games.
- `player/` is the browser player they share (`player.js` and its images).
- `spacealert/` has the Space Alert mission generator (`spacealert.py`), the scripted missions
  (`scripts.py`), the menu and player pages, and the sound files.
- `kitchenalert/` has everything for Kitchen Alert (see below).
- `docs/` has the screenshots in this README.


## Threat Card Difficulties

This player does not announce the colour of the threat card to draw. It assumes
you prepare your threat decks during setup — mixing colours as you like for
intermediate difficulty — and then simply draw from the top. Announcements name
the turn, the severity and the zone, e.g. "Time T+5, Serious Threat, Zone Blue".


## Attributions

The Space Alert board game was created by Vlaada Chvátil and published at Czech Games Edition, see http://czechgames.com/en/space-alert/.

While this software is published under the GPL, this does not include the sound files and the background of the main menu, which are copyright of Czech Games Edition.

This program was inspired by the Flash-based player at
http://www.phipsisoftware.com/SpaceAlert.htm

The double action mission scripts were transcribed from
https://github.com/nibuen/SpaceAlertMissionGenerator (MIT licensed), file
`ConstructedMissions.java`.

![Player screenshot](/docs/alert.png?raw=true)


## Kitchen Alert

The same player also runs services for Kitchen Alert, a cooperative restaurant mod of
Space Alert. The rules are in [`kitchenalert/rules.md`](kitchenalert/rules.md), in Swedish in
[`kitchenalert/regler.md`](kitchenalert/regler.md); the board and the order cards are in
`kitchenalert/print/`.
Start the server as above and open
http://localhost:8000/kitchen.htm

A service works like a mission: 12 rounds in three phases. Instead of threats, orders are
announced with the round they arrive, their size and the dining room where the guests sit,
e.g. "Time T plus three. New order. Red dining room." As in Space Alert, red is the left side
of the board and blue the right. Draw the top card of the regular or large order deck. Space Alert's other announcements have kitchen names:

| Kitchen Alert | Space Alert | Effect |
| --- | --- | --- |
| Delivery | Incoming data | Each player may draw one card. |
| Handover | Data transfer | Each player may give one card to another player before the beep. |
| Rush hour | Communications down | No talking until "Rush is over". |
| The kitchen closes | Operation ends | End of the third phase. |

Everything below is in `kitchenalert/`:

- `rules.md` and `regler.md`: the rules in English and Swedish.
- `print/`: the board and the order cards (English and Swedish) as SVG and PDF, and the scripts
  that draw them.
- `kitchenalert.py` generates services on top of the Space Alert generator. A normal service
  for four players has 7 order points: 5 regular orders (1 point) and 1 large order (2 points),
  one per round on T+1 to T+8. Easy has 6 points, hard 8, and five players get one point more.
  Run `python3 kitchenalert/kitchenalert.py -p 4 -s normal` to print a service, or add
  `--script` for the format of `kitchen_scripts.py`.
- `kitchen_scripts.py` has five fixed services, so that playtest groups can compare the same
  service. Lines marked `5P` only apply with five players.
- `kitchen.htm`, `kitchen-player.htm` and `kitchen.js` are the menu and player. `kitchen.js`
  loads after `player/player.js` and replaces the events and widgets that differ.
- `audio/` holds the announcements, made with macOS text-to-speech by `make_kitchen_audio.py`
  (needs ffmpeg). Change the wording or the voice there and run it again, e.g.
  `python3 kitchenalert/make_kitchen_audio.py --voice Daniel`.
