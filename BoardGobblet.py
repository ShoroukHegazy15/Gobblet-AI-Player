import random


class Gobblet:
    def __init__(self):
        # Initialize the game board as a 4x4 grid
        self.board = [[[] for _ in range(4)] for _ in range(4)]

        # Initialize player pieces
        self.white_pieces = [4, 3, 2, 1] * 3  # "extra-large", "large", "medium", "small"
        self.black_pieces = [4, 3, 2, 1] * 3  # "extra-large", "large", "medium", "small"

        # Current player ('white' or 'black')
        self.current_player = 'white'

    def size_to_number(self, size):
        """
        Map piece sizes to numerical values.
        """
        size_mapping = {"small": 1, "medium": 2, "large": 3, "extra-large": 4}
        return size_mapping.get(size, 0)  # Default to 0 if size is not found

    def _is_within_board(self, row, col):
        """
        Check if the given coordinates are within the bounds of the board.
        """
        return 0 <= row < 4 and 0 <= col < 4

    def is_valid_move(self, start_row, start_col, end_row, end_col, size):
        """
        Check if a move is valid.
        """
        if not self._is_within_board(start_row, start_col) or not self._is_within_board(end_row, end_col):
            return False

        start_stack = self.board[start_row][start_col]
        end_stack = self.board[end_row][end_col]

        if not start_stack:
            return False

        # size = self.size_to_number(size)

        if start_stack[-1][1] != size:
            return False

        if end_stack and end_stack[-1][1] <= size:
            return False  # Move is invalid if there's a larger or equal-sized piece on the destination stack

        # Check if the starting stack is covered by a larger or equal-sized piece
        for i in range(len(start_stack) - 1):
            if start_stack[i][1] > size:
                return False  # Move is invalid if there's a larger piece covering the piece being moved
            elif start_stack[i][1] == size:
                return False  # Move is invalid if there's an equal-sized piece covering the piece being moved

        return True
    
    def is_valid_placement(self, row, col, size):
        # Check if placing a piece on the board is valid
        if not self._is_within_board(row, col):
            return False

        cell_stack = self.board[row][col]

        # If the cell is empty, it's a valid placement
        if not cell_stack:
            return True

        # Check if the top piece on the cell is smaller than the new piece
        top_piece_size = cell_stack[-1][1]
        return self.compare_piece_sizes(size, top_piece_size)
    
    
    def compare_piece_sizes(self, sizeInput, top_piece_size):
        if(sizeInput>top_piece_size):
            return True
        return False

    def get_valid_moves(self):
        """
        Get all valid moves for the current player.
        """
        valid_moves = []

        # Iterate through each cell on the board
        for row in range(4):
            for col in range(4):
                # Check if placing a piece from the off-the-board pile is valid
                for size in [1, 2, 3, 4]:
                    if size in getattr(self, f"{self.current_player}_pieces"):
                        if self.is_valid_placement(row, col, size):
                            valid_moves.append(("place", size, (row, col)))

                # Check if moving a piece on the board is valid
                start_stack = self.board[row][col]
                if start_stack and start_stack[-1][0] == self.current_player:
                    for end_row in range(4):
                        for end_col in range(4):
                            if self._is_within_board(end_row, end_col):
                                if self.is_valid_move(row, col, end_row, end_col, start_stack[-1][1]):
                                    valid_moves.append(("move",start_stack[-1][1],(row, col), (end_row, end_col)))

        return valid_moves

    def place_piece(self, row, col, size):
        """
        Place a piece on the board.
        """
        if not self._is_within_board(row, col):
            return False

        current_stack = self.board[row][col]
        # size_number = self.size_to_number(size)

        # Check if the stack is empty or the top piece is smaller
        if not current_stack or current_stack[-1][1] < size:
            piece = (self.current_player, size)
            self.board[row][col].append(piece)

            # Check if the size is present in the player's pieces before removing it
            player_pieces = getattr(self, f"{self.current_player}_pieces")
            if size in player_pieces:
                player_pieces.remove(size)
                return True
        else:
            return False


    def move_piece(self, start_row, start_col, end_row, end_col):
        """
        Move a piece on the board.
        """
        if not self._is_within_board(start_row, start_col) or not self._is_within_board(end_row, end_col):
            return False

        start_stack = self.board[start_row][start_col]
        end_stack = self.board[end_row][end_col]

        if not start_stack or not end_stack:
            return False

        size_number = start_stack[-1][1]

        if self.is_valid_move(start_row, start_col, end_row, end_col, size_number):
            piece = start_stack.pop()
            self.board[end_row][end_col].append(piece)
            return True
        else:
            return False

    def print_board(self):
        for row in self.board:
            print(row)
    def game_is_over(self):
        # Check for a win horizontally, vertically, or diagonally
        for row in range(4):
            if self._check_row_win(row):
                return True

        for col in range(4):
            if self._check_col_win(col):
                return True

        if self._check_diag_win():
            return True

        return False

    def _check_row_win(self, row):
        pieces = [self.board[row][col][0] for col in range(4) if self.board[row][col]]
        return len(pieces) == 4 and all(piece == pieces[0] for piece in pieces)


    def _check_col_win(self, col):
        pieces = [self.board[row][col][0] for row in range(4) if self.board[row][col]]
        return len(pieces) == 4 and all(piece == pieces[0] for piece in pieces)

    def _check_diag_win(self):
        pieces = [self.board[i][i][0] for i in range(4) if self.board[i][i]]
        return len(pieces) == 4 and (
            all(piece == pieces[0] for piece in pieces) or
            all(piece == pieces[0] for piece in reversed(pieces))
        )
