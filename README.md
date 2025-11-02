# Peluche Express

A gentle adventure game for young children, vibe coded with Python and Pygame .

## Project Structure

```
Peluche Express/
├── venv/                   # Virtual environment 
├── requirements.txt        # List of Python dependencies
├── README.md               # Project overview and instructions
├── ROADMAP.md              # Project roadmap/checklist
├── main.py                 # Entry point for your game
├── src/                # Python package for your game code
│   ├── __init__.py
│   ├── game.py             # Main game loop and logic
│   ├── player.py           # Player character logic
│   ├── level.py            # Level structure and logic
│   ├── puzzle.py           # Puzzle mechanics
│   ├── dog.py              # Dog encounter/feeding logic
│   └── ...                 # More modules as needed
├── assets/                 # All game assets
│   ├── images/             # Sprites, backgrounds, etc.
│   ├── audio/              # Music and sound effects
│   └── fonts/              # Custom fonts (if any)
├── data/                   # Game data (levels, dialogues, etc. in JSON/YAML)
├── script/                 # Utility scripts (like env_setup.sh)
│   └── env_setup.sh
└── Whitepaper.md           # Design document
```

### Folder & File Descriptions

- **venv/**: Your Python virtual environment (not tracked by version control).
- **requirements.txt**: List of Python packages to install (e.g., `pygame`).
- **README.md**: This file. Project description and instructions.
- **ROADMAP.md**: Your development checklist and roadmap.
- **main.py**: The main script to launch your game.
- **peluche/**: All your Python code, organized by feature.
- **assets/**: All images, sounds, and fonts for the game.
- **data/**: Level layouts, dialogue, and other structured data (JSON/YAML).
- **script/**: Utility scripts (setup, build, etc.).
- **Whitepaper.md**: Your game design document.

---

## Getting Started

1. Set up your virtual environment and install dependencies (see `script/env_setup.sh`).
2. Run `main.py` to start the game (to be implemented).
3. Use the `ROADMAP.md` to track your progress.

---

For more details, see the whitepaper and roadmap files.