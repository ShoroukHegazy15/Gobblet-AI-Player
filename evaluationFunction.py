from cvc import *

class Evaluation:

    def evaluate(view, board):
        opponent_team_pieces = []  # Array for opponent team
        current_player_pieces = []  # Array for current player team

        for pos, pieces in view.board.board_state.items():
            if len(pieces) != 0:
                if pieces[-1]:
                    top_item = pieces[-1]
                    if top_item[1] == view.board.currentPlayer():
                        if top_item[0] == "L":
                            current_player_pieces.append(4)
                        elif top_item[0] == "M":
                            current_player_pieces.append(3)
                        elif top_item[0] == "S":
                            current_player_pieces.append(2)
                        else:
                            current_player_pieces.append(1)
                    else:
                        if top_item[0] == "L":
                            opponent_team_pieces.append(4)
                        elif top_item[0] == "M":
                            opponent_team_pieces.append(3)
                        elif top_item[0] == "S":
                            opponent_team_pieces.append(2)
                        else:
                            opponent_team_pieces.append(1)

        # Piece values (you can adjust these based on your preferences)
        sumOpp=0
        for i in range(len(opponent_team_pieces)):
            sumOpp=sumOpp+opponent_team_pieces[i]
        sumCurr=0
        for i in range(len(current_player_pieces)):
            sumCurr=sumCurr+current_player_pieces[i]
        material_advantage = sumCurr - sumOpp

        # Stacking advantage heuristic
        stacking_advantage = 0
        for pos, pieces in view.board.board_state.items():
            if len(pieces) > 1:
                stacking_advantage += len(pieces) - 1

        # Threat prevention heuristic
        threat_prevention = 0
        for pos, pieces in view.board.board_state.items():
            if len(pieces) > 1 and pieces[-1][1] != view.board.currentPlayer():
                threat_prevention += len(pieces)

        # Combine heuristics with piece values
        evaluation_score = material_advantage + stacking_advantage + threat_prevention

        return evaluation_score
