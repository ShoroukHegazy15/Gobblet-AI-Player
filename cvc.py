import copy
import pygame
import os
from trialmove import Move
from trialmove import Board
import random              
import time
#random module for AI random moves 

class GobbletPiece(pygame.sprite.Sprite):
    def __init__(self, color, size, piece_id, position):
        super().__init__()
        self.color = color
        self.size = size
        self.piece_id = piece_id
        self.image = pygame.image.load(os.path.join(f"Assets/{color}{size}.png")).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        self.original_position = position  # Store the original position

class ViewCVC():
    def __init__(self, game):
        self.game = game
        # self.AlgosInstance=Algos()
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

        #timer
        self.game.paused_flag=0
        self.fixed_start_time=0
        self.elapsed_seconds = 0
        self.mins=0

    def startGame(self,levelP1,levelP2):
        self.display_menu(levelP1,levelP2)
    


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

    def display_menu(self,levelP1,levelP2):
        self.run_display = True
        self.clock = pygame.time.Clock()
        if self.game.paused_flag == 0:
            self.start_time = pygame.time.get_ticks()
            self.fixed_start_time=self.start_time
        else:
            self.start_time = self.fixed_start_time
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.BACK_COLOR)
            self.game.display.blit(self.bg, (0, 0))
            # Draw Gobblet pieces
            self.Gobblet_pieces.draw(self.game.display)
            time.sleep(2)
            if(levelP1=="Easy"):
                print("EASY")
                self.random_ai_player()
            elif(levelP1=="Medium"):
                print("MEDIUM")
                self.MediumLevelAI()
            elif(levelP1=="Hard"):
                print("HARD")
                self.HardAI()
            time.sleep(2)
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.BACK_COLOR)
            self.game.display.blit(self.bg, (0, 0))
            # Draw Gobblet pieces
            self.Gobblet_pieces.draw(self.game.display)
            time.sleep(1)
            if(levelP2=="Easy"):
                self.random_ai_player()
            elif(levelP2=="Medium"):
                self.MediumLevelAI()
            elif(levelP2=="Hard"):
                self.HardAI()
            time.sleep(2)
            
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.BACK_COLOR)
            self.game.display.blit(self.bg, (0, 0))
            # Draw Gobblet pieces
            self.Gobblet_pieces.draw(self.game.display)
            # time.sleep(2)
            self.game.paused=False
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.pause_menu
            self.game.paused_flag =1
            self.run_display = False
        
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

        
        if(self.game_is_over()):
            time.sleep(2)
            Bool,winner=self.game_is_over()
            self.game.curr_menu=self.game.win_screen
            self.game.curr_menu.setMsg(winner+" Wins")
            self.run_display=False
        # Simulate the computer  making a random move
        if self.board.currentPlayer() == 2:  # Player 1 is human, Player 2 is the computer
            print("this is player: ", self.board.current_player, " turn")

            valid_moves = self.get_valid_moves_for_pieces("black")   #can be called b2a anywhere with the color parameter
            
            #computer yl3b bel black bsss

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
                    if(len(self.piecesBoard[old_position])==0):
                        self.piecesBoard[old_position].clear()
                    else:
                        self.piecesBoard[old_position].pop()
                    self.piecesBoard[new_position].append(moved_piece)
                
                for position, pieces in self.board.board_state.items():
                    print(f"Position {position} has pieces: {pieces}")
                    print("\n")            
            else:
                print("\nno valid moves for BLACk!!!\n")
        elif  self.board.currentPlayer()==1:
            print("this is player: ", self.board.current_player, " turn")

            valid_moves = self.get_valid_moves_for_pieces("white")   #can be called b2a anywhere with the color parameter
            
            #Computer momken yl3b white w black
            
            if valid_moves:
                move = random.choice(valid_moves)
                old_position = move.start_position
                new_position = move.end_position
                
                # Update the position of the chosen piece as if it's being dragged by the computer
                chosen_piece = self.get_piece_at_position(old_position)
                if chosen_piece:
                    chosen_piece.rect.center = new_position
                    chosen_piece.original_position = new_position
                
                new_board = self.board.make_move(move, player=1)  # Pass the computer player as an argument
                
                # Remove the piece from the list at old_position
                if old_position in self.pieces and self.pieces[old_position]:  # Check if the list is not empty
                    moved_piece = self.pieces[old_position].pop()
                    self.pieces[new_position].append(moved_piece)
                    
                    # Reorder the sprites to ensure the dragged piece is drawn last (on top)
                    self.Gobblet_pieces.remove(moved_piece)
                    self.Gobblet_pieces.add(moved_piece)
                if old_position in self.piecesBoard and self.pieces[old_position]:

                    if(len(self.piecesBoard[old_position])==0):
                        self.piecesBoard[old_position].clear()
                    else:
                        self.piecesBoard[old_position].pop()
                    self.piecesBoard[new_position].append(moved_piece)
                    
         
            else:
                print("\nno valid moves for White!!!\n")
          
         
        self.board.switchPlayer()
        self.printBoard()
                
    def MediumLevelAI(self):
        if(self.game_is_over()):
            time.sleep(3)
            Bool,winner=self.game_is_over()
            self.game.curr_menu=self.game.win_screen
            self.game.curr_menu.setMsg(winner+" Wins")
            self.run_display=False

        # Simulate the computer making a random move
        if self.board.currentPlayer() == 2 :  # Player 1 is human, Player 2 is the computer
            print("this is player: ", self.board.current_player, " turn")
            from algos import Algos 
            AlgosInstance=Algos(self.game)
            #can be called b2a anywhere with the color parameter
            moveMinMax = AlgosInstance.getBestMoveAlphaBeta(self.board,self.pieces,self.board.current_player,2)  #can be called b2a anywhere with the color parameter
            
            #computer yl3b bel black bsss
         
            
            if moveMinMax:
                old_position = moveMinMax.start_position
                new_position = moveMinMax.end_position
                
                # Update the position of the chosen piece as if it's being dragged by the computer
                chosen_piece = self.get_piece_at_position(old_position)
                if chosen_piece:
                    chosen_piece.rect.center = new_position
                    chosen_piece.original_position = new_position
                
                new_board = self.board.make_move(moveMinMax, player=2)  # Pass the computer player as an argument
                self.game.display.fill(self.BACK_COLOR)
                self.game.display.blit(self.bg, (0, 0))
                # Draw Gobblet pieces
                self.Gobblet_pieces.draw(self.game.display)
                # Remove the piece from the list at old_position
                if old_position in self.pieces and self.pieces[old_position]:  # Check if the list is not empty
                    moved_piece = self.pieces[old_position].pop()
                    self.pieces[new_position].append(moved_piece)
                    
                    # Reorder the sprites to ensure the dragged piece is drawn last (on top)
                    self.Gobblet_pieces.remove(moved_piece)
                    self.Gobblet_pieces.add(moved_piece)
      
            else:
                print("\nno valid moves for BLACk!!!\n")
            self.printBoard()
            # self.board.switchPlayer()
        elif  self.board.currentPlayer()==1:
            print("this is player: ", self.board.current_player, " turn")
            from algos import Algos 
            # gameCopy=copy.deepcopy(self.game)
            AlgosInstance=Algos(self.game)
            moveMinMax = AlgosInstance.getBestMoveAlphaBeta(self.board,self.pieces,self.board.current_player,2)  #can be called b2a anywhere with the color parameter
            #Computer momken yl3b white w black
            #valid_moves = self.get_valid_moves_for_black_pieces()
            
            if moveMinMax:
                old_position = moveMinMax.start_position
                new_position = moveMinMax.end_position
                
                # Update the position of the chosen piece as if it's being dragged by the computer
                chosen_piece = self.get_piece_at_position(old_position)
                if chosen_piece:
                    chosen_piece.rect.center = new_position
                    chosen_piece.original_position = new_position
                    

                new_board = self.board.make_move(moveMinMax, player=1)  # Pass the computer player as an argument
                
                # Remove the piece from the list at old_position
                if old_position in self.pieces and self.pieces[old_position]:  # Check if the list is not empty
                    moved_piece = self.pieces[old_position].pop()
                    self.pieces[new_position].append(moved_piece)
                    
                    # Reorder the sprites to ensure the dragged piece is drawn last (on top)
                    self.Gobblet_pieces.remove(moved_piece)
                    self.Gobblet_pieces.add(moved_piece)
                if old_position in self.piecesBoard and self.pieces[old_position]:
 
                    if(len(self.pieces[old_position])==0):
                        self.pieces[old_position].clear()
                    else:
                        self.pieces[old_position].pop()
                    self.pieces[new_position].append(moved_piece)
                    
       
            else:
                print("\nno valid moves for White!!!\n")
            # self.board.switchPlayer()     
        self.board.switchPlayer()
        self.printBoard()
    
    def printBoard(self):
        board= self.getSimplifiedBoard()
        for row in board:
            print(row)     
                
    def HardAI(self):
        
        self.game.display.fill(self.BACK_COLOR)
        self.game.display.blit(self.bg, (0, 0))
                # Draw Gobblet pieces
        self.Gobblet_pieces.draw(self.game.display)
        if(self.game_is_over()):
            time.sleep(3)
            Bool,winner=self.game_is_over()
            self.game.curr_menu=self.game.win_screen
            self.game.curr_menu.setMsg(winner+" Wins")
            self.run_display=False
        from algos import Algos 
        AlgosInstance=Algos(self.game)
        # Simulate the computer making a random move
        if self.board.currentPlayer() == 2 :  # Player 1 is human, Player 2 is the computer
            print("this is player: ", self.board.current_player, " turn")
            
            #can be called b2a anywhere with the color parameter
            moveAlphaBeta = AlgosInstance.getBestMoveMinimax(self.board,self.pieces,self.board.current_player,2)  #can be called b2a anywhere with the color parameter
            
            #computer yl3b bel black bsss
         
            
            if moveAlphaBeta:
                old_position = moveAlphaBeta.start_position
                new_position = moveAlphaBeta.end_position
                
                # Update the position of the chosen piece as if it's being dragged by the computer
                chosen_piece = self.get_piece_at_position(old_position)
                if chosen_piece:
                    chosen_piece.rect.center = new_position
                    chosen_piece.original_position = new_position
                
                new_board = self.board.make_move(moveAlphaBeta, player=2)  # Pass the computer player as an argument
                self.game.display.fill(self.BACK_COLOR)
                self.game.display.blit(self.bg, (0, 0))
                # Draw Gobblet pieces
                self.Gobblet_pieces.draw(self.game.display)
                
                # Remove the piece from the list at old_position
                if old_position in self.pieces and self.pieces[old_position]:  # Check if the list is not empty
                    moved_piece = self.pieces[old_position].pop()
                    self.pieces[new_position].append(moved_piece)
                    
                    # Reorder the sprites to ensure the dragged piece is drawn last (on top)
                    self.Gobblet_pieces.remove(moved_piece)
                    self.Gobblet_pieces.add(moved_piece)
       
            else:
                print("\nno valid moves for BLACk!!!\n")
           
        elif  self.board.currentPlayer()==1:
            print("this is player: ", self.board.current_player, " turn")

            moveAlphaBeta = AlgosInstance.getBestMoveMinimax(self.board,self.pieces,self.board.current_player,2) #can be called b2a anywhere with the color parameter
            #Computer momken yl3b white w black
          
            
            if moveAlphaBeta:
                old_position = moveAlphaBeta.start_position
                new_position = moveAlphaBeta.end_position
                
                # Update the position of the chosen piece as if it's being dragged by the computer
                chosen_piece = self.get_piece_at_position(old_position)
                if chosen_piece:
                    chosen_piece.rect.center = new_position
                    chosen_piece.original_position = new_position
                
                new_board = self.board.make_move(moveAlphaBeta, player=1)  # Pass the computer player as an argument
                
                # Remove the piece from the list at old_position
                if old_position in self.pieces and self.pieces[old_position]:  # Check if the list is not empty
                    moved_piece = self.pieces[old_position].pop()
                    self.pieces[new_position].append(moved_piece)
                    
                    # Reorder the sprites to ensure the dragged piece is drawn last (on top)
                    self.Gobblet_pieces.remove(moved_piece)
                    self.Gobblet_pieces.add(moved_piece)
                if old_position in self.piecesBoard and self.pieces[old_position]:
                  
                    if(len(self.pieces[old_position])==0):
                        self.pieces[old_position].clear()
                    else:
                        self.pieces[old_position].pop()
                    self.pieces[new_position].append(moved_piece)
                    
                
            else:
                print("\nno valid moves for White!!!\n")

        
                            
        self.board.switchPlayer()
        self.printBoard()
    
    #al fakra an al valid moves lazm tan2s al pieces al adima
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
                                # else:
                                    # print("\nexternal move is invalid!!!!\n")
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
                              
        elif(Color=="white"):
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
                   

        return valid_moves
    

    def game_is_over(self):
        board=self.getSimplifiedBoard()
        # Check for a win horizontally, vertically, or diagonally
        for row in range(4):
            if self._check_row_win(board,row):
                print("Ana row")
                Bool,winner=self._check_row_win(board,row)
                return True,winner

        for col in range(4):
            if self._check_col_win(board,col):
                print("Ana col")
                Bool,winner=self._check_col_win(board,col)
                return True,winner

        if self._check_diag_win(board):
            print("Ana diag")
            Bool,winner=self._check_diag_win(board)
            return True,winner

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
            return True,pieces[0][0]



    def _check_col_win(self,board, col):
        pieces = [board[row][col][-1] for row in range(4) if board[row][col] ]
        counterOfTruth=0
        for piece in pieces:
            if(piece[0]==pieces[0][0]):
                counterOfTruth+=1
            else:
                return False
        if(counterOfTruth==4):
            return True,pieces[0][0]

    def _check_diag_win(self,board):
        pieces = [board[i][i][-1] for i in range(4) if board[i][i]]
        counterOfTruth=0
        for piece in pieces:
            if(piece[0]==pieces[0][0]):
                counterOfTruth+=1
            else:
                return False
        if(counterOfTruth==4):
            return True,pieces[0][0]
        counterOfTruth=0
        pieces=[]
        if(board[0][3]):
            pieces.append(board[0][3][-1])
        if(board[1][2]):
            pieces.append(board[1][2][-1])
        if(board[2][1]):
            pieces.append(board[2][1][-1])
        if(board[3][0]):
            pieces.append(board[3][0][-1])
        for piece in pieces:
            if(piece[0]==pieces[0][0]):
                counterOfTruth+=1
            else:
                return False
        if(counterOfTruth==4):
            return True,pieces[0][0]
        
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
        

    def draw_timer(self,m,s,size,x,y):
        font=pygame.font.Font(self.game.font_name,size)
        text_serface =font.render("{}:{}".format(m,s),True,(250,250,250))
        text_rect=text_serface.get_rect()
        text_rect.center =(x,y) #make the center of the rectag\ngle the given x and y
        self.game.display.blit(text_serface,text_rect)

    def timer(self):
        self.current_time = pygame.time.get_ticks()
        self.elapsed_milliseconds = self.current_time - self.start_time - self.game.total_paused_mseconds
        self.elapsed_seconds = self.elapsed_milliseconds // 1000
        self.clock.tick(60)
        self.show_timer()

    def show_timer(self):
        if self.elapsed_seconds == 60:
            self.start_time = pygame.time.get_ticks()
            self.mins += 1
        if self.mins ==  60:
            pass
        if self.elapsed_seconds <10 and self.mins<10:
            str_sec= "0"+ str(self.elapsed_seconds)
            str_mins= "0"+ str(self.mins)
        elif self.mins<10 :
            str_sec =str(self.elapsed_seconds)
            str_mins= "0" +  str(self.mins)
        else :
            str_sec =str(self.elapsed_seconds)
            str_mins= str(self.mins)
        self.draw_timer(str_mins,str_sec,24,877,40)