import random


# Simple random AI player
def random_ai_player(game):
    valid_moves = game.get_valid_moves()
    if not valid_moves:
        return  # No valid moves

    move= random.choice(valid_moves)
    move_type=move[0]
    if move_type == "place":
        size,coordinates = move[1],move[2]
        row, col = coordinates
        game.place_piece(row,col,size)
    elif move_type == "move":
     # Extracting source and destination coordinates
        size,src_coordinates, dest_coordinates = move[1],move[2],move[3]
        src_row, src_col = src_coordinates
        dest_row, dest_col = dest_coordinates
        game.move_piece(src_row,src_col,dest_row,dest_col)

def play_game():
        # Create an instance of the Gobblet class
    game = Gobblet()

        # Main game loop
    while True:
        # Check if the game is over (you need to implement a game-over condition)
        if game.game_is_over():
            break

        # Print the current state of the board
        print("Current Board:")
        game.print_board()

        # Random AI player 1 makes a move
        random_ai_player(game)
        
        if(game.current_player=='white'):
            game.current_player='black'
        else:
            game.current_player='white'
        # Check if the game is over
        if game.game_is_over():
            break

        # Print the current state of the board
        print("\nCurrent Board:")
        game.print_board()

        # Random AI player 2 makes a move
        random_ai_player(game)

        # Print the final state of the board
        print("\nFinal Board:")
        game.print_board()

if __name__ == "__main__":
    # Play the game
    play_game()

# if __name__ == "__main__":
#     # Create an instance of the Gobblet class
#     game = Gobblet()

#     # Print the initial state of the board
#     print("Initial Board:")
#     game.print_board()

#     # Get and print valid moves for the current player
#     valid_moves = game.get_valid_moves()
#     print("\nValid Moves:")
#     for move in valid_moves:
#         print(move)

#     # Example: Place a piece on the board
#     game.place_piece(0, 0, "large")
#     game.place_piece(0, 0, "extra-large")
#     game.place_piece(0, 0, "extra-large")
#     game.place_piece(0, 1, "extra-large")
#     print("\nAfter placing an extra-large piece:")
#     game.print_board()

#     # Get and print valid moves for the current player after the placement
#     valid_moves = game.get_valid_moves()
#     print("\nValid Moves:")
#     for move in valid_moves:
#         print(move)
