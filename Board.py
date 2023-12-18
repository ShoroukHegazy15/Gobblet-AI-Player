# import copy


# class Piece:
    
#     """
#     Piece that contain stack and player and its size and 
    
#     """
#     def __init__(self,player,SizeOfPiece,stack):
#         self.player=player
#         self.SizeOfPiece=SizeOfPiece
#         self.stack=stack
        

# class Stack(object):

#     """
#     Stack of pieces that must push if there is no above piece and push if in the top of stack do not contain any larger piece
#     """
    
#     def __init__(self, pieces=None):
#         self.pieces = pieces or []

#     def __len__(self):
#         return len(self.pieces)

#     def __getitem__(self, key):
#         return self.pieces[key]

#     def __copy__(self):
#         return Stack(list(self.pieces))

#     def top(self):
#         return self.pieces[-1]

#     def push(self, piece):
#         if self.pieces and piece.size >= self.top().size:
#             raise ValueError()
#         self.pieces.append(piece)

#     def pop(self):
#         return self.pieces.pop()
    

# class OutSideStacks:

#     """
#     Each player has a number of stacks outside 
#     """

#     def __init__(self, stacks):
#         self.stacks = stacks

#     def __copy__(self):
#         stacks = list(copy(stack) for stack in self.stacks)
#         return OutSideStacks(stacks)

#     @property
#     def available(self):
#         available = []
#         for stack in self.stacks:
#             try:
#                 available.append(stack.top())
#             except IndexError:
#                 pass
#         return available




# class Board:
#     WHITE_PLAYER = "W"
#     BLACK = "B"
#     BOARD_SIZE = 4
#     PIECES_COUNT = 4
#     UNUSED_SETS = 3
#     W_UNUSED_ROW = BOARD_SIZE
#     B_UNUSED_COLUMN = BOARD_SIZE
#     PIECES= ["XS", "S", "M", "L"]
#     def __init__(self):
#         # Create a square board with "size" columns and rows,
#         # where each cell is a list.
#         self.cells = []
#         self.draw=False
#         self.FromPiecesCells=[]
#         self.ToPiecesCells=[]
#         #Create 2D array with stack on each column
#         for row_i in Board.BOARD_SIZE:
#             row = []
#             self.cells.append(row)
#             self.FromPiecesCells.append(row)
#             self.ToPiecesCells.append()
#             for col_i in Board.BOARD_SIZE:
#                 stack = Stack()
#                 row.append(stack)
        
#     def get_piece_on_top(self, x, y, player):
#         return self.cells[x][y].top()
    
#     def is_piece_placeable(self, x, y, piece):
#         if(self.cells[x][y].top().size>Board.get_piece_on_top().SizeOfPiece):
#             return True
#         else:
#             return False
#     def __getitem__(self, r,c):
#         return self.cells[r][c]
    
#     def generate_possible_moves(self,player):
#         result = []
#         availablePiecesArray=self.availablePieces(player)
#     #Return avaliable peices
#     def availablePieces(self,player):
#         available = []
#         for row in self.cells:
#             for cell in row:
#                 if cell and player==cell.top().player:
#                     available.append(cell.top())
#         return available   
    
#     def find(self, piece):
#         for key, cell in self:
#             try:
#                 if cell.top() is piece:
#                     return key
#             except IndexError:
#                 pass


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
        size_number = self.size_to_number(size)

        # Check if the stack is empty or the top piece is smaller
        if not current_stack or current_stack[-1][1] < size_number:
            piece = (self.current_player, size_number)
            self.board[row][col].append(piece)

            # Check if the size is present in the player's pieces before removing it
            player_pieces = getattr(self, f"{self.current_player}_pieces")
            if size_number in player_pieces:
                player_pieces.remove(size_number)
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
    
if __name__ == "__main__":
    # Create an instance of the Gobblet class
    game = Gobblet()

    # Print the initial state of the board
    print("Initial Board:")
    game.print_board()

    # Get and print valid moves for the current player
    valid_moves = game.get_valid_moves()
    print("\nValid Moves:")
    for move in valid_moves:
        print(move)

    # Example: Place a piece on the board
    game.place_piece(0, 0, "large")
    game.place_piece(0, 0, "extra-large")
    game.place_piece(0, 0, "extra-large")
    game.place_piece(0, 1, "extra-large")
    print("\nAfter placing an extra-large piece:")
    game.print_board()

    # Get and print valid moves for the current player after the placement
    valid_moves = game.get_valid_moves()
    print("\nValid Moves:")
    for move in valid_moves:
        print(move)
