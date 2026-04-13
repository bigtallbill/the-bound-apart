# Project: The Bound Apart
A single or multiplayer coop space sim in the same vein as Freespace2 and Wing Commander.

## Primary mechanics
1st person space sim focusing on dogfights and strategic missions.

### Between Missions
The player will first register via an enrollment process where they set their callsign, after which they are assigned to their carrier.
Then they see the primary game menu which has a bunch of themed animated "buttons" when hovered over:

 - Hangar: allows you to review unlocked fighter craft and stats of capital ships
 - Training: lets you into a training simulator
 - Pilot Arena: Multiplayer dogfights
 - Mission Briefing: Starts a single or multiplayer mission
 - Engineering: the options menu

### Missions
when launched into a mission, the player/s are taken through a mix of scripted dialog/events and free dogfighting combat.

### Ship Physics
Ships are simulated using their engine manuvering handling specs

- Yaw, Pitch and Roll speeds
- Max speed
- Max Accelleration
- Drift damping (so if you turn tightly the ship will try to alter your current vector to match. but effectiveness is based on this performance metric so some ships can feel drifty and others more responsive)

#### Pilot controls
Pilots generally move their ships with the mouse. and left click to fire primary and rightclick for secondary. mouse wheel changes secondary (typically different missile types).

##### Keymap

- `left-mouse` - Fire primary
- `right-mouse` - Fire seconday
- `mouse-wheel` - cycle secondary
- `m` - match velocity of target.
- `h` - cycle visible hostile targets prefering those near the center reticule.
- `shift-h` - cycle all hostile targets.
- `c` - open communication window to chat with squadron in multiplayer/coop
- `p` - opens power menu which allows the player to use the mouse to drag power adjustment sliders

## Techinical Implementation
Server authoritive even in single player. The godot client is only responsible for rendering and as a frontend UI.
We'll use websockets for communication with the elixir/phoenix backend.

When a player is in multiplayer mode (toggled on) then the game starts a session on the server which generates a join code that other players can be invited with. then when launching a mission all players go into that together.

The player can toggle public multiplayer on or off at any point in the menu. this will switch to using the public servers instead of local. When on local players on the LAN can still join, if the player has setup the network correctly (ports etc).

The server is bundled with godot using (https://github.com/burrito-elixir/burrito)[Buritto]

## Main factions:
### The Bound
Enigmatic progentitor race that left a lot of large technological works littered about. The other factions covet these artifacts and control over them is the cause of more than one war. Many legitimate and illigitemate organisations exist to trade and study these artifcacts.
### Faction1
Represents the human expansion into space as one organization with many sub-species members
### Faction2
The main antagonist to Faction1,
