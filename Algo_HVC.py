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

        # return move
        return move
    def minimax(self,ViewHVC, board, player, maxDepth, currentDepth):
        self.i += 1  # Increment self.i
        print("i= ", self.i)
        print("\n")
        
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
            newBoard = board.make_move(move, player)
          
            if newBoard is not None:
                nowPlayer = 3 - player  # Switch players
                currentScore, _ = self.minimax(ViewHVC, newBoard, nowPlayer, maxDepth, currentDepth + 1)
                board.undo_last_move(player) 

                if board.currentPlayer() == player:
                    if currentScore > bestScore:
                        bestScore = currentScore
                        bestMove = move
                else:
                    if currentScore < bestScore:
                        bestScore = currentScore
                        bestMove = move

        print("bestscore",{bestScore})
        return bestScore, bestMove

    
