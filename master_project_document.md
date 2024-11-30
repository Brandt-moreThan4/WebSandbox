# Project Master File

## Project Structure

```
├── .env
├── .gitignore
├── .vscode
│   └── launch.json
├── __pycache__
│   └── app_1.cpython-312.pyc
├── app_1.py
├── backend
│   ├── __pycache__
│   │   ├── app.cpython-312.pyc
│   │   └── bot_logic.cpython-312.pyc
│   ├── app.py
│   ├── bot_logic.py
│   ├── requirements.txt
│   └── toy.py
├── frontend
│   ├── index.html
│   ├── script.js
│   └── style.css
├── ml_mods
│   ├── __pycache__
│   │   └── player.cpython-312.pyc
│   └── player.py
├── toy.py
└── utils.py
```

## C:\Users\User\OneDrive\Desktop\Code\WebSandbox\app_1.py

```py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import time
from backend.bot_logic import get_bot_move
from dotenv import load_dotenv
import os

# # Load environment variables from .env file
# load_dotenv()

# Initialize the Flask app with the correct static folder
app = Flask(__name__, static_folder='frontend', static_url_path='')
# CORS(app)

@app.route('/')
def serve_index():
    """
    Serve the index.html page from the frontend directory.
    """
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/move', methods=['POST'])
def get_move():
    """
    Handle requests from the frontend to get the bot's move.
    Expects a JSON payload with the current board state.
    """
    data = request.json
    board = data.get('board')  # Get the current board state from the request

    if board is None:
        return jsonify({"error": "Board state not provided"}), 400

    try:
        # Call the function to determine the bot's move
        col = get_bot_move(board)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    time.sleep(1)  # Simulate human-like delay

    return jsonify({"column": col})

if __name__ == '__main__':
    # Start the Flask app
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")

```

## C:\Users\User\OneDrive\Desktop\Code\WebSandbox\toy.py

```py
from pathlib import Path


p = Path()
print(p)
print(p.cwd())
print(p.absolute())
print(__file__)
```

## C:\Users\User\OneDrive\Desktop\Code\WebSandbox\utils.py

```py
import os
import json
from pathlib import Path

def get_folder_tree(folder_path, exclusions=None, indent=''):
    if exclusions is None:
        exclusions = []

    tree_structure = ""
    try:
        # Get a list of all items in the current directory
        items = os.listdir(folder_path)
    except PermissionError:
        tree_structure += f"{indent}[Permission Denied]\n"
        return tree_structure

    # Loop through each item in the folder
    for index, item in enumerate(sorted(items)):
        # Skip any item in the exclusions list
        if item in exclusions:
            continue

        # Construct the full item path
        item_path = os.path.join(folder_path, item)
        # Build the tree structure string
        connector = '├── ' if index < len(items) - 1 else '└── '
        tree_structure += f"{indent}{connector}{item}\n"

        # If the item is a directory, recursively get its contents
        if os.path.isdir(item_path):
            new_indent = indent + ('│   ' if index < len(items) - 1 else '    ')
            tree_structure += get_folder_tree(item_path, exclusions, new_indent)

    return tree_structure

def create_master_markdown(folder_path, output_file='master_project_document.md',exclusions=None):
    if exclusions is None:
        exclusions = []

    # Create the master Markdown content
    markdown_content = "# Project Master File\n\n"
    markdown_content += "## Project Structure\n\n"
    markdown_content += "```\n"
    markdown_content += get_folder_tree(folder_path, exclusions)
    markdown_content += "```\n\n"

    # Traverse the folder to add each code file's content
    for root, _, files in os.walk(folder_path):
        # Skip excluded directories
        if any(exclusion in root for exclusion in exclusions):
            continue
        for file in files:
            # Skip excluded files
            if file in exclusions:
                continue

            # Get the full file path
            file_path = os.path.join(root, file)

            # Only include text/code files (you can add more extensions as needed)
            if file.endswith(('.py', '.js', '.html', '.css', '.md', '.java', '.txt', '.sh')):
                markdown_content += f"## {file_path}\n\n"
                markdown_content += "```" + file.split('.')[-1] + "\n"
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        markdown_content += f.read()
                except Exception as e:
                    markdown_content += f"Error reading file: {e}"
                markdown_content += "\n```\n\n"

    # Write the content to a master Markdown file
    with open(output_file, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)


