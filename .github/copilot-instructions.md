# Copilot Instructions for Peluche Express

## Project Overview
- **Peluche Express** is a gentle adventure/platformer game for children, built with Python and Arcade (not Pygame).
- Main entry point: `main.py` instantiates `PelucheExpress` from `src/game.py`.
- Game logic is modularized in `src/`:
  - `game.py`: Main game loop and orchestration (delegates to modules)
  - `player.py`: Player logic and animation
  - `resource_utils.py`: Asset path helpers
  - `apple_manager.py`: Apple collection logic
  - `camera_utils.py`: Camera following and deadzone logic
  - `ui_draw.py`: UI and screen drawing helpers
  - `level_manager.py`: Level loading, switching, and reset
  - `level_exit.py`: End zone/level exit logic
  - `input_handler.py`: Input and player movement
  - `state_manager.py`: State transitions and level exit update
- Assets (sprites, backgrounds, etc.) are in `assets/images/` and referenced via `get_resource_path()`.
- Level configuration is loaded from `config/levels.json`.

## Architecture & Patterns
- **Game Loop**: Managed by `arcade.Window` subclass (`PelucheExpress`).
- **State Management**: Game states include `main_screen`, `transition_screen`, `game`, and `level_exit`. State transitions are handled in `state_manager.py` and `level_manager.py`.
- **Player Logic**: `Player` class in `player.py` manages animation, movement, and input. Animation frames use seahorse sprites from `assets/images/advanced/Player/shp1/`.
- **Scene & Tilemaps**: Levels use Arcade's tilemap system. Scene objects are managed via `arcade.Scene` and sprite lists.
- **Apple Collection**: Apples are tracked and displayed with a custom counter in the UI, logic in `apple_manager.py`.
- **Camera**: Camera follows the player with deadzone logic in `camera_utils.py`.

## Developer Workflows
- **Run the Game**: Execute `python main.py` from the project root.
- **Build**: Use `build_exe.bat` (Windows) or `build_game.sh` (Linux/macOS) for packaging. See `BUILD.md` for details.
- **Environment Setup**: Use `script/env_setup.sh` to set up Python environment and install dependencies from `requirements.txt`.
- **Assets**: Add new images/sprites to appropriate subfolders in `assets/images/`. Reference them using `get_resource_path()`.
- **Levels**: Edit or add levels in `config/levels.json` and corresponding tilemaps in `tilemaps/`.

## Conventions & Patterns
- **Resource Loading**: Always use `get_resource_path()` for asset paths to ensure cross-platform compatibility.
- **Animation**: Player animation states are managed by texture switching in `Player.update()`. Use `walk_textures`, `jump_textures`, etc.
- **Input Handling**: All key input is processed via `input_handler.py` and game state logic in `game.py`.
- **State Transitions**: Use the `state` attribute in `PelucheExpress` to control screen transitions. Transition logic is in `state_manager.py` and `level_manager.py`.
- **Physics**: Platformer physics are managed by `arcade.PhysicsEnginePlatformer`.

## Integration Points
- **Arcade Library**: Core game loop, rendering, input, and physics.
- **External Data**: Level configs (`config/levels.json`), tilemaps (`tilemaps/*.tmx`).

## Examples
- To add a new player animation, update the relevant texture lists in `Player.__init__()` and reference new asset files.
- To add a new level, update `config/levels.json` and create a new `.tmx` file in `tilemaps/`.
- To add new game logic, create a new module in `src/` and import it in `game.py` as needed.

---

For more details, see `README.md`, `BUILD.md`, and `ROADMAP.md`.
