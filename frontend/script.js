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
        // Use a relative path for the API endpoint
        const response = await fetch('/api/move', {
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
