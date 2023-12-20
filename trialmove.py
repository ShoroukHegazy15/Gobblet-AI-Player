class Move:
    def __init__(self, start_position, end_position,piece_size,):
        self.start_position = start_position
        self.end_position = end_position
        self.piece_size = piece_size

class Board:
    def __init__(self, board_positions, piece_positions):
        self.board_positions = board_positions
        self.piece_positions = piece_positions
        self.move_track = []
        self.current_player = 1
        self.board_state = {position: [] for position in board_positions}
        #key(board_positions)
        #value (lists of stack of pieces on each tile in that position)
        #initial value for each key (position) is an empty list [], y3ny there are no pieces on that position initially.
        
    def make_move(self, move,player):
        if player == 1:  # Human player
            if self.is_valid_move(move):
                new_board = self.make_internal_move(move) if move.start_position in self.board_positions else self.make_external_move(move)
                """ for position, pieces in self.board_state.items():
                    print(f"Position {position} has pieces: {pieces}") """
                return new_board
            else:
                print("Invalid move!")
                return None  # Return the current board if the move is invalid
            
        elif player == 2:  # Computer player
            #if self.is_valid_move(move):
            new_board = self.make_internal_move(move) if move.start_position in self.board_positions else self.make_external_move(move)
            for position, pieces in self.board_state.items():
                print(f"Position {position} has pieces: {pieces}")
            return new_board
            
    def is_valid_move(self, move):
        #print("Checking valid move...")
        start_position, end_position, piece_size = move.start_position, move.end_position, move.piece_size
        # Check if the end position is on the board
        if end_position not in self.board_positions:
            return False
        # Check if the end position is empty or the piece being placed is larger than the piece on top
        if self.board_state[end_position]:
            top_piece_size = self.board_state[end_position][-1]   # extract top piece size on the end position
            if piece_size >= top_piece_size:
                #print("Invalid move: Piece is larger or equal to the piece on top.")
                return False
        return True

    def make_internal_move(self, move):
        start_position, end_position, piece_size = move.start_position, move.end_position, move.piece_size
        # Update the board state based on the move
        #print(f"Making internal move: {move}")
        # Remove the piece from the start position  el heya wa7da mn el board_positions
        self.board_state[start_position].pop()  
        # Add the piece to the end position
        self.board_state[end_position].append(piece_size)
        return self  #Return the new board state after the internal move

    def make_external_move(self, move):
        start_position, end_position, piece_size = move.start_position, move.end_position, move.piece_size
        # Add the piece to the end position
        self.board_state[end_position].append(piece_size)
        return self
    
    def switchPlayer(self):
        self.current_player = 3 - self.current_player  # Toggle between 1 and 2
        #print("player: ",self.current_player)

    def currentPlayer(self):
        # Returns the player whose turn it is to play on the current board
        return self.current_player

    # undo a move
    def undo_moves(self):
        # check if it is not the first move
        if len(self.move_track) != 0:
            # Retrieves the last move made 
            move = self.move_track.pop()
            # Update the board state 
            # Switch players
            self.switchPlayer()
            print(f"undo move Done")

            
        else :
            print(f"Invalid undo move")



