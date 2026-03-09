# Chess Bot with Pygame

A fully interactive **Chess Bot application** built using **Python, Pygame, and python-chess**.
This project provides a graphical chess interface where a user can play against an AI-powered chess engine with animated moves, undo/redo functionality, and legal move highlighting.

The project explores concepts from **game development, AI search algorithms, and graphical rendering** while implementing the rules and mechanics of chess.

---

## Features

* Interactive chess board built using **Pygame**
* Play against an **AI chess engine**
* **Move animations** for pieces
* **Undo / Redo functionality**
* **Pawn promotion support**
* **Legal move highlighting**
* Automatic **checkmate and draw detection**
* Clean modular architecture separating UI, rendering, and logic

---

## How the Chess Bot Works

The system uses the **python-chess library** to handle the game rules and board representation.

The **Pygame interface** handles:

* Board rendering
* Piece animation
* Mouse interactions
* User input
* Game state updates

The **AI engine** evaluates positions using Minimax with Alpha-Beta pruning to predict the best move.

## AI Algorithm (Minimax with Alpha-Beta Pruning)

The chess engine selects moves using the **Minimax algorithm enhanced with Alpha-Beta pruning**.

### Minimax Concept

Minimax is a decision-making algorithm used in two-player games such as chess.
The algorithm explores possible moves in a **game tree** and assumes that:

* The **AI player tries to maximize** the evaluation score.
* The **opponent tries to minimize** the evaluation score.

At each depth of the tree:

* **Max nodes** represent the AI player.
* **Min nodes** represent the opponent.

The algorithm evaluates board positions using a heuristic function and selects the move that leads to the **best possible outcome assuming optimal play from both sides**.

---

### Alpha-Beta Pruning

Alpha-Beta pruning is an optimization technique for Minimax.

It reduces the number of nodes evaluated by **cutting off branches that cannot affect the final decision**.

Two values are maintained:

* **Alpha (α)** → Best score the maximizing player can guarantee
* **Beta (β)** → Best score the minimizing player can guarantee

If at any point:

```
α ≥ β
```

the algorithm stops exploring that branch because it cannot influence the final decision.

This significantly **reduces computation time** while producing the same optimal move as standard Minimax.

---

### Game Tree Example

Below is a simplified example of a Minimax search tree.

```text
                    Root (AI)
                   Max Node
                 /           \
              Min             Min
            /     \         /     \
          Max     Max     Max     Max
          / \     / \     / \     / \
         3   5   6   9   1   2   0   -1
```

Evaluation flow:

1. Bottom values represent **evaluated board positions**.
2. Min nodes choose the **minimum value** from their children.
3. Max nodes choose the **maximum value** from their children.

Result propagation:

```
Min layer → [3,5] → 3
Min layer → [6,9] → 6
Min layer → [1,2] → 1
Min layer → [0,-1] → -1

Max layer → [3,6] → 6
Max layer → [1,-1] → 1

Root chooses → max(6,1) = 6
```

Therefore, the AI selects the move leading to the branch with score **6**.

---

### Why This Works Well for Chess

Minimax with Alpha-Beta pruning allows the engine to:

* Evaluate **many possible move sequences**
* Simulate **opponent responses**
* Avoid exploring unnecessary branches
* Select moves that maximize the engine's advantage

This approach is widely used in **classic chess engines** before the introduction of neural-network-based engines.


---

## Project Structure

```text
python-chess-engine/
│
├── img/                # Chess piece images
│
├── main.py             # Main game loop and UI controller
├── renderer.py         # Handles board drawing and animations
├── evaluation.py       # Chess engine logic and move evaluation
├── constants.py        # Game constants (board size, colors, etc.)
│
├── requirements.txt    # Project dependencies
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/aprataps4/python-chess-engine.git
cd python-chess-engine
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python main.py
```

---

## Controls

| Action       | Control                         |
| ------------ | ------------------------------- |
| Select piece | Left mouse click                |
| Move piece   | Left mouse click on destination |
| Undo move    | ← Left Arrow                    |
| Redo move    | → Right Arrow                   |
| Promotion    | Press Q, R, B, or K             |

---

## Example Gameplay

![Chess Gameplay](img/chess-demo.gif)

## Key Concepts Implemented

* Chess move generation
* Board evaluation
* Game state management
* Event-driven UI programming
* Animation using Pygame
* Modular Python project structure

---

## Possible Improvements

Future enhancements for the project:

* Add **difficulty levels**
* Improve **evaluation heuristics**
* Add **move history panel**
* Implement **storing the predicted move till now to reduce computational overload**

---

## Author

**Akhand Pratap Singh**

GitHub
https://github.com/aprataps4

LinkedIn
https://www.linkedin.com/in/akhand-pratap-singh-52978b28b/

Email
[2004akhandpsingh@gmail.com]

---

⭐ If you like this project, feel free to star the repository!

