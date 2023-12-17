class Move:
    def __init__(self, start_position, end_position, piece_size):
        self.start_position = start_position
        self.end_position = end_position
        self.piece_size = piece_size
        


    def get_startPosition(self):
        return self.start_position
    
    def set_startPosition(self, start_position):
        self.start_position = start_position

    def get_endPosition(self):
        return self.end_position
    
    def set_endPosition(self, end_position):
        self.end_position = end_position



class Board:
    def __init__(self, board_positions, piece_positions):
        self.board_positions = board_positions
        self.piece_positions = piece_positions
        self.board_state = {}
        self.move_track = []
        self.current_player = 1

    
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


    # undo a move
    def undo_moves(self):
        # check if it is not the first move
        if len(self.move_track) != 0:
            # Retrieves the last move made 
            move = self.move_track.pop()
            # Update the board state 

            # Switch players
            self.current_player = not self.current_player 

            print(f"undo move Done")


            
        else :
            print(f"Invalid undo move")

