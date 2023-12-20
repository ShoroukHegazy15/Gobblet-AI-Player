import pygame
import os
from trialmove import Move
from trialmove import Board
import random        #random module for AI random moves 

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
        self.board_positions = [
            (215, 110), (386, 110), (555, 110), (724, 110),
            (215, 280), (386, 280), (555, 280), (724, 280),
            (215, 450), (386, 450), (555, 450), (724, 450),
            (215, 620), (386, 620), (555, 620), (724, 620),
        ]
        #self.pieces = {pos: [] for pos in self.board_centers}
        self.piece_positions = [(57, 107), (57, 274), (57, 447),
                                (898, 274), (898, 447), (898, 617)]
        #empty dictionary to associate f kol position 3l board w 3l sides fee anhy pieces?
        self.pieces = {pos: [] for pos in self.piece_positions + self.board_positions}
       
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

        if new_position in self.pieces:
            # Append the dragged_piece to the list at new_position
            self.pieces[new_position].append(self.dragged_piece)

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
            self.handle_drag_and_drop()
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
                    if self.board.currentPlayer() == 1 and piece.color == "white":
                        self.dragged_piece = piece
                        self.drag_offset = (piece.rect.centerx - mouse_x, piece.rect.centery - mouse_y)
                        break
                elif piece.rect.center in self.board_positions:
                    if self.board.currentPlayer() == 1 and piece.color == "white":
                        self.dragged_piece = piece
                        self.drag_offset = (piece.rect.centerx - mouse_x, piece.rect.centery - mouse_y)
                        break

        # If a piece is being dragged, update its position
        if self.dragged_piece and mouse_pressed:
            self.dragged_piece.rect.center = (mouse_x + self.drag_offset[0], mouse_y + self.drag_offset[1])

        # If the mouse button is released and a piece is being dragged
        elif self.dragged_piece and not mouse_pressed:
            self.handle_dropped_piece()

    def handle_dropped_piece(self):
        """ print("now im printing the ccontents of pieces dictionary:")
        for pos, pieces in self.pieces.items():
            print(f"Position {pos} has pieces: {pieces}") """
        old_position = self.dragged_piece.original_position
        new_position = None    # Initialize new_position to None
        # Check if the piece is close to a board position, then create a move
        for board_position in self.board_positions:
            if self.dragged_piece and self.is_close_to_position(self.dragged_piece.rect.center, board_position):
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
                        # Reorder the sprites to ensure the dragged piece is drawn last
                        self.Gobblet_pieces.remove(self.dragged_piece)
                        self.Gobblet_pieces.add(self.dragged_piece)
                        
                        self.board.switchPlayer()
                        self.random_ai_player() 
                        self.board.switchPlayer()

                    """ else:
                        # If the new position is not in board_positions, keep the piece at its old position
                        self.dragged_piece.rect.center = old_position
 """
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
        for pos, pieces in self.pieces.items():
            print(f"Position {pos} has pieces:")
            for piece in pieces:
                print(f"  - Color: {piece.color}, Size: {piece.size}, Piece ID: {piece.piece_id}")
            
    def is_close_to_position(self, pos1, pos2, threshold=100):
        # """Check if two positions are close within a given threshold."""
        return abs(pos1[0] - pos2[0]) < threshold and abs(pos1[1] - pos2[1]) < threshold

    

    def get_piece_at_position(self, position):
        """Retrieve the top piece at a given position."""
        if position in self.pieces and self.pieces[position]:
            return self.pieces[position][-1]  # Get the top piece at the position
        else:
            return None  # No piece at the position
 

    def random_ai_player(self):
    # Simulate the computer making a random move
        if self.board.currentPlayer() == 2:  # Player 1 is human, Player 2 is the computer
            print("This is player: ", self.board.current_player, " turn")

            # Computer plays with black pieces only
            valid_moves = self.get_valid_moves_for_black_pieces()
            if valid_moves:
                move = random.choice(valid_moves)
                old_position = move.start_position
                new_position = move.end_position

                # Update the position of the chosen piece as if it's being dragged by the computer
                chosen_piece = self.get_piece_at_position(old_position)
                if chosen_piece:
                    chosen_piece.rect.center = new_position
                    chosen_piece.original_position = new_position
                # Make the move on the board
                new_board = self.board.make_move(move, player=2)
                if new_board is not None:
                    # If the move was successful, update the current board
                    self.board = new_board
                    self.update_pieces_dictionary(old_position, new_position)
                    self.board.switchPlayer()
                # Continue the game loop by allowing the human player to make a move
            self.handle_drag_and_drop()
        # Continue with the rest of your method...
        self.board.switchPlayer()


    # New method to get valid moves for black pieces only
    def get_valid_moves_for_black_pieces(self):
        valid_moves = []
        for start_position in self.piece_positions[3:] or start_position in self.board_positions:  # Consider only black pieces
            for end_position in self.board_positions:
                piece_size = self.get_piece_size_at_position(start_position)
                move = Move(start_position, end_position, piece_size)
                if self.board.is_valid_move(move):
                    valid_moves.append(move)
        return valid_moves

    def get_piece_size_at_position(self, position):
        # Helper method to get the piece size at a given position
        if position in self.pieces and self.pieces[position]:
            return self.pieces[position][-1].size  # Get the size of the top piece
        else:
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


  
