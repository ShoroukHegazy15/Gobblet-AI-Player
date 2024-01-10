from trialmove import Move, Board
from view import View
from evaluationFunction import Evaluation
from cvc import *
# from cvc import *
INFINITY = float('inf')

class Algos:
    def getBestMoveMinimax(self,ViewCVC, board, player, maxDepth):
        # Get best move for minmax algo
        score, move = self.minimax(ViewCVC,board, player, maxDepth, 0)
        # return move
        return move

    def minimax(self,ViewCVC, board, player, maxDepth, currentDepth):
        # check if we're done recursing
        if ViewCVC.game_is_over() or currentDepth == maxDepth:
            return Evaluation.evaluate(ViewCVC,board), None

        # otherwise get values from below
        bestMove = None
        if board.currentPlayer() == player:
            bestScore = -INFINITY
        else:
            bestScore = INFINITY

        # go through each valid move
        #ta2riban hia validmoves l boarda di kol mara bigib nafs al vaildmoves
        #kol mara bit3aml 3al aol board
        for move in ViewCVC.get_valid_moves_for_pieces(board.currentPlayer()):
            #hna al valid moves btt3ml azai 
            newBoard = board.make_move(move, player)
            #al moshkla an al lazam tat3ml m3 al board ali complicated awi homa mfrod tat3ml m3 code ali board w tal3i al state
            #al board state lo fiha color yab2a al modo3 at7l al code sha8l tmm
            nowPlayer=0
            if(player==1):
                nowPlayer=2
            else:
                nowPlayer=1
            currentScore, currentMove = self.minimax(ViewCVC,newBoard,nowPlayer, maxDepth, currentDepth + 1)

            if board.currentPlayer() == player:
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
            return Evaluation.evaluate(board), None

        # Otherwise get values from below
        bestMove = None
        bestScore = -INFINITY

        # Go through each move
        for move in View.get_valid_moves_for_black_pieces():
            newBoard = board.make_move(move, player)
            # Recurse
            recursedScore, _ = self.alphaBeta(newBoard, maxDepth, currentDepth + 1, -beta, -max(alpha, bestScore))
            currentScore = -recursedScore

            # Update the best score
            if currentScore > bestScore:
                bestScore = currentScore
                bestMove = move

            # Update alpha for pruning
            alpha = max(alpha, bestScore)

            # If we’re outside the bounds, then prune: exit immediately
            if bestScore >= beta:
                return bestScore, bestMove

        return bestScore, bestMove

    def getBestMoveAlphaBeta(self, board, maxDepth):
        # Get best move for alpha beta algo
        score, move = self.alphaBeta(board, maxDepth, 0, -INFINITY, INFINITY)
        # return move
        return move

    def getBestMoveAlphaBetaID(self, board, maxDepth):
        # Get best move for Alpha Beta Iterative Deepening algo
        bestMove = None
        for depth in range(1, maxDepth + 1):
            score, move = self.alphaBeta(board, depth, -float('inf'), float('inf'))
            bestMove = move

        return bestMove
