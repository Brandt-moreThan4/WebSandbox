import random
from pathlib import Path
import sys

# PARENT_DIR = Path(__file__).resolve().parent.parent
# sys.path.append(str(PARENT_DIR))

from ml_mods.player import get_random_move



def get_bot_move(board) -> int | None:
    
    # Generate a list of available columns (not full)
    columns = len(board[0])

    # If the top row of the board is None, the column is not full
    available_cols = [col for col in range(7) if board[0][col] is None]

    # Randomly select a column for now
    if available_cols:
        return random.choice(available_cols)
    else:
        return None  # No moves available (game might be over)

def get_bot_move(board) -> int | None:
    
    return get_random_move(board)  # Call the function from the ml_mods package
