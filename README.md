Asteroids (VB6)
=================

Brief project overview
This is an Asteroids-style game written in Visual Basic 6. It uses arrays named `SpaceObject` to represent ships, asteroids and bullets, a `PictureBox` called `Picture1` as the drawing surface, and a `Timer` for the main update loop.

## Files Of Interest

- `Form1.frm` - Main form, UI setup, timer loop, player input, drawing, black hole behavior, scoring, and round reset logic.
- `Module1.bas` - Global variables, movement math, collision detection, shooting, explosions, health, and damage logic.
- `asteroids.vbp` / `asteroids.vbw` - VB6 project and workspace files.
- `tools/` - Helper scripts for converting SVG paths into VB6 polygon angle/radius assignments.

## Features

- **Two-player asteroid combat**: Blue and Red ships fight in the same arena.
- **Health system**: Ships start with 100% health and lose health when hit by opponent bullets.
- **Win-based scoring**: Players earn points by winning rounds, not by individual hits.
- **Energy pickups**: Green plus-shaped pickups spawn during play and restore health.
- **Black hole**: A central gravity well pulls ships, asteroids, bullets, and pickups toward it. Anything that touches the visible event horizon is sucked in. If a ship is sucked in, the other player wins the round.
- **Explosions and round reset**: Destroyed ships explode, a winner message is shown, and the round resets after a short delay.
- **Improved thrust**: Both players use stronger main engine thrust for faster acceleration and better control.

## Controls

### Player 1 - Blue Ship

- Rotate left/right: Left arrow / Right arrow
- Thrust: Down arrow
- Shoot: Up arrow

### Player 2 - Red Ship

- Rotate left/right: A / D
- Thrust: S
- Shoot: G

Holding the shoot key fires repeatedly with a short cooldown.

## How To Run

Open `asteroids.vbp` in the Visual Basic 6 IDE and press Run (F5). VB6 is required to build and run this project as provided.

## How The Game Works

Each object is stored in `SpaceObject(objIndex, propertyIndex)`. Important properties include whether the object exists, screen position, orientation, velocity, mass, collision behavior, and an angle/radius list used to draw the polygon shape.

The main loop runs on `Timer1` and handles:

- Key state and player input
- Rotation and thrust
- Black hole gravity and event-horizon contact
- Object movement and screen wrapping
- Collision detection
- Health and energy pickup behavior
- Scores, winner messages, and round resets
- Drawing to `Picture1`

## Key Routines

- `MakeCoords` converts an object's angle/distance pairs into absolute X/Y drawing points.
- `MovementCalc` converts polar direction and speed into X/Y offsets.
- `DetectCollide4` is the active collision detection and response routine.
- `DoThrust` applies acceleration in a direction.
- `Shoot` creates bullets and handles repeated firing.
- `Explode` spawns particles and deactivates a destroyed ship.

## Recent Changes

- Added health and damage for both ships.
- Added visual health bars below the scores.
- Added green health pickups that restore 20% health.
- Changed scoring so points are awarded for round wins.
- Added explosion effects, winner messages, and automatic round resets.
- Added a central black hole with gravity and a visible event horizon.
- Updated the black hole so any object touching the visible event horizon is sucked in.
- Made a sucked-in ship immediately lose the round while the other player wins.
- Fixed input release handling with `KP(KeyCode) = 0`.
- Remapped Player 1 shooting from Ctrl to Up arrow.
- Restored timer-driven continuous shooting with a short cooldown.
- Redesigned the Player 1 ship polygon.
- Tuned player colors and draw behavior.
- Boosted both players' main thrust force from `7` to `20`.

## Notes And Known Quirks

- The code contains multiple collision routines (`DetectCollide`, `DetectCollide3`, and `DetectCollide4`). `DetectCollide4` is the active routine called from the main loop.
- `Timer1.Interval` is set to 5 ms, but the actual frame rate depends on drawing and physics workload.
- The project uses classic VB6 conventions and array-heavy game state, so many behaviors are controlled through numeric `SpaceObject` indexes.

## Planned Improvements

- Add sound effects for shooting and explosions.
- Improve asteroid splitting logic when bullets hit asteroids.
- Add a main menu or persistent game-over state.

## Using A Figma SVG

The helper script `tools/svg_to_vb_angles.py` converts an SVG path or SVG file into VB6 `SpaceObject` angle/radius assignment lines.

From the `tools` folder:

```bash
pip install -r requirements.txt
python svg_to_vb_angles.py --path "M...Z" --scale 1.1 --samples 800
```

The `--scale` flag changes the ship size. For example, `1.1` makes the ship 10% larger. You can also save a Figma SVG export to a file and use `--svg-file ship.svg` instead of `--path`.

## Credits

Original implementation by Professor Darren Martin. Gameplay enhancements, documentation, and visual updates were added as part of this project.