def combine_jsons(folder_path, output_file='combined.json', exclusions:list=None):
    if exclusions is None:
        exclusions = []

    combined_data = []
    for root, _, files in os.walk(folder_path):
        # Skip excluded directories
        if any(exclusion in root for exclusion in exclusions):
            continue
        for file in files:
            # Skip excluded files
            if file in exclusions:
                continue
            if any(exclusion in file for exclusion in exclusions):
                continue

            # Get the full file path
            file_path = os.path.join(root, file)

            # Only include JSON files
            if file.endswith('.json'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # combined_data.append(data)
                        combined_data.extend(data)
                except Exception as e:
                    print(f"Error reading file: {e}")

    # Write the combined data to a single JSON file
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(combined_data, json_file, indent=4)


if __name__ == "__main__":


    # Example usage:
    FOLDER = r'C:\Users\User\OneDrive\Desktop\Code\WebSandbox'
    # FOLDER = r'C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training'
    EXCLUSIONS = ['.git', 'node_modules','ipynb']  # Add any other folder/file names you want to exclude

    create_master_markdown(FOLDER, exclusions=EXCLUSIONS)

    # # Combine all JSON files in the folder and subfolders
    # DATA_FOLDER = Path(FOLDER) / 'data'
    # DATA_Exclusions = ['stable','old']
    # combine_jsons(DATA_FOLDER, output_file=DATA_FOLDER / 'combined.json', exclusions=DATA_Exclusions)
```

## C:\Users\User\OneDrive\Desktop\Code\WebSandbox\backend\app.py

```py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # Import the CORS module
import time

# Add the parent directory to the path if it isn't there already
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.bot_logic import get_bot_move  # Adjust import path if necessary

# Initialize the Flask app
app = Flask(__name__, static_folder="../frontend", static_url_path="/")
CORS(app)  # Enable CORS for all routes

@app.route('/')
def serve_index():
    """
    Serve the index.html page from the frontend directory.
    """
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/move', methods=['POST'])
def get_move():
    """
    Handle requests from the frontend to get the bot's move.
    Expects a JSON payload with the current board state.
    """
    data = request.json
    board = data.get('board')  # Get the current board state from the request

    if board is None:
        return jsonify({"error": "Board state not provided"}), 400

    try:
        # Call the function to determine the bot's move
        col = get_bot_move(board)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    time.sleep(1)  # Simulate human-like delay

    return jsonify({"column": col})

if __name__ == '__main__':
    app.run(debug=True)

```

## C:\Users\User\OneDrive\Desktop\Code\WebSandbox\backend\bot_logic.py

```py
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

```

## C:\Users\User\OneDrive\Desktop\Code\WebSandbox\backend\requirements.txt

```txt

```

## C:\Users\User\OneDrive\Desktop\Code\WebSandbox\backend\toy.py

```py
from pathlib import Path


p = Path()
print(p)
print(p.cwd())
print(p.absolute())
print(__file__)
```

## C:\Users\User\OneDrive\Desktop\Code\WebSandbox\frontend\index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Connect 4 Game</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Connect 4</h1>
    <div id="board">
        <!-- Manually creating a 6x7 board (6 rows, 7 columns) -->
        <!-- Row 1 -->
        <div class="cell" data-row="0" data-col="0"></div>
        <div class="cell" data-row="0" data-col="1"></div>
        <div class="cell" data-row="0" data-col="2"></div>
        <div class="cell" data-row="0" data-col="3"></div>
        <div class="cell" data-row="0" data-col="4"></div>
        <div class="cell" data-row="0" data-col="5"></div>
        <div class="cell" data-row="0" data-col="6"></div>
        <!-- Row 2 -->
        <div class="cell" data-row="1" data-col="0"></div>
        <div class="cell" data-row="1" data-col="1"></div>
        <div class="cell" data-row="1" data-col="2"></div>
        <div class="cell" data-row="1" data-col="3"></div>
        <div class="cell" data-row="1" data-col="4"></div>
        <div class="cell" data-row="1" data-col="5"></div>
        <div class="cell" data-row="1" data-col="6"></div>
        <!-- Row 3 -->
        <div class="cell" data-row="2" data-col="0"></div>
        <div class="cell" data-row="2" data-col="1"></div>
        <div class="cell" data-row="2" data-col="2"></div>
        <div class="cell" data-row="2" data-col="3"></div>
        <div class="cell" data-row="2" data-col="4"></div>
        <div class="cell" data-row="2" data-col="5"></div>
        <div class="cell" data-row="2" data-col="6"></div>
        <!-- Row 4 -->
        <div class="cell" data-row="3" data-col="0"></div>
        <div class="cell" data-row="3" data-col="1"></div>
        <div class="cell" data-row="3" data-col="2"></div>
        <div class="cell" data-row="3" data-col="3"></div>
        <div class="cell" data-row="3" data-col="4"></div>
        <div class="cell" data-row="3" data-col="5"></div>
        <div class="cell" data-row="3" data-col="6"></div>
        <!-- Row 5 -->
        <div class="cell" data-row="4" data-col="0"></div>
        <div class="cell" data-row="4" data-col="1"></div>
        <div class="cell" data-row="4" data-col="2"></div>
        <div class="cell" data-row="4" data-col="3"></div>
        <div class="cell" data-row="4" data-col="4"></div>
        <div class="cell" data-row="4" data-col="5"></div>
        <div class="cell" data-row="4" data-col="6"></div>
        <!-- Row 6 -->
        <div class="cell" data-row="5" data-col="0"></div>
        <div class="cell" data-row="5" data-col="1"></div>
        <div class="cell" data-row="5" data-col="2"></div>
        <div class="cell" data-row="5" data-col="3"></div>
        <div class="cell" data-row="5" data-col="4"></div>
        <div class="cell" data-row="5" data-col="5"></div>
        <div class="cell" data-row="5" data-col="6"></div>
    </div>
    <p id="status"></p>
    <script src="script.js"></script>
</body>
</html>

```

## C:\Users\User\OneDrive\Desktop\Code\WebSandbox\frontend\script.js

```js
const columns = 7;
const rows = 6;
let currentPlayer = 'red';
let board = Array(rows).fill(null).map(() => Array(columns).fill(null));

// Display initial status
document.getElementById('status').textContent = `${currentPlayer.toUpperCase()}'s turn`;

// Attach click event listeners to all cells
const cells = document.querySelectorAll('.cell');
cells.forEach(cell => {
    cell.addEventListener('click', handleCellClick);
});

function handleCellClick(event) {
    // Only allow player moves if it's their turn
    if (currentPlayer !== 'red') return;

    const col = parseInt(event.target.dataset.col);

    // Find the lowest available row in the selected column
    for (let r = rows - 1; r >= 0; r--) {
        if (!board[r][col]) {
            // Update the board state
            board[r][col] = currentPlayer;

            // Find the cell element in the DOM using data attributes
            const cell = document.querySelector(`.cell[data-row='${r}'][data-col='${col}']`);
            cell.classList.add('taken', currentPlayer);

            // Check if the move results in a win
            if (checkWin(r, col)) {
                document.getElementById('status').textContent = `${currentPlayer.toUpperCase()} wins!`;
                disableBoard();
            } else {
                // Switch to the bot's turn
                currentPlayer = 'yellow';
                document.getElementById('status').textContent = `Bot's turn...`;

                // Call function to get the bot's move
                getBotMove(board);
            }
            break;
        }
    }
}

async function getBotMove(board) {
    try {
        // Make a request to the backend to get the bot's move
        const response = await fetch('http://127.0.0.1:5000/api/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                board: board,
                player: 'bot', // Optional, if needed by your backend logic
            }),
        });

        const data = await response.json();
        const botCol = data.column;

        // Handle the bot's move
        if (botCol !== null) {
            for (let r = rows - 1; r >= 0; r--) {
                if (!board[r][botCol]) {
                    // Update the board state
                    board[r][botCol] = currentPlayer;

                    // Find the cell element in the DOM
                    const cell = document.querySelector(`.cell[data-row='${r}'][data-col='${botCol}']`);
                    cell.classList.add('taken', currentPlayer);

                    // Check if the bot's move results in a win
                    if (checkWin(r, botCol)) {
                        document.getElementById('status').textContent = `${currentPlayer.toUpperCase()} wins!`;
                        disableBoard();
                    } else {
                        // Switch back to the player's turn
                        currentPlayer = 'red';
                        document.getElementById('status').textContent = `${currentPlayer.toUpperCase()}'s turn`;
                    }
                    break;
                }
            }
        }
    } catch (error) {
        console.error('Error getting bot move:', error);
        document.getElementById('status').textContent = 'Error getting bot move. Try again.';
    }
}

