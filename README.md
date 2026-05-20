Asteroids (VB6)
=================

Brief project overview
This is an Asteroids-style game written in Visual Basic 6. It uses arrays named `SpaceObject` to represent ships, asteroids and bullets, a `PictureBox` called `Picture1` as the drawing surface, and a `Timer` for the main update loop.

Files of interest
- `Form1.frm` - main form, UI setup and the main timer loop (physics update, collision calls and drawing).
- `Module1.bas` - global variables, data structures and helper routines (movement math, collision detection, shooting, etc.).
- `asteroids.vbp` / `asteroids.vbw` - VB6 project and workspace files.

What this project contains
Each object is stored in `SpaceObject(objIndex, propertyIndex)`. Important properties include existence, screen position, orientation, velocity, mass and an angle/radius list that defines the polygonal shape.

The project now includes:
- **Health System**: Ships have 100% health, taking damage when hit by bullets.
- **Energy Products**: Green plus shapes (+) that spawn periodically and restore health.
- **Winning Logic**: Scores track round wins rather than individual hits.
- **Black Hole**: A massive gravity well in the center of the screen that pulls everything toward it. Anything that touches the visible event horizon is sucked in; if a ship is sucked in, the other player wins the round.

Key routines
- `MakeCoords` converts an object's angle/distance pairs into absolute XY points for drawing.
- `MovementCalc` converts polar direction/speed into X/Y offsets.
- `DetectCollide4` is the primary collision detection and response routine used by the game.
- `Explode` spawns particles and deactivates a ship when its health reaches zero.

Game loop behavior
The main loop runs on `Timer1` and updates key state, rotation, player thrust, object movement (with screen wrapping), draw coordinates, collision detection, health/energy spawning, and drawing to `Picture1`.

How to run
Open the project in the Visual Basic 6 IDE using `asteroids.vbp` and press Run (F5). VB6 is required to build and run this project as provided.

Controls (as implemented in the code)
- Player 1 (Blue ship):
  - Rotate left/right: Left arrow / Right arrow
  - Thrust: Down arrow, using the stronger main engine force.
  - Shoot: Up arrow — hold to fire repeatedly; there is a short cooldown to control fire rate.
- Player 2 (Red ship):
	- Rotate left/right: A / D
	- Thrust: S, using the stronger main engine force.
	- Shoot: G

Notes and known quirks
- The code includes multiple collision routines (`DetectCollide`, `DetectCollide3`, `DetectCollide4`). `DetectCollide4` is the active routine called from the main loop.
- The timer interval is set to 5 ms, but actual frame rate will be limited by the computations and drawing time.

Credits
Original implementation by my professor Darren Martin. Major gameplay enhancements (Health, Energy, Scoring, Round Resets) implemented by me.

Assignment status and immediate next steps
Status: Completed major gameplay features (Health, Energy, Winning Logic, Visual UI Improvements).

Planned next improvements
- Add sound effects for shooting and explosions.
- Improve asteroid splitting logic when hit by bullets.
- Add a main menu or "Game Over" persistent state.

Changes I made
 - **Health and Damage System**: Implemented a health system where ships start at 100% health and lose 10% when hit by an opponent's bullet.
 - **Visual Health Bars**: Added green health bars that deplete against a grey background, positioned below the scores.
 - **Energy Products (Pickups)**: Created green plus-shaped (+) items that spawn periodically and restore 20% health on collision.
 - **Win-Based Scoring**: Refined the scoring logic so that players earn points only by winning a round (depleting opponent's health to 0), rather than for every hit.
 - **Destruction and Reset**: Added a dramatic explosion effect upon ship destruction, a color-coded "Blue/Red Wins!" message, and an automatic round reset after a short delay.
 - **Black Hole Gravity & Visuals**: Implemented a central black hole with gravitational pull. Ships, asteroids, bullets, and pickups are pulled toward the center. The visible event horizon now sucks in any object that touches it, and a sucked-in ship immediately loses the round.
 - **Fixed input-release handling**: corrected the `Picture1_KeyUp` handler to properly clear key state (`KP(KeyCode) = 0`).
 - **Remapped Player 1 fire button**: moved Player 1 shooting from Ctrl to Up arrow (keycode 38).
 - **Restored timer-driven continuous shooting**: Player 1 now fires while the Up arrow is held instead of only on key release.
 - **Added firing cooldown**: implemented a ~150 ms cooldown inside `Shoot(SON)` to control fire rate.
 - **Redesigned Player 1 ship**: replaced ship polygon with a larger modern design and added visual accents.
 - **Color and draw tweaks**: set Player 1 to Cyan (Blue) and Player 2 to a Warm Red, with improved rendering using `DrawMode = 13` for consistent UI colors.
 - **Boosted rocket thrust**: increased both players' main engine force from `7` to `20` in the timer-loop thrust controls for stronger acceleration.

Files edited
 - `Form1.frm` — Main game loop, UI drawing (scores, health bars, winner messages), energy spawning, and round reset logic.
 - `Module1.bas` — Global variables (`Health`, `RoundOver`, etc.), explosion routine, and refined collision/damage logic.
 - `README.md` — Documented all features and changes.


Using your Figma SVG
 - I added a small helper script at `tools/svg_to_vb_angles.py` that converts an SVG path (or SVG file) into VB6 `SpaceObject` angle/radius assignments. It uses `svgpathtools` and prints assignment lines you can paste into `Form1.frm`.
 - Usage (from the `tools` folder):

```bash
pip install -r requirements.txt
python svg_to_vb_angles.py --path "M...Z" --scale 1.1 --samples 800
```

 - The `--scale` flag lets you make the ship slightly bigger (1.1 = 10% larger). If you prefer, save your Figma SVG export to a file and use `--svg-file ship.svg` instead of `--path`.


