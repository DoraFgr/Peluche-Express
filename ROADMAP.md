# Peluche Express — Project Roadmap

A step-by-step guide to building the game, with checkboxes to track your progress.

## 1. Project Setup
- [x] Install Python and Pygame
- [x ] Set up the project folder structure
- [x ] Create a simple “Hello, World” Pygame window

## 2. Core Game Loop
- [X ] Display a start screen with a “Start Journey” button
- [x ] Show a simple clock (static for now)
- [ x] Transition to a basic game screen when starting

## 3. Player Controls & Movement
- [ x] Add a player character (placeholder image)
- [x ] Implement left/right movement, duck and jump
- [ x] Implement the right sprite for the right action

## 4. Map transition
### Map Transition Steps
- [ x] Define End Zone in Map: Add an "End Zone" object or tile in your Tiled map (e.g., in an "Objects" layer) and give it a unique name (e.g., "LevelEnd").
- [ x] Detect Player Entering End Zone: In your update logic, check if the player collides with the "End Zone" object.
- [ x] Add End Zone Sprite/Effect: Create or select a sprite for the end zone (e.g., portal, door, flag) and place it at the end of the map using Tiled or code.
- [ ] Trigger Transition State: When the player enters the end zone, set a state (e.g., `self.transitioning = True`). Disable player input and physics.
- [ ] Play Player Animation: Animate the player (e.g., waving, jumping, walking into portal). Optionally, fade out or move the player off-screen.
- [ ] Play End Zone Animation/Effect: Animate the end zone sprite (e.g., portal glow, door opening).
- [ ] Wait for Animation to Finish: Use a timer or frame count to wait for the animation to complete.
- [ x] Load Next Level: Call your `_go_to_next_level()` method. Reset all transition states and re-enable input.


## 4. Level Structure
- [ ] Create a simple level (one screen, flat ground)
- [ ] Add a “train arrives” and “train departs” animation (simple at first)
- [ ] Set up a way to move between levels (e.g., pressing a key)

## 5. Puzzle & Interaction
- [ ] Add a basic puzzle (e.g., drag an object to a target)
- [ ] Show a simple choice (with icons/images, not text)

## 6. Dog Encounter & Feeding
- [ ] Place a “dog” in the level (placeholder image)
- [ ] Trigger a feeding animation when the player reaches the dog

## 7. Clock & Progression
- [ ] Advance the clock after each level
- [ ] Move to the next level after feeding the dog

## 8. End Game Sequence
- [ ] After all levels, show a bedtime animation and gentle music

## 9. Polish & Extras
- [ ] Add collectibles (optional)
- [ ] Replace placeholder art with real photos and cartoon effects
- [ ] Add sound effects and music
- [ ] Add narration or voiceover (optional)
- [ ] Export the game as a Windows executable 