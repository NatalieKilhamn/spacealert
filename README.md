# Space Alert Mission Player

The Space Alert board game (http://czechgames.com/en/space-alert/) includes a CD with audio files that must be played during missions. But because players are often noisily discussing how to save their ship, it is much more comfortable to use a graphical display along with the audio. This program contains a player that runs in your browser and accompanies your missions with graphics and sound. 

## Features:
- Random mission generator. The original CD only contains eight missions. This program can randomly generate missions that are equally good as those on the CD.
- Based on HTML5 rather than e.g. Flash.
- All the scripted missions from the game: the eight regular missions, the training runs and simulations, and the double action missions from The New Frontier (12 regular and 6 easier).
- Supports missions for double action cards (for the expansion), both scripted and generated.

![Main menu](/menu.png?raw=true)


## Usage

1. Start the server with

> python3 server.py

or

> python3 server.py --port &lt;PORT&gt;

if the default port 8000 is not ok.

2. Now point your web browser at
http://localhost:8000/index.htm
and use the webpage to start either a randomly generated mission or a scripted mission from the game CD.

3. To stop the server simply use Ctrl+C or the "Exit" button at the bottom of the main menu.


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

![Player screenshot](/alert.png?raw=true)
