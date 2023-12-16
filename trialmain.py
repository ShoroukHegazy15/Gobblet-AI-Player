class GobbletGameState:
    def __init__(self):
        # Define constants for player identification
        self.EMPTY = 0
        self.WHITE_PLAYER = 1
        self.BLACK_PLAYER = 2

        # Define the size of the board (adjust as needed)
        self.BOARD_SIZE = 4

        # Initialize an empty board
        self.board = [[self.EMPTY] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]

        # Initialize the current player to move
        self.current_player = self.WHITE_PLAYER

        # Store the dragged piece and its position
        self.dragged_piece = None
        self.dragged_piece_position = None

    def initialize_game_state(self):
        # Reset the board to its initial state
        self.board = [[self.EMPTY] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]

        # Set the starting player
        self.current_player = self.WHITE_PLAYER

        # Reset dragged piece information
        self.dragged_piece = None
        self.dragged_piece_position = None

    def print_board(self):
        for row in self.board:
            print(row)

    def update_board(self, new_board):
        # Update the board state with a new configuration
        self.board = new_board

    def set_dragged_piece(self, piece, position):
        # Set the dragged piece and its position
        self.dragged_piece = piece
        self.dragged_piece_position = position

    def clear_dragged_piece(self):
        # Clear the dragged piece information
        self.dragged_piece = None
        self.dragged_piece_position = None

def make_move(self, move):
        # Ensure the move is valid
        if self.is_valid_move(move.start_position, move.end_position):
            # Create a new board to represent the updated state
            new_board = [row[:] for row in self.board]

            # Make the move on the new board
            start_row, start_col = move.start_position
            end_row, end_col = move.end_position
            new_board[end_row][end_col] = new_board[start_row][start_col]
            new_board[start_row][start_col] = self.EMPTY

            # Create a new game state with the updated board
            new_game_state = GobbletGameState()
            new_game_state.update_board(new_board)
            new_game_state.current_player = self.current_player  # Assuming you want to keep the same player

            # Clear the dragged piece information in the new game state
            new_game_state.clear_dragged_piece()

            # Switch to the next player in the new game state
            new_game_state.switch_player()

            # Check for game over conditions in the new game state
            if new_game_state.is_game_over():
                print("Game Over. Winner:", new_game_state.get_winner())
                # You might want to handle the end of the game here in your GUI

            return new_game_state

        else:
            print("Invalid Move. Please try again.")
            # Return the current state if the move is invalid
            return self


# Example usage:
game_state = GobbletGameState()
game_state.initialize_game_state()
game_state.print_board()

# Assume a move has been made and a piece is being dragged to a new position
new_board_state = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0]]
game_state.update_board(new_board_state)

# Assume a piece is being dragged
game_state.set_dragged_piece("S", (2, 2))

# Print the updated board state and dragged piece information
game_state.print_board()
print("Dragged Piece:", game_state.dragged_piece)
print("Dragged Piece Position:", game_state.dragged_piece_position)

# Clear the dragged piece information
game_state.clear_dragged_piece()
print("Dragged Piece after clearing:", game_state.dragged_piece)
