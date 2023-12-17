class Move:
    def __init__(self, start_position, end_position,piece_size,):
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
        #self.dragged_piece=dragged_piece
        self.move_track = []
        self.current_player = 1
        
       
       # self.board_state = {}
        self.board_state = {position: [] for position in board_positions}
        #def set_dragged_piece(self, dragged_piece):
         #   self.dragged_piece = dragged_piece
                #key(board_positions)
                #value (lists of stack of pieces on each tile in that position)
                
        #self.board_state = [[0] * (self.BOARD_SIZE + 1) for _ in range(self.BOARD_SIZE + 1)]

    #def make_move(self, move):
        #new_board = Board(self.board_positions, self.piece_positions)
        #if self.isValidMove(move):
            
        # Check if it's an internal move or an external move
        #return new_board    

    def make_move(self, move):
        if self.is_valid_move(move):
            new_board = self.make_internal_move(move) if move.start_position in self.board_positions else self.make_external_move(move)
            return new_board
        else:
            print("Invalid move!")
            return None  # Return the current board if the move is invalid

    def is_valid_move(self, move):
        print("Checking valid move...")
        start_position, end_position, piece_size = move.start_position, move.end_position, move.piece_size

        # Check if the end position is on the board
        if end_position not in self.board_positions:
            return False

        # Check if the end position is empty or the piece being placed is larger than the piece on top
        if self.board_state[end_position]:
            top_piece_size = self.board_state[end_position][-1]   # extract top piece size on the end position
            print("abl check el size")
            if piece_size >= top_piece_size:
                print("Invalid move: Piece is larger or equal to the piece on top.")
                return False
        return True

    def make_internal_move(self, move):
        start_position, end_position, piece_size = move.start_position, move.end_position, move.piece_size

        # Update the board state based on the move
        print(f"Making internal move: {move}")

        # Remove the piece from the start position  el heya wa7da mn el board_positions
        self.board_state[start_position].pop()  

        # Add the piece to the end position
        self.board_state[end_position].append(piece_size)

        return self  # Return the new board state after the internal move

    def make_external_move(self, move):
        start_position, end_position, piece_size = move.start_position, move.end_position, move.piece_size
        # Place a piece from the stack onto the board
        print(f"Making external move: {move}")
        
        # Remove the piece from the start position  el heya wa7da mn el piece_positions
        #self.board_state[start_position].pop()  
        
        # Add the piece to the end position
        self.board_state[end_position].append(piece_size)

        return self

    
    def switchPlayer(self):
        # Helping method to switch the current player
        self.current_player = not self.current_player

    
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
            switchPlayer()

            print(f"undo move Done")


            
        else :
            print(f"Invalid undo move")




