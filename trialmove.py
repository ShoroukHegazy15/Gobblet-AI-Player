class Move:
    def __init__(self, start_position, end_position,piece_size,):
        self.start_position = start_position
        self.end_position = end_position
        self.piece_size = piece_size

class Board:
    def __init__(self, board_positions, piece_positions):
        self.board_positions = board_positions
        self.piece_positions = piece_positions
        #self.dragged_piece=dragged_piece
       
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

        """ 
    def make_move_internal(self, from_x, from_y, to_x, to_y, piece, player):
        if piece != self.get_movable_piece(from_x, from_y, player):
            return False
        if not self.is_piece_placeable(to_x, to_y, piece, player):
            return False

        # remove from old tile
        self.tiles[from_x][from_y] &= ~(piece << player)

        # put to a new tile
        self.tiles[to_x][to_y] |= (piece << player)

        # add the new board to the history
        count = 1
        simple_hash = self.calculate_simple_hash()
        if simple_hash in self.positions_counter:
            count += self.positions_counter[simple_hash]
        self.positions_counter[simple_hash] = count

        # draw check
        if count >= 3:
            self.draw = True

        return True
    
    def get_placeable_pieces(self, x, y):
        result = 0
        for i in range(self.PIECES_COUNT - 1, -1, -1):
            if not self.is_piece_on(x, y, self.PIECES[i]):
                result |= self.PIECES[i]
            else:
                break
        return result

    def is_piece_placeable(self, x, y, piece, player):
        highest_w_piece = self.get_piece_on_top(x, y, self.WHITE_PLAYER)
        highest_b_piece = self.get_piece_on_top(x, y, self.BLACK)

        return piece > highest_w_piece and piece > highest_b_piece

    def get_piece_on_top(self, x, y, player):
        mask = self.WHITE_MASK if player == self.WHITE_PLAYER else self.BLACK_MASK
        player_tile = (self.tiles[x][y] & mask) >> player
        if player_tile > 0:
            piece_index = int((player_tile & -player_tile).bit_length()) - 1
            return 1 << piece_index
        else:
            return 0
    
        
    def get_movable_piece(self, x, y, player):
        highest_w_piece = self.get_piece_on_top(x, y, self.WHITE_PLAYER)
        highest_b_piece = self.get_piece_on_top(x, y, self.BLACK)

        if player == self.WHITE_PLAYER:
            return highest_w_piece if highest_w_piece > highest_b_piece else 0
        else:
            return highest_b_piece if highest_b_piece > highest_w_piece else 0

    def is_piece_on(self, x, y, piece, player):
        return (self.tiles[x][y] & (piece << player)) > 0

    def is_piece_on(self, x, y, piece):
        return self.is_piece_on(x, y, piece, self.WHITE_PLAYER) or self.is_piece_on(x, y, piece, self.BLACK)
    
        
 """