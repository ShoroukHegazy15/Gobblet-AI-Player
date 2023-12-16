from game import Game
#from board import Board
#from move import Move
g=Game()

while(g.running):
   g.curr_menu.display_menu()
   g.game_loop()
g.quit()
    
 #Create a board
    #board = Board()

# Display the initial board state
#print(board)

# Generate and display possible moves for a player
#possible_moves = board.generate_possible_moves(Board.WHITE_PLAYER)
#for move in possible_moves:
 #   print(move)

# Make a move and display the updated board state
#move = Move(0, 0, 1, 1, 1, 0)  # Example move
#board.make_move(move)
#print(board)
