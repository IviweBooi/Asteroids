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

Key routines
- `MakeCoords` converts an object's angle/distance pairs into absolute XY points for drawing.
- `MovementCalc` converts polar direction/speed into X/Y offsets.
- `DetectCollide4` is the primary collision detection and response routine used by the game.

Game loop behavior
The main loop runs on `Timer1` and updates key state, rotation, thrust, object movement (with screen wrapping), draw coordinates, collision detection and drawing to `Picture1`.

How to run
Open the project in the Visual Basic 6 IDE using `asteroids.vbp` and press Run (F5). VB6 is required to build and run this project as provided.

Controls (as implemented in the code)
- Player 1 (object index 0):

- Player 1 (object index 0):
  - Rotate left/right: Left (37) / Right (39)
  - Thrust: Down (40)
  - Shoot: Up arrow (38) — hold to fire repeatedly; there is a short cooldown to control fire rate.
- Player 2 (object index 3):
	- Rotate left/right: A (65) / D (68)
	- Thrust: S (83)
	- Shoot: G (71)

Notes and known quirks
- The code includes multiple collision routines (`DetectCollide`, `DetectCollide3`, `DetectCollide4`). `DetectCollide4` is the active routine called from the main loop.
- There are small code issues that I plan to address, for example `KP(KeyCode) = 0 = 0` in `Picture1_KeyUp` which should clear key state, and some harmless leftover lines like `X = X`.
- The timer interval is set to 5 ms, but actual frame rate will be limited by the computations and drawing time.

Credits
Original implementation by my professor Darren Martin. I have not made any code changes yet; this README is my first addition for the assignment.

Assignment status and immediate next steps
Status: I have not modified the original game code yet; this README documents the starting point.

Planned next improvements
- Fix input-release behavior so key states clear correctly.
- Add a changelog and commit history as I make changes.
- Simplify and improve collision performance.
- Add clearer build/run instructions and consider extracting testable logic for unit tests.

Changes I made
 - Fixed input-release handling: corrected the `Picture1_KeyUp` handler to properly clear key state (`KP(KeyCode) = 0`) and removed the single-shot-on-release behavior.
 - Remapped Player 1 fire button: moved Player 1 shooting from Ctrl to Up arrow (keycode 38).
 - Restored timer-driven continuous shooting: Player 1 now fires while the Up arrow is held (timer loop calls `Shoot(0)`) instead of only on key release.
 - Added firing cooldown: implemented a ~150 ms cooldown inside `Shoot(SON)` in `Module1.bas` to control fire rate during continuous fire.
 - Redesigned Player 1 ship: replaced `SpaceObject(0, 10..) ` polygon entries with a larger modern polygon and added small colored PSet accents at the ship centre for visual flair.
 - Color and draw tweaks: set Player 1 outline to cyan (`RGB(0,150,255)`) and Player 2 to a warm tint (`RGB(255,100,100)`), plus small highlight pixels around Player 1.
 - Tuned thrust: increased main thrust responsiveness for both players — final configured thrust value is `7` (previously experimented with `100`, then reduced to `7`).
 - Minor cleanups: removed/cleared some leftover debug lines and fixed small drawing quirks to improve playability.

Files edited
 - `Form1.frm` — fixed key-up handling, remapped Player 1 shoot to Up arrow, enabled hold-to-fire, updated Player 1 polygon and colors, tuned `DoThrust` calls to use thrust = 7, and added small PSet accents.
 - `Module1.bas` — added the ~150 ms cooldown check inside `Shoot(SON)` to throttle continuous firing.
 - `README.md` — updated to first-person voice and expanded this changes summary.


Files I edited
- `Form1.frm` — fixed key-up handling, moved Player 1 shooting to be timer-driven (Up arrow), removed single-shot on KeyUp.
- `Module1.bas` — added a 150 ms cooldown in `Shoot(SON)`.
- `README.md` — updated to first-person voice and added this summary of changes.

Notes
These changes are intentionally small and focused on input and firing behavior as the first assignment step. I have not altered collision physics or drawing logic yet; those are planned next steps.


