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
                    
            #if newBoard is not None:
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
                #3yzeen n update el pieces kman
                #if new_position in ViewHVC.pieces :
                    # Remove the dragged_piece from the list at old_position
                ViewHVC.pieces[new_position].remove(chosen_piece)
                #if old_position in ViewHVC.pieces and chosen_piece in ViewHVC.pieces[old_position]:
                    # Append the dragged_piece to the list at new_position
                ViewHVC.pieces[old_position].append(chosen_piece)
                
                #if old_position in ViewHVC.pieces and ViewHVC.pieces[old_position]:  # Check if the list is not empty
                #moved_piece = ViewHVC.pieces[move.old_position].pop()
                #ViewHVC.pieces[move.start_position].append(move.piece_size)

        #print("bestscore",{bestScore})
        return bestScore, bestMove

    def getBestMoveAlphaBeta(self, ViewHVC, board, player, maxDepth):
            # if(player==2 and self.view.board.currentPlayer()==1):
            #     self.view.board.switchPlayer()
            # elif(player==1 and self.view.board.currentPlayer()==2):
            #     self.view.board.switchPlayer()
            # self.view.board=board
            # self.view.pieces=pieces
            # Get best move for alpha beta algo
            score, move = self.alphaBeta(ViewHVC, board, player, maxDepth, 0, -INFINITY, INFINITY)
            self.best_move = move
            # return move
            return move
    
    def getBestMoveAlphaBetaID(self, ViewHVC, board, player, maxDepth):
        # if(player==2 and self.view.board.currentPlayer()==1):
        #     self.view.board.switchPlayer()
        # elif(player==1 and self.view.board.currentPlayer()==2):
        #     self.view.board.switchPlayer()
        # self.view.board=board
        # self.view.pieces=pieces
        # Get best move for Alpha Beta Iterative Deepening algo
        bestMove = None
        for depth in range(1, maxDepth + 1):
            score, move = self.alphaBeta(ViewHVC, board, player, depth, -INFINITY, INFINITY)
            bestMove = move
            self.best_move = move
        return bestMove
    
    def alphaBeta(self, ViewHVC, board, player, maxDepth, currentDepth, alpha, beta):
        self.i +=1
        print("i=", self.i)
        print("\n")
        # Check if we’re done recursing
        if ViewHVC.game_is_over() or currentDepth == maxDepth:
            # check if player is same as current_player attribute of board
            return Evaluation.evaluate(ViewHVC, board), None
    
        # Otherwise get values from below
        bestMove = None
        bestScore = -INFINITY
    
        # Go through each move
        # if(player==1):
        #     playerColor="white"
        # elif(player==2):
        #     playerColor="black"
        valid_moves = ViewHVC.get_valid_moves_for_pieces(self.player_colors[player])
    
        for i in range(len(valid_moves)):
            #hna al valid moves btt3ml azai 
            move=valid_moves[i]
            newBoard = board.make_move(move, player)
    
            if newBoard is not None:
                nowPlayer = 3 - player  # Switch players
                currentScore, _ = self.alphaBeta(ViewHVC, newBoard, nowPlayer, maxDepth, currentDepth + 1, -beta, -max(alpha, bestScore))
                board.undo_last_move()
    
            # if move.start_position in self.view.pieces and self.view.pieces[move.start_position]:  # Check if the list is not empty
            #     moved_piece = self.view.pieces[move.start_position].pop()
            #     self.view.pieces[move.end_position].append(moved_piece)
            
            # Recurse
            # recursedScore, _ = self.alphaBeta(newBoard, nowPlayer, maxDepth, currentDepth + 1, -beta, -max(alpha, bestScore))
            # currentScore = -recursedScore
    
            # Update the best score
                if board.currentPlayer() == player:
                    if currentScore > bestScore:
                        bestScore = currentScore
                        bestMove = move
                    else:
                        if currentScore < bestScore:
                            bestScore = currentScore
                            bestMove = move
    
            # Update alpha for pruning
            # alpha = max(alpha, bestScore)
    
            # If we’re outside the bounds, then prune: exit immediately
            # if bestScore >= beta:
            #     return bestScore, bestMove
            
            # if move.end_position in self.view.pieces and self.view.pieces[move.end_position]:  # Check if the list is not empty
            #     undoedPiece = self.view.pieces[move.end_position].pop()
            #     self.view.pieces[move.start_position].append(undoedPiece)
                
            # undoedMove=Move(move.end_position,move.start_position,move.piece_size)
            # self.view.board.undo_moves(undoedMove,player)
        print("bestscore",{bestScore})
        return bestScore, bestMove
        
