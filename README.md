# Sudoku Solver and Playable Board

A Pygame board for entering a Sudoku puzzle, highlighting conflicts, requesting a hint, and watching a backtracking solver search for solutions.

## Solver

The solver uses the minimum-remaining-values (MRV) heuristic: at each step it selects the empty cell with the fewest legal candidates. This narrows the search earlier than choosing the first empty cell.

## Controls

- Click a cell and press 1–9 to enter a value.
- S or Enter — solve.
- H — request a hint.
- N — cycle through found solutions.
- F1–F5 — load a sample puzzle.
- R — clear the board.
- L — lock entered values as givens.

## Run

    python -m pip install -r requirements.txt
    python main.py

The solver caps its result list at 300 solutions so an empty grid cannot create an unbounded collection. It is an educational solver and interface, not a puzzle generator or difficulty-rating system.
