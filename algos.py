from cvc import *
from trialmove import Move, Board
from view import View
from evaluationFunction import *
import importlib
# from cvc import *
INFINITY = float('inf')

class Algos:
    
    def __init__(self,game):
        from cvc import ViewCVC
        self.view=ViewCVC(game)
        
    
    def getBestMoveMinimax(self, board, player, maxDepth):
        if(player==2 and self.view.board.currentPlayer()==1):
            self.view.board.switchPlayer()
        elif(player==1 and self.view.board.currentPlayer()==2):
            self.view.board.switchPlayer()
        self.view.board=board
        # Get best move for minmax algo
        score, move = self.minimax(board, player, maxDepth, 0)
        # return move
        return move

    def minimax(self, board, player, maxDepth, currentDepth):
        # check if we're done recursing
        if self.view.game_is_over() or currentDepth == maxDepth:
            return Evaluation.evaluate(self.view,board), None

        # otherwise get values from below
        bestMove = None
        if self.view.board.currentPlayer() == player:
            bestScore = -INFINITY
        else:
            bestScore = INFINITY

        # go through each valid move
        #ta2riban hia validmoves l boarda di kol mara bigib nafs al vaildmoves
        #kol mara bit3aml 3al aol board
        if(player==1):
            playerColor="white"
        elif(player==2):
            playerColor="black"
        for i in range(len(self.view.get_valid_moves_for_pieces(playerColor))):
            #hna al valid moves btt3ml azai 
            move=self.view.get_valid_moves_for_pieces(playerColor)[i]
            newBoard = self.view.board.make_move(move, player)
            #al moshkla an al lazam tat3ml m3 al board ali complicated awi homa mfrod tat3ml m3 code ali board w tal3i al state
            #al board state lo fiha color yab2a al modo3 at7l al code sha8l tmm
            # Remove the piece from the list at old_position
            if move.start_position in self.view.pieces and self.view.pieces[move.start_position]:  # Check if the list is not empty
                moved_piece = self.view.pieces[move.start_position].pop()
                self.view.pieces[move.end_position].append(moved_piece)
                #     # Reorder the sprites to ensure the dragged piece is drawn last (on top)
                # self.view.Gobblet_pieces.remove(moved_piece)
                # self.view.Gobblet_pieces.add(moved_piece)
            nowPlayer=0
            if(player==1):
                nowPlayer=2
            else:
                nowPlayer=1
            currentScore, currentMove = self.minimax(newBoard,nowPlayer, maxDepth, currentDepth + 1)
            #mfrod n3ml undo l move
            if board.currentPlayer() == player:
                if currentScore > bestScore:
                    bestScore = currentScore
                    bestMove = move
            else:
                if currentScore < bestScore:
                    bestScore = currentScore
                    bestMove = move
            if move.end_position in self.view.pieces and self.view.pieces[move.end_position]:  # Check if the list is not empty
                undoedPiece = self.view.pieces[move.end_position].pop()
                self.view.pieces[move.start_position].append(undoedPiece)
                
            undoedMove=Move(move.end_position,move.start_position,move.piece_size)
            self.view.board.undo_moves(undoedMove,player)

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
