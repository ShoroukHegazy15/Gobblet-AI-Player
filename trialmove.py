class Move:
    def __init__(self, start_position, end_position, piece_size):
        self.start_position = start_position
        self.end_position = end_position
        self.piece_size = piece_size

class Board:
    def __init__(self, board_positions, piece_positions):
        self.board_positions = board_positions
        self.piece_positions = piece_positions
        self.board_state = {}
    
    def make_move(self, move):
        # Check if it's an internal move or an external move
        if move.start_position in self.board_positions:
            self.make_internal_move(move)
        elif move.start_position in self.piece_positions[:3] or move.start_position in self.piece_positions[3:] :
            self.make_external_move(move)
        else:
            print(f"invalid move")

    def make_internal_move(self, move):
        # Update the board state based on the move
        print(f"Making internal move: {move}")

    def make_external_move(self, move):
        # Place a piece from the stack onto the board
        print(f"Making external move: {move}")
