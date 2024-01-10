from cvc import *


class Evaluation:

    def evaluate(view,board):
        """
        Evaluate the given Goblet Game board state.

        Parameters:
        - board_state: Dictionary representing the current state of the game.
        - material_weight: Weight assigned to threats compared to material advantage.


        Returns:
        - A numerical score indicating the desirability of the board state.
        """
        opponent_team_pieces = []  # Array for opponent team
        current_player_pieces = []  # Array for current player team
                
        for pos, pieces in view.board.board_state.items():
            if(len(pieces)!=0):
                if(pieces[-1]):
                    topitem=pieces[-1]
                    if(topitem[1]==view.board.currentPlayer()):
                        if(topitem[0]=="L"):
                            current_player_pieces.append(4)
                        elif(topitem[0]=="M"):
                            current_player_pieces.append(3)
                        elif(topitem[0]=="S"):
                            current_player_pieces.append(2)
                        else:
                            current_player_pieces.append(1)
                    else:
                        if(topitem[0]=="L"):
                            opponent_team_pieces.append(4)
                        elif(topitem[0]=="M"):
                            opponent_team_pieces.append(3)
                        elif(topitem[0]=="S"):
                            opponent_team_pieces.append(2)
                        else:
                            opponent_team_pieces.append(1)

    # # Piece values (you can adjust these based on your preferences)
        V_XS, V_S, V_M, V_L = 1, 3, 5, 7
        sumOpp=0
        for i in range(len(opponent_team_pieces)):
            sumOpp=sumOpp+opponent_team_pieces[i]
        sumCurr=0
        for i in range(len(current_player_pieces)):
            sumCurr=sumCurr+current_player_pieces[i]
        return sumCurr-sumOpp
