from trialmove import Move, Board
from evaluationFunction import Evaluation
INFINITY = float('inf')

class Algos:
    player_colors = {1: "white", 2: "black"}
    def __init__(self):
        self.i = 0  

    def getBestMoveMinimax(self,ViewHVC, board, player, maxDepth):
        # Get best move for minmax algo
        score, move = self.minimax(ViewHVC,board, player, maxDepth, 0)
        self.best_move = move
        return move
        
    def minimax(self,ViewHVC, board, player, maxDepth, currentDepth):
        # check if we're done recursing
        if ViewHVC.game_is_over() or currentDepth == maxDepth:
            return Evaluation.evaluate(ViewHVC,board),None

        # otherwise get values from below
        bestMove = None
        if board.currentPlayer() == player:
            bestScore = -INFINITY
        else:
            bestScore = INFINITY

        valid_moves = ViewHVC.get_valid_moves_for_pieces(self.player_colors[player])
        for i in range(len(valid_moves)):
            move = valid_moves[i]
            if move and move.start_position is not None and move.end_position is not None:
                old_position = move.start_position
                new_position = move.end_position
                
            # Update the position of the chosen piece as if it's being dragged by the computer
                chosen_piece = ViewHVC.get_piece_at_position(old_position)
                
            newBoard = board.make_move(move, player)
            if newBoard is not None:
            # If the move was successful, update the current board
                               
                if old_position in ViewHVC.pieces and chosen_piece in ViewHVC.pieces[old_position]:
                    # Remove the dragged_piece from the list at old_position
                    ViewHVC.pieces[old_position].remove(chosen_piece)
                if new_position in ViewHVC.pieces :
                    # Append the dragged_piece to the list at new_position
                    ViewHVC.pieces[new_position].append(chosen_piece)
                    
                nowPlayer = 3 - player  # Switch players
                currentScore, _ = self.minimax(ViewHVC, newBoard, nowPlayer, maxDepth, currentDepth + 1)

                if board.currentPlayer() == player:
                    if currentScore > bestScore:
                        bestScore = currentScore
                        bestMove = move
                else:
                    if currentScore < bestScore:
                        bestScore = currentScore
                        bestMove = move
                board.undo_last_move(player)    #4elt mn boardstate
                
                ViewHVC.pieces[new_position].remove(chosen_piece)
                ViewHVC.pieces[old_position].append(chosen_piece)
                
        return bestScore, bestMove

    def getBestMoveAlphaBeta(self, ViewHVC, board, player, maxDepth):
    # Get best move for alpha beta algo
        _, move = self.alphaBeta(ViewHVC, board, player, maxDepth, 0, -INFINITY, INFINITY)
        self.best_move = move
        return move

        
    def alphaBeta(self, ViewHVC, board, player, maxDepth, currentDepth, alpha, beta):
        # Check if we’re done recursing
        if ViewHVC.game_is_over() or currentDepth == maxDepth:
            return Evaluation.evaluate(ViewHVC, board), None
    
        # Otherwise get values from below
        bestMove = None
        bestScore = -INFINITY if player == 2 else INFINITY  # Initialize based on player's turn
    
        valid_moves = ViewHVC.get_valid_moves_for_pieces(self.player_colors[player])
        for i in range(len(valid_moves)):
            #hna al valid moves btt3ml azai 
            move=valid_moves[i]
            if move and move.start_position is not None and move.end_position is not None:
                old_position = move.start_position
                new_position = move.end_position
                
            # Update the position of the chosen piece as if it's being dragged by the computer
                chosen_piece = ViewHVC.get_piece_at_position(old_position)
                
            newBoard = board.make_move(move, player)
            if newBoard is not None:
            # If the move was successful, update the current board
                if old_position in ViewHVC.pieces and chosen_piece in ViewHVC.pieces[old_position]:
                    # Remove the dragged_piece from the list at old_position
                    ViewHVC.pieces[old_position].remove(chosen_piece)
                if new_position in ViewHVC.pieces :
                    # Append the dragged_piece to the list at new_position
                    ViewHVC.pieces[new_position].append(chosen_piece)
                
                nowPlayer = 3 - player  # Switch players
                currentScore, _ = self.alphaBeta(ViewHVC, newBoard, nowPlayer, maxDepth, currentDepth + 1, alpha, beta)
                
                """ # Update the best score
                if board.currentPlayer() == player:    #maxi  black 2 AI
                    if currentScore > bestScore:
                        bestScore = currentScore
                        bestMove = move
                    else:
                        if currentScore < bestScore:   #mini white 1 ana
                            bestScore = currentScore
                            bestMove = move """
                 # Update the best score
                if player == 2:  # Maximizing player (black AI)
                    bestScore = max(bestScore, currentScore)
                    if currentScore == bestScore:
                        bestMove = move
                    alpha = max(alpha, bestScore)  # Update alpha for pruning
                else:  # Minimizing player (white human)
                    bestScore = min(bestScore, currentScore)
                    if currentScore == bestScore:
                        bestMove = move
                    beta = min(beta, bestScore)  # Update beta for pruning
                
                board.undo_last_move(player)
                ViewHVC.pieces[new_position].remove(chosen_piece)
                ViewHVC.pieces[old_position].append(chosen_piece)
                
                # Pruning condition
                if beta <= alpha:
                    break

        return bestScore, bestMove
