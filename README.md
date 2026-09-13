# Tetris Game

**Creator: Evan**

A fully functional Tetris game built with Python and Pygame, featuring the classic original Tetris design with modern enhancements.

## Features

✅ **Fully Functional Gameplay**
- Classic Tetris mechanics with all 7 Tetromino pieces
- Smooth piece movement and rotation
- Line clearing with score calculations
- Progressive difficulty levels
- Fast and optimized game loop

✅ **Player Management**
- Player name input and score tracking
- High scores saved to file (scores.json)
- Top 10 scores display
- Persistent data storage between sessions

✅ **Original Tetris Design**
- Classic color scheme matching original Tetris
- Authentic piece colors and shapes
- Grid-based layout similar to the classic game
- Retro UI with period-appropriate fonts

✅ **Performance**
- Optimized 60 FPS game loop
- Fast collision detection
- Efficient grid management
- Minimal memory footprint

## Installation

1. Clone the repository:
```bash
git clone https://github.com/youngwarrior009/tetris-game-evan.git
cd tetris-game-evan
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

### Controls

**Menu:**
- `SPACE` - Start Game
- `H` - View High Scores
- `Q` - Quit

**During Gameplay:**
- `LEFT ARROW` - Move piece left
- `RIGHT ARROW` - Move piece right
- `DOWN ARROW` - Soft drop (move down one line)
- `UP ARROW` - Rotate piece
- `SPACE` - Hard drop (instantly drop to bottom)
- `P` - Pause (coming soon)

**Game Over:**
- `SPACE` - Save your score
- `Q` - Return to menu

### Scoring

- Single line: 100 points
- Double line: 300 points
- Triple line: 500 points
- Tetris (4 lines): 800 points

Level increases by 1 for every 10 lines cleared.

## Game Files

- `tetris.py` - Main game file
- `scores.json` - Player high scores (created automatically)
- `requirements.txt` - Python dependencies

## Running the Game

```bash
python tetris.py
```

## Game States

1. **Menu Screen** - Main menu with game title and options
2. **Playing** - Active gameplay
3. **Game Over** - Game over screen with score display
4. **Score Entry** - Enter player name for high score

## Technical Details

- **Language:** Python 3
- **Framework:** Pygame 2.5.2
- **Screen Resolution:** 800x900 pixels
- **Grid Size:** 10x20 blocks
- **FPS:** 60
- **Data Format:** JSON for score storage

## High Scores

Your scores are automatically saved to `scores.json` in the same directory as the game. The top 10 scores are displayed on the menu screen and saved persistently.

## Future Enhancements

- Sound effects
- Background music
- Pause functionality
- Multiple difficulty modes
- Statistics tracking
- Leaderboard system

---

**Creator:** Evan

Enjoy the classic game of Tetris!
