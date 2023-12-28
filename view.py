import pygame
import os
from trialmove import Move
from trialmove import Board
import random               #random module for AI random moves 

class GobbletPiece(pygame.sprite.Sprite):
     def __init__(self, color, size, piece_id, position):
        super().__init__()
        self.color = color
        self.size = size
        self.piece_id = piece_id
        self.image = pygame.image.load(os.path.join(f"Assets/{color}{size}.png")).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        self.original_position = position  # Store the original position

class View():
    def __init__(self, game):
        self.game = game
        self.run_display = True
        self.bg = pygame.image.load(os.path.join("Assets/board.png")).convert()
        self.BACK_COLOR = (30, 54, 45)
        self.board_positions = [#8irt hna shwit arkam 386->385,724->725
            (215, 110), (385, 110), (555, 110), (725, 110),
            (215, 280), (385, 280), (555, 280), (725, 280),
            (215, 450), (385, 450), (555, 450), (725, 450),
            (215, 620), (385, 620), (555, 620), (725, 620),
        ]
        #self.pieces = {pos: [] for pos in self.board_centers}
        self.piece_positions = [(57, 107), (57, 274), (57, 447),
                                (898, 274), (898, 447), (898, 617)]
        #empty dictionary to associate f kol position 3l board w 3l sides fee anhy pieces?
        self.pieces = {pos: [] for pos in self.piece_positions + self.board_positions}
        self.piecesBoard = {pos: [] for pos in  self.board_positions}
        
    
        self.Gobblet_pieces = pygame.sprite.Group()  # Group to store all Gobblet pieces
        self.create_pieces()
        
        # Store the currently dragged piece and its offset
        self.dragged_piece = None
        self.drag_offset = (0, 0)
        self.board = Board(self.board_positions, self.piece_positions)
        self.hour, self.mins, self.sec = 00, 00, 00
        self.paused=False
        self.clock = pygame.time.Clock()

        if self.board.currentPlayer() == 1:  # Player 1's turn
            self.handle_drag_and_drop()  # Allow the human player to make a move
        elif self.board.currentPlayer() == 2:  # Player 2's turn
            self.random_ai_player()
        
        # player_one = True  # if a human is playing white, then this will be True, else False
        # player_two = False
        # human_turn = (self.board.current_player and player_one) or (not self.board.current_player and player_two)

        
    def create_pieces(self):
        sizes = ["XS", "S", "M", "L"]
        white_piece_count = {"L": 0, "M": 0, "S": 0, "XS": 0}
        black_piece_count = {"L": 0, "M": 0, "S": 0, "XS": 0}

        for color, positions, piece_count in [("white", self.piece_positions[:3], white_piece_count),
                                            ("black", self.piece_positions[3:], black_piece_count)]:

            for size in sizes:
                for piece_id, start_center in enumerate(positions):
                    # Check the size of the piece and update the count
                    if piece_count[size] < 3:
                        piece = GobbletPiece(color, size, piece_id, start_center)
                        self.Gobblet_pieces.add(piece)
                        self.pieces[start_center].append(piece)
                        piece_count[size] += 1
                        
    def update_pieces_dictionary(self, old_position, new_position):
        # Update the pieces dictionary based on the move
        if old_position in self.pieces and self.dragged_piece in self.pieces[old_position]:
            # Remove the dragged_piece from the list at old_position
            self.pieces[old_position].remove(self.dragged_piece)
        if old_position in self.piecesBoard:
            # Remove the dragged_piece from the list at old_position
            self.piecesBoard[old_position].remove(self.dragged_piece)
        if new_position in self.pieces :
            # Append the dragged_piece to the list at new_position
            self.pieces[new_position].append(self.dragged_piece)
            self.piecesBoard[new_position].append(self.dragged_piece)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.BACK_COLOR)
            self.game.display.blit(self.bg, (0, 0))
            # Draw Gobblet pieces
            self.Gobblet_pieces.draw(self.game.display)
            self.handle_drag_and_drop()#end of program 
            # self.timer()
            self.blit_screen()
    
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.pause_menu
            self.paused= not self.paused
            self.run_display = False

    def handle_drag_and_drop(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # Check for piece dragging in reverse order
        for piece in reversed(self.Gobblet_pieces.sprites()):
            if piece.rect.collidepoint(mouse_x, mouse_y) and mouse_pressed and not self.dragged_piece:
                # Only allow dragging if the piece's position is in piece_positions
                if piece.rect.center in self.piece_positions:
                    # Only allow dragging white pieces during human turn
                    if self.board.currentPlayer() == 1 and piece.color == "white" and not self.has_black_piece_on_top(piece):
                        self.dragged_piece = piece
                        self.drag_offset = (piece.rect.centerx - mouse_x, piece.rect.centery - mouse_y)
                        break
                elif piece.rect.center in self.board_positions:
                    if self.board.currentPlayer() == 1 and piece.color == "white" and not self.has_black_piece_on_top(piece):
                        self.dragged_piece = piece
                        self.drag_offset = (piece.rect.centerx - mouse_x, piece.rect.centery - mouse_y)
                        break

        # If a piece is being dragged, update its position
        if self.dragged_piece and mouse_pressed:
            self.dragged_piece.rect.center = (mouse_x + self.drag_offset[0], mouse_y + self.drag_offset[1])

        # If the mouse button is released and a piece is being dragged
        elif self.dragged_piece and not mouse_pressed:
            self.handle_dropped_piece()

    def has_black_piece_on_top(self, piece):
        position = piece.rect.center
        if position in self.pieces and len(self.pieces[position]) > 1:
            # Check if there is a black piece on top of the dragged white piece
            top_piece = self.pieces[position][-1]
            if top_piece.color == "black":
                return True
        return False 
        
    def handle_dropped_piece(self): #this function must take arguments of which play random ai or hard ai or what
        old_position = self.dragged_piece.original_position
        new_position = None    # Initialize new_position to None
        # Check if the piece is close to a board position, then create a move
        for board_position in self.board_positions:
            if self.dragged_piece and self.is_close_to_position(self.dragged_piece.rect.center, board_position) :
                new_position = board_position
                move_instance = Move(old_position, new_position, self.dragged_piece.size,)
                new_board = self.board.make_move(move_instance,1)
                if new_board is not None:
                    # If the move was successful, update the current board
                    self.board = new_board
                    # Update the original_position when the piece is moved to the board
                    if new_position in self.board_positions:
                        self.dragged_piece.rect.center = new_position
                        self.dragged_piece.original_position = new_position  # Update the original_position here

                        self.update_pieces_dictionary(old_position, new_position)
                        # Reorder the sprites to ensure the dragged piece is drawn last; on top y3ny
                        self.Gobblet_pieces.remove(self.dragged_piece)  
                        self.Gobblet_pieces.add(self.dragged_piece)   #bn7otaha on top of stack 3l board
                        if(self.board.current_player==1 and self.game_is_over()):
                            print("White winSSSSSSSSSSSSSSSSSSSSSSSSSs")
                            return 1
                        elif(self.board.current_player==2 and self.game_is_over()):
                            print("Black winsSSSSSSSSSSS")
                            return 2
                            
                        self.board.switchPlayer()
                        self.random_ai_player() 
                        self.board.switchPlayer()
                else:
                    # If the move is invalid, revert the position of the dragged piece
                    self.dragged_piece.rect.center = old_position
                    print("Move is invalid, reverting position.")
                    print("this is still player: ",self.board.current_player, " turn")
                    
                break
        # If new_position is None, the piece was not dropped near any board position
        if new_position is None:
        # Snap the piece back to its original position
            self.dragged_piece.rect.center = old_position
            print("this is still player: ",self.board.current_player, " turn")
        self.dragged_piece = None
        
        # Print the contents of the pieces dictionary after each move
        print("\n********Contents of the pieces dictionary:**********")
        # for pos, pieces in self.pieces.items():
        #     print(f"Position {pos} has pieces:")
        #     # x,y=pos
        #     # print(x,y)
        #     # print("Top Piece: ",self.pieces.items()[pos][-1])
        #     i=0
        #     if(pos in self.board_positions):
        #         for piece in pieces:
        #             print(i)
        #             i+=1
        #             print(f"  - Color: {piece.color}, Size: {piece.size}, Piece ID: {piece.piece_id}")
        #     # for piece in pieces:
        #     #     print(f"  - Color: {piece.color}, Size: {piece.size}, Piece ID: {piece.piece_id}")
        board= self.getSimplifiedBoard()
        for row in board:
            print(row)

            
    def is_close_to_position(self, pos1, pos2, threshold=100):
        # """Check if two positions are close within a given threshold."""
        return abs(pos1[0] - pos2[0]) < threshold and abs(pos1[1] - pos2[1]) < threshold

    def get_piece_at_position(self, position):
        """Retrieve the top piece at a given position."""
        if position in self.pieces and self.pieces[position]:
            return self.pieces[position][-1]  # Get the top piece at the position
        else:
            print("\nana el 3mla moshkela\n")
            return None  # No piece at the position                
    
    def random_ai_player(self):
        # Simulate the computer making a random move
        if self.board.currentPlayer() == 2 :  # Player 1 is human, Player 2 is the computer
            print("this is player: ", self.board.current_player, " turn")

            valid_moves = self.get_valid_moves_for_pieces("black")   #can be called b2a anywhere with the color parameter
            
             #computer yl3b bel black bsss
            #valid_moves = self.get_valid_moves_for_black_pieces()
             
            if valid_moves:
                move = random.choice(valid_moves)
                old_position = move.start_position
                new_position = move.end_position
                
                # Update the position of the chosen piece as if it's being dragged by the computer
                chosen_piece = self.get_piece_at_position(old_position)
                if chosen_piece:
                    chosen_piece.rect.center = new_position
                    chosen_piece.original_position = new_position
                
                new_board = self.board.make_move(move, player=2)  # Pass the computer player as an argument
                
                # Remove the piece from the list at old_position
                if old_position in self.pieces and self.pieces[old_position]:  # Check if the list is not empty
                    moved_piece = self.pieces[old_position].pop()
                    self.pieces[new_position].append(moved_piece)
                    
                    # Reorder the sprites to ensure the dragged piece is drawn last (on top)
                    self.Gobblet_pieces.remove(moved_piece)
                    self.Gobblet_pieces.add(moved_piece)
                if old_position in self.piecesBoard and self.pieces[old_position]:
                    self.piecesBoard[old_position].pop()
                    self.piecesBoard[new_position].append(moved_piece)
                    
                for position, pieces in self.board.board_state.items():
                    print(f"Position {position} has pieces: {pieces}")
                    print("\n")            
            else:
                print("\nno valid moves for BLACk!!!\n")
                
    def get_valid_moves_for_pieces(self,Color):
        valid_moves = []

        # Check if there is at least one black piece on the board
        piece_on_board = any(self.pieces[pos] and self.pieces[pos][-1].color == Color for pos in self.board_positions)
        if(Color=="black"):
            # Consider black pieces on the side for the first move
            if not piece_on_board:
                for start_position in self.piece_positions[3:]:
                    if self.pieces[start_position]:  # Check if the list is not empty
                        for end_position in self.board_positions:
                            piece_size = self.get_piece_size_at_position(start_position)
                            if piece_size is not None:  # Check if the piece size is not None
                                move = Move(start_position, end_position, piece_size)
                                if self.board.is_valid_move(move):
                                    valid_moves.append(move)
                                else:
                                    print("\nexternal move is invalid!!!!\n")
            else:
                # If there is at least one black piece on the board, consider internal moves as well
                for start_position in self.piece_positions[3:]:
                    if self.pieces[start_position]:  # Check if the list is not empty
                        for end_position in self.board_positions:
                            piece_size = self.get_piece_size_at_position(start_position)
                            if piece_size is not None:  # Check if the piece size is not None
                                move = Move(start_position, end_position, piece_size)
                                if self.board.is_valid_move(move):
                                    valid_moves.append(move)
                                    
                for start_position in self.board_positions:
                    if self.pieces[start_position] and self.pieces[start_position][-1].color == Color:  # Check if the list is not empty and the piece is black
                        for end_position in self.board_positions:
                            piece_size = self.get_piece_size_at_position(start_position)
                            if piece_size is not None:  # Check if the piece size is not None
                                move = Move(start_position, end_position, piece_size)
                                if self.board.is_valid_move(move):
                                    valid_moves.append(move)
                                else:
                                    print("\ninternal move is invalid!!!!\n")
        else:
            # Consider white pieces on the side for the first move
            if not piece_on_board:
                for start_position in self.piece_positions[:3]:
                    if self.pieces[start_position]:  # Check if the list is not empty
                        for end_position in self.board_positions:
                            piece_size = self.get_piece_size_at_position(start_position)
                            if piece_size is not None:  # Check if the piece size is not None
                                move = Move(start_position, end_position, piece_size)
                                if self.board.is_valid_move(move):
                                    valid_moves.append(move)
                                else:
                                    print("\nexternal move is invalid!!!!\n")
            else:
                # If there is at least one black piece on the board, consider internal moves as well
                for start_position in self.piece_positions[:3]:
                    if self.pieces[start_position]:  # Check if the list is not empty
                        for end_position in self.board_positions:
                            piece_size = self.get_piece_size_at_position(start_position)
                            if piece_size is not None:  # Check if the piece size is not None
                                move = Move(start_position, end_position, piece_size)
                                if self.board.is_valid_move(move):
                                    valid_moves.append(move)
                                    
                for start_position in self.board_positions:
                    if self.pieces[start_position] and self.pieces[start_position][-1].color == Color:  # Check if the list is not empty and the piece is black
                        for end_position in self.board_positions:
                            piece_size = self.get_piece_size_at_position(start_position)
                            if piece_size is not None:  # Check if the piece size is not None
                                move = Move(start_position, end_position, piece_size)
                                if self.board.is_valid_move(move):
                                    valid_moves.append(move)
                                else:
                                    print("\ninternal move is invalid!!!!\n")
    
        return valid_moves
         
    def get_valid_moves_for_black_pieces(self):
        valid_moves = []

        # Check if there is at least one black piece on the board
        black_piece_on_board = any(self.pieces[pos] and self.pieces[pos][-1].color == "black" for pos in self.board_positions)

        # Consider black pieces on the side for the first move
        if not black_piece_on_board:
            print("\nif\n")
            for start_position in self.piece_positions[3:]:
                if self.pieces[start_position]:  # Check if the list is not empty
                    for end_position in self.board_positions:
                        piece_size = self.get_piece_size_at_position(start_position)
                        if piece_size is not None:  # Check if the piece size is not None
                            move = Move(start_position, end_position, piece_size,)
                            if self.board.is_valid_move(move):
                                valid_moves.append(move)
                            else:
                                print("\nexternal move is invalid!!!!\n")
        else:
            print("\nelse\n")
            # If there is at least one black piece on the board, consider internal moves as well
            for start_position in self.piece_positions[3:]:
                if self.pieces[start_position]:  # Check if the list is not empty
                    for end_position in self.board_positions:
                        piece_size = self.get_piece_size_at_position(start_position)
                        if piece_size is not None:  # Check if the piece size is not None
                            move = Move(start_position, end_position, piece_size)
                            if self.board.is_valid_move(move):
                                valid_moves.append(move)
                                
            for start_position in self.board_positions:
                if self.pieces[start_position] and self.pieces[start_position][-1].color == "black":  # Check if the list is not empty and the piece is black
                    for end_position in self.board_positions:
                        piece_size = self.get_piece_size_at_position(start_position)
                        if piece_size is not None:  # Check if the piece size is not None
                            move = Move(start_position, end_position, piece_size)
                            if self.board.is_valid_move(move):
                                valid_moves.append(move)
                            else:
                                print("\ninternal move is invalid!!!!\n")

        return valid_moves
    

    def game_is_over(self):
        board=self.getSimplifiedBoard()
        # Check for a win horizontally, vertically, or diagonally
        for row in range(4):
            if self._check_row_win(board,row):
                self.game.curr_menu=self.game.win_screen   #win screen appears
                # self.game.curr_menu=self.game.lose_screen   #lose screen appears
                self.run_display = False
                return True

        for col in range(4):
            if self._check_col_win(board,col):
                self.game.curr_menu=self.game.win_screen    #win screen appears
                # self.game.curr_menu=self.game.lose_screen   #lose screen appears
                self.run_display = False
                return True

        if self._check_diag_win(board):
            self.game.curr_menu=self.game.win_screen      #win screen appears
            # self.game.curr_menu=self.game.lose_screen   #lose screen appears
            self.run_display = False
            return True

        return False

    def _check_row_win(self,board, row):
        pieces = [board[row][col][-1] for col in range(4) if board[row][col]]
        counterOfTruth=0
        for piece in pieces:
            if(piece[0]==pieces[0][0]):
                counterOfTruth+=1
            else:
                return False
        if(counterOfTruth==4):
            return True
        # return len(pieces) == 4 and all(piece == pieces[0] for piece in pieces)


    def _check_col_win(self,board, col):
        pieces = [board[row][col][-1] for row in range(4) if board[row][col] ]
        counterOfTruth=0
        for piece in pieces:
            if(piece[0]==pieces[0][0]):
                counterOfTruth+=1
            else:
                return False
        if(counterOfTruth==4):
            return True

    def _check_diag_win(self,board):
        pieces = [board[i][i][-1] for i in range(4) if board[i][i]]
        counterOfTruth=0
        for piece in pieces:
            if(piece[0]==pieces[0][0]):
                counterOfTruth+=1
            else:
                return False
        if(counterOfTruth==4):
            return True
        counterOfTruth=0
        for piece in reversed(pieces):
            if(piece[0]==pieces[0][0]):
                counterOfTruth+=1
            else:
                return False
        if(counterOfTruth==4):
            return True
        
    #simple 2d array with only 0-4 and 2d array
    def getSimplifiedBoard(self):
        board = [[[] for _ in range(4)] for _ in range(4)]
        i=0
        j=0
        for pos, pieces in self.pieces.items():
            if(pos in self.board_positions):
                for piece in pieces:
                    if(piece.color=="white"):
                        board[j][i].append(("white",piece.size))
                    elif(piece.color=="black"):
                        board[j][i].append(("black",piece.size))
                i+=1
            if(i>3):
                i=0
                j+=1
        return board
        
    def get_piece_size_at_position(self, position):
        # method to get the piece size at a given position
        if position in self.pieces and self.pieces[position]:
            return self.pieces[position][-1].size  # Get the size of the top piece
        else:
            print("\nana el moshkela el tanya\n")
            return None  # No piece at the position   
        

     
    def draw_timer(self,hr,m,s,size,x,y):
        font=pygame.font.Font(self.game.font_name,size)
        text_serface =font.render("{}:{}:{}".format(hr,m,s),True,(250,250,250))
        text_rect=text_serface.get_rect()
        text_rect.center =(x,y) #make the center of the rectag\ngle the given x and y
        self.game.display.blit(text_serface,text_rect)

    #def timer(self):
    #    if not self.paused:
     #       self.sec += 1
      #      time.sleep(1)
    
    def timer(self):
        #clock=pygame.time.Clock()
        self.clock.tick(1)
        if not self.paused:
            self.sec += 1    
        self.show_timer()

    def show_timer(self):
        if self.sec == 60:
            self.sec=0
            self.mins += 1
        if self.mins ==  60:
            self.mins=0
            self.hour += 1
        if self.sec<10 and self.mins<10 and self.hour<10:
            str_sec= "0"+ str(self.sec)
            str_mins= "0"+ str(self.mins)
            str_hr= "0"+ str(self.hour)
        elif self.mins<10 and self.hour<10:
            str_sec =str(self.sec)
            str_mins= "0" +  str(self.mins)
            str_hr= "0"+ str(self.hour)
        elif self.hour<10:
            str_sec =str(self.sec)
            str_mins= str(self.mins)
            str_hr= "0"+ str(self.hour)
        else :
            str_sec =str(self.sec)
            str_mins= str(self.mins)
            str_hr= str(self.hour)
        self.draw_timer(str_hr,str_mins,str_sec,24,877,40)


  
