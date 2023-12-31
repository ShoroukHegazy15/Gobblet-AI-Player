from trialmove import Move, Board
from view import View
from evaluation import Evaluate
INFINITY = float('inf')

class Algos:   
  def minmax(self, board, player, maxDepth, currentDepth):
  # check if we're done recursing
        if  board.game_is_over() or currentDepth == maxDepth:
            return Evaluate.evaluate(board.board_state), None

  # otherwise get values from below
        bestMove = None
        if board.currentPlayer() == player:
            bestScore = -INFINITY
        else:
            bestScore = INFINITY
          
 # go through each valid move
        for move in View.get_valid_moves_for_black_pieces():
            newBoard = board.make_move(move, player)
            currentScore, currentMove = self.minmax(newBoard, player, maxDepth, currentDepth + 1)

            if board.current_player == player:
                if currentScore > bestScore:
                    bestScore = currentScore
                    bestMove = move
            else:               
                if currentScore < bestScore:
                    bestScore = currentScore
                    bestMove = move

        return bestScore, bestMove

  def alphaBeta(self, board, maxDepth, currentDepth, alpha, beta):
        # Check if we’re done recursing
        if board.game_is_over() or currentDepth == maxDepth:
            # check if player is same as current_player attribute of board
            player = board.currentPlayer()
            return Evaluate.evaluate(board.board_state), None

        # Otherwise get values from below
        bestMove = None
        bestScore = -INFINITY
    
        # Go through each move
        for move in View.get_valid_moves_for_black_pieces():
            newBoard = board.make_move(move, player)
            # Recurse
            recursedScore, currentMove = self.alphaBeta(newBoard, maxDepth, currentDepth + 1, -beta, -max(alpha, bestScore))
            currentScore = -recursedScore
    
            # Update the best score
            if currentScore > bestScore:
                bestScore = currentScore
                bestMove = move
    
            # If we’re outside the bounds, then prune: exit immediately
            if bestScore >= beta:
                return bestScore, bestMove
        return bestScore, bestMove