function disableBoard() {
    cells.forEach(cell => cell.removeEventListener('click', handleCellClick));
}

function checkWin(row, col) {
    // Helper function to count consecutive pieces in a specified direction
    function count(directionRow, directionCol) {
        let r = row + directionRow;
        let c = col + directionCol;
        let count = 0;

        // Continue counting while within board bounds and pieces match the current player
        while (
            r >= 0 &&
            r < rows &&
            c >= 0 &&
            c < columns &&
            board[r][c] === currentPlayer
        ) {
            count++;
            r += directionRow; // Move in the specified row direction
            c += directionCol; // Move in the specified column direction
        }
        return count; // Return the count of matching pieces
    }

    // Check for four-in-a-row in various directions
    return (
        count(0, 1) + count(0, -1) >= 3 || // Horizontal check (left + right)
        count(1, 0) + count(-1, 0) >= 3 || // Vertical check (up + down)
        count(1, 1) + count(-1, -1) >= 3 || // Diagonal \ (bottom-left to top-right)
        count(1, -1) + count(-1, 1) >= 3   // Diagonal / (bottom-right to top-left)
    );
}

```

## C:\Users\User\OneDrive\Desktop\Code\WebSandbox\frontend\style.css

```css
body {
    font-family: Arial, sans-serif;
    text-align: center;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
}

h1 {
    margin-top: 20px;
}

#board {
    display: grid;
    grid-template-columns: repeat(7, 50px); /* 7 columns */
    grid-gap: 5px;
    margin: 20px auto;
    max-width: 400px;
    border: 2px solid #000;
}

.cell {
    width: 50px;
    height: 50px;
    background-color: #f1f1f1;
    border: 1px solid #ccc;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}

.cell.taken {
    cursor: not-allowed;
}

.cell.red {
    background-color: red;
}

.cell.yellow {
    background-color: yellow;
}

#status {
    margin-top: 15px;
    font-size: 18px;
}

```

## C:\Users\User\OneDrive\Desktop\Code\WebSandbox\ml_mods\player.py

```py
import random

def get_random_move(board) -> int | None:
    
    # Generate a list of available columns (not full)
    columns = len(board[0])

    # If the top row of the board is None, the column is not full
    available_cols = [col for col in range(7) if board[0][col] is None]

    # Randomly select a column for now
    if available_cols:
        return random.choice(available_cols)
    else:
        return None  # No moves available (game might be over)
```

