# Build Instructions for Peluche Express

## Quick Build

Simply run the build script:

```bash
./build_game.sh
```

## What it does

The build script will:
1. ✅ Check if you're in the right directory
2. ✅ Verify virtual environment exists  
3. ✅ Activate the virtual environment
4. ✅ Install PyInstaller if needed
5. ✅ Clean previous builds
6. ✅ Build the executable using PyInstaller
7. ✅ Show build results and file size

## Requirements

- Virtual environment set up with `venv`
- All dependencies installed (`pip install -r requirements.txt`)
- Bash shell (Git Bash on Windows works fine)

## Output

After successful build, you'll find:
- `dist/PelucheExpress.exe` - Your standalone game executable (≈45MB)
- Ready to share with anyone - no Python installation required!

## Testing

To test your built game:
```bash
cd dist
./PelucheExpress.exe
```

## Troubleshooting

If build fails:
1. Make sure you're in the project root directory
2. Check that `venv` directory exists
3. Verify all dependencies are installed
4. Check the error output for specific issues

## Manual Build (alternative)

If you prefer to build manually:
```bash
source venv/Scripts/activate
pyinstaller --clean peluche_express.spec
```
