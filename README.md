# AI Escape Room Project

## Overview
This project is an AI-driven escape room game implemented in Python using Pygame.
The game features an intelligent agent that must navigate through various rooms, solve challenges, and collect keys to progress through multiple levels.

## Features
- **Multiple Search Algorithms**:
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - A* Pathfinding
- **Various Challenge Types**:
  - Riddles
  - Quote Completion
  - Caesar Cipher Decryption
- **Progressive Difficulty**:
  - Three distinct levels
  - Increasing complexity in pathfinding
  - Different combinations of challenges

## Game Components
### Grid System
- 5x3 grid layout
- Traversable and non-traversable cells
- Unique cell identifiers (e.g., 'a1', 'b2', 'c3')
- Exit point and multiple starting positions

### Agent
- Autonomous movement
- Key collection capability
- Challenge interaction
- Multiple movement strategies

### Challenges
1. **Riddles**: Text-based puzzles requiring logical thinking
2. **Quote Challenges**: Fill in missing words from famous quotes
3. **Caesar Cipher**: Decode encrypted messages using shift ciphers

## Project Structure
```
AI PROJECT/
├── assets/
│   ├── agent.png
│   └── key.png
├── classes/
│   ├── challenges/
│   │   ├── CaesarCipher.py
│   │   ├── QuoteChallenge.py
│   │   └── Riddle.py
│   ├── agent.py
│   ├── cell.py
│   ├── door.py
│   ├── game.py
│   ├── key.py
│   ├── level.py
│   └── state.py
├── utils/
│   ├── constants.py
│   └── helpers.py
└── main.py
```

## Installation Requirements
- Python 3.x
- Pygame library
- Required Python packages:
  ```
  pip install pygame
  ```

## How to Run
1. Clone the repository
2. Install the required dependencies
3. Run the main script:
   ```
   python main.py
   ```

## Gameplay Instructions
1. Click a valid starting position when prompted
2. Watch the AI agent navigate through the room
3. Solve challenges when encountering keys:
   - Type your answers for riddles
   - Complete missing words in quotes
   - Decrypt Caesar cipher messages
4. Collect all keys before reaching the exit
5. Progress through all three levels to complete the game

## Technical Details
### Pathfinding Algorithms
- **Level 1**: Uses BFS for optimal path finding
- **Level 2**: Implements DFS for exploration
- **Level 3**: Utilizes A* algorithm with Manhattan distance heuristic

### Challenge System
Each challenge is implemented as a separate class with:
- Initialization parameters
- Verification methods
- Reset functionality
- State tracking

### Scoring System
- Points awarded for:
  - Completing challenges
  - Collecting keys
  - Finishing levels
