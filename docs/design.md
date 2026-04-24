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
Represents the human expansion into space as a few organizations, some are governments, planet states or corporations.

#### Governments
Rough earth timeline post 2026:

 - 2030 first AI fueled wars bagan
 - 2033 china invades Europe and becomes GCE (greater china europa)
 - 2034 china attempts to annex historically russian territory
 - 2035 america/russia ally to defend against chinese encroachment
 - 

1. the consolidation of europe+china
2. the evolution of the america/russia/australia alliance
#### Planet States
1. New Crete

### Faction2
The main antagonist to Faction1, the only alien race known to humans except the evidence of The Bound.

They are technologically similar to the humans but act as a single community. They have short range telepathic links that carry emotional/intent content, they cannot "talk" over their links, but they tend to act as one, even though each indivudual does have a distinct self.

In the broader interstellar space, they organize into colonies and exchange information/emotion/intent via "runner" ships between systems.

## Technology

### Hyperspace
Inter system jump technology was discovered in the form of a species of biomechanical plant that appears to be an invention of The Bound (unconfirmed).
So far efforts to replicate the technology have not been fruitful. Scaling up has limits as each plant must be grown while preventing it from jumping away. Technology was developed to contain the plants. Anything the plant has it's roots in can be jumped and the destination can be controlled by introducing controlled pheromones into calibrated points on each plant. Every jump drive is unique. When jumping the plant must be fully exposed, so the branches can unfurl. Again feromones are used to "close" the plant so it can be contained and protected. while the plants can sustain damage and regrow, this takes significant time and can throw off jump calibrations. Emergency jumps have happened in conflict with damaged plants that either lead to success or disaster (jumping inside planets or stars etc).

The plants appear to thrive off subspace in some unknown way. So occasionally they need to retreat to areas the plants favor for recouperation.

It is common for some military ships to maintain a secondary smaller plant for emergency precision jumps.

Fighter craft cannot be equiped with jump drives due to the bulky nature of supporting systems. Carrier vessels are required for fighter-craft.
