from cvc import *

class Evaluation:

    def evaluate(view):
        opponent_team_pieces = []  # Array for opponent team
        current_player_pieces = []  # Array for current player team

        for pos, pieces in view.board.board_state.items():
            if len(pieces) != 0:
                if pieces[-1]:
                    top_item = pieces[-1]
                    if top_item[1] == view.board.currentPlayer():
                        # if piece is at corners append 5 to the player score
                        if(pos==(215,110) or pos ==(725,110) or pos==(725,620) or pos==(215,620)):
                            current_player_pieces.append(5)
                        # if piece is at center, append 7 to the player score
                        elif(pos==(385,280) or pos==(555,280) or pos==(555,450) or pos==(385,450)):
                            current_player_pieces.append(7)
                        # append to score according to size of piece at the top of stack    
                        if top_item[0] == "L":
                            current_player_pieces.append(4)
                        elif top_item[0] == "M":
                            current_player_pieces.append(3)
                        elif top_item[0] == "S":
                            current_player_pieces.append(2)
                        else:
                            current_player_pieces.append(1)
                    else:
                        # if piece is at corners append 5 to the opponent score
                        if(pos==(215,110) or pos ==(725,110) or pos==(725,620) or pos==(215,620)):
                            opponent_team_pieces.append(5)
                        # if piece is at corners append 7 to the opponent score
                        elif(pos==(385,280) or pos==(555,280) or pos==(555,450) or pos==(385,450)):
                            opponent_team_pieces.append(7)
                        # append to score according to size of piece at the top of stack
                        if top_item[0] == "L":
                            opponent_team_pieces.append(4)
                        elif top_item[0] == "M":
                            opponent_team_pieces.append(3)
                        elif top_item[0] == "S":
                            opponent_team_pieces.append(2)
                        else:
                            opponent_team_pieces.append(1)

        # According to the previous appended scores, we calculate total player score and opponent score
        sumOpp=0
        for i in range(len(opponent_team_pieces)):
            sumOpp=sumOpp+opponent_team_pieces[i]
        sumCurr=0
        for i in range(len(current_player_pieces)):
            sumCurr=sumCurr+current_player_pieces[i]

        # calculate material advantage for current player
        material_advantage = sumCurr - sumOpp

        # Stacking advantage heuristic
        stacking_advantage = 0
        for pos, pieces in view.board.board_state.items():
            if len(pieces) > 1:
                stacking_advantage += len(pieces) - 1

        # Threat prevention heuristic
        threat_prevention = 0
        winChance=0
        rescueChance=0
        lossChance=0
        boardTemp=view.getSimplifiedBoard()
        
        for row in range(4):
            # Check for a winning situation in the row for Player 1
            if ((check_row_Score(boardTemp,row)==4 )and view.board.currentPlayer()==1 ):
                winChance=winChance+1000
                return 10000000000
            # Check for a rescue chance in the row for Player 1
            elif((check_row_Score(boardTemp,row)==31)and view.board.currentPlayer()==1 ):
                rescueChance=rescueChance+1000
            # Check for a potential winning situation in the row for Player 1
            elif (( check_row_Score(boardTemp,row)==3)and view.board.currentPlayer()==1 ):
                winChance=winChance+1000
            # Check for potential losses or blocked situations in the row for Player 1
            elif((check_row_Score(boardTemp,row)==30 or check_row_Score(boardTemp,row)==40) and view.board.currentPlayer()==1 ):
                lossChance=lossChance-1000
            # Check for a winning situation in the row for Player 2
            elif((check_row_Score(boardTemp,row)==40)and view.board.currentPlayer()==2):
                winChance=winChance+1000
                return 10000000000
            # Check for a rescue chance in the row for Player 2
            elif(check_row_Score(boardTemp,row)==13  and view.board.currentPlayer()==2 ):
                rescueChance=rescueChance+1000
            # Check for a potential winning situation in the row for Player 2
            elif((check_row_Score(boardTemp,row)==30)and view.board.currentPlayer()==2):
                winChance=winChance+1000
            # Check for potential losses or blocked situations in the row for Player 2
            elif((check_row_Score(boardTemp,row)==4 or check_row_Score(boardTemp,row)==3) and view.board.currentPlayer()==2 ):
                lossChance=lossChance-1000
            # Adjust chances for specific situations in the row
            elif(check_row_Score(boardTemp,row)==20 and view.board.currentPlayer()==1):
                lossChance=lossChance-250
            elif(check_row_Score(boardTemp,row)==2 and view.board.currentPlayer()==2):
                lossChance=lossChance-250
            elif(check_row_Score(boardTemp,row)==2 and view.board.currentPlayer()==1):
                winChance=winChance+500
            elif(check_row_Score(boardTemp,row)==20 and view.board.currentPlayer()==2):
                winChance=winChance+500
            
        for col in range(4):
            # Check for a winning situation in the column for Player 1
            if ((check_col_Scores(boardTemp,col)==4)and view.board.currentPlayer()==1 ):
                winChance=winChance+1000
                return 10000000000
            # Check for a rescue chance in the column for Player 1
            elif((check_col_Scores(boardTemp,col)==31)and view.board.currentPlayer()==1 ):
                rescueChance=rescueChance+1000
            # Check for a potential winning situation in the column for Player 1
            elif((check_col_Scores(boardTemp,col)==3)and view.board.currentPlayer()==1 ):
                rescueChance=rescueChance+1000
            # Check for potential losses or blocked situations in the column for Player 1
            elif((check_col_Scores(boardTemp,col)==30 or check_col_Scores(boardTemp,col)==40) and view.board.currentPlayer()==1 ):
                lossChance=lossChance-1000
            # Check for a winning situation in the column for Player 2
            elif((check_col_Scores(boardTemp,col)==40)and view.board.currentPlayer()==2):
                winChance=winChance+ 1000
                return 10000000000
            # Check for a rescue chance in the column for Player 2
            elif(check_col_Scores(boardTemp,col)==13  and view.board.currentPlayer()==2 ):
                rescueChance=rescueChance+1000
            # Check for a potential winning situation in the column for Player 2
            elif((check_col_Scores(boardTemp,col)==30)and view.board.currentPlayer()==2):
                winChance=winChance+ 1000
            # Check for potential losses or blocked situations in the column for Player 2
            elif((check_col_Scores(boardTemp,col)==4 or check_col_Scores(boardTemp,col)==3) and view.board.currentPlayer()==2 ):
                lossChance=lossChance-1000
            # Adjust chances for specific situations in the column
            elif(check_col_Scores(boardTemp,col)==20 and view.board.currentPlayer()==1):
                lossChance=lossChance-250
            elif(check_col_Scores(boardTemp,col)==2 and view.board.currentPlayer()==2):
                lossChance=lossChance-250
            elif(check_col_Scores(boardTemp,col)==2 and view.board.currentPlayer()==1):
                winChance=winChance+500
            elif(check_col_Scores(boardTemp,col)==20 and view.board.currentPlayer()==2):
                winChance=winChance+500

        # Check for a winning situation in the left diagonal for Player 1
        if ((check_diag_ScoresLeft(boardTemp)==4 )and view.board.currentPlayer()==1 ):
                winChance=winChance+1000
                return 10000000000
        # Check for a rescue chance in the left diagonal for Player 1
        elif((check_diag_ScoresLeft(boardTemp)==31)and view.board.currentPlayer()==1 ):
                rescueChance=rescueChance+1000
        # Check for a potential winning situation in the left diagonal for Player 1
        elif((check_diag_ScoresLeft(boardTemp)==3)and view.board.currentPlayer()==1 ):
                winChance=winChance+ 1000
        # Check for potential losses or blocked situations in the left diagonal for Player 1
        elif((check_diag_ScoresLeft(boardTemp)==30 or check_diag_ScoresLeft(boardTemp)==40) and view.board.currentPlayer()==1 ):
                lossChance=lossChance-1000
        # Check for a winning situation in the left diagonal for Player 2
        elif((check_diag_ScoresLeft(boardTemp)==40)and view.board.currentPlayer()==2):
                winChance=winChance+ 1000
                return 10000000000
        # Check for a rescue chance in the left diagonal for Player 2
        elif(check_diag_ScoresLeft(boardTemp)==13  and view.board.currentPlayer()==2 ):
                rescueChance=rescueChance+1000
        # Check for a potential winning situation in the left diagonal for Player 2
        elif(check_diag_ScoresLeft(boardTemp)==30  and view.board.currentPlayer()==2 ):
                winChance=winChance+ 1000
        # Check for potential losses or blocked situations in the left diagonal for Player 2
        elif((check_diag_ScoresLeft(boardTemp)==4 or check_diag_ScoresLeft(boardTemp)==3) and view.board.currentPlayer()==2 ):
                lossChance=lossChance-1000
        # Adjust chances for specific situations in the left diagonal
        elif(check_diag_ScoresLeft(boardTemp)==20 and view.board.currentPlayer()==1):
                lossChance=lossChance-250
        elif(check_diag_ScoresLeft(boardTemp)==2 and view.board.currentPlayer()==2):
                lossChance=lossChance-250
        elif(check_diag_ScoresLeft(boardTemp)==2 and view.board.currentPlayer()==1):
            winChance=winChance+500
        elif(check_diag_ScoresLeft(boardTemp)==20 and view.board.currentPlayer()==2):
            winChance=winChance+500

        # Check for a winning situation in the right diagonal for Player 1
        if ((check_diag_Scoresright(boardTemp)==4 )and view.board.currentPlayer()==1 ):
                winChance=winChance+1000
                return 10000000000
        # Check for a rescue chance in the right diagonal for Player 1
        elif((check_diag_Scoresright(boardTemp)==31)and view.board.currentPlayer()==1 ):
                rescueChance=rescueChance+1000
        # Check for a potential winning situation in the right diagonal for Player 1
        elif (( check_diag_Scoresright(boardTemp)==3)and view.board.currentPlayer()==1 ):
                winChance=winChance+1000
        # Check for potential losses or blocked situations in the right diagonal for Player 1
        elif((check_diag_Scoresright(boardTemp)==30 or check_diag_Scoresright(boardTemp)==40) and view.board.currentPlayer()==1 ):
                lossChance=lossChance-1000
        # Check for a winning situation in the right diagonal for Player 2
        elif(( check_diag_Scoresright(boardTemp)==40)and view.board.currentPlayer()==2):
                winChance=winChance+ 1000
                return 10000000000
        # Check for a rescue chance in the right diagonal for Player 2
        elif(check_diag_Scoresright(boardTemp)==13  and view.board.currentPlayer()==2 ):
                rescueChance=rescueChance+1000
        # Check for a potential winning situation in the right diagonal for Player 2
        elif(( check_diag_Scoresright(boardTemp)==30)and view.board.currentPlayer()==2):
                winChance=winChance+ 1000
        # Check for potential losses or blocked situations in the right diagonal for Player 2
        elif((check_diag_Scoresright(boardTemp)==4 or check_diag_Scoresright(boardTemp)==3) and view.board.currentPlayer()==2 ):
                lossChance=lossChance-1000
        # Adjust chances for specific situations in the right diagonal
        elif(check_diag_Scoresright(boardTemp)==20 and view.board.currentPlayer()==1):
            lossChance=lossChance-250
        elif(check_diag_Scoresright(boardTemp)==2 and view.board.currentPlayer()==2):
            lossChance=lossChance-250
        elif(check_diag_Scoresright(boardTemp)==2 and view.board.currentPlayer()==1):
                winChance=winChance+500
        elif(check_diag_Scoresright(boardTemp)==20 and view.board.currentPlayer()==2):
                winChance=winChance+500
    
        for pos, pieces in view.board.board_state.items():
            # Check for multiple pieces at the same position controlled by the opponent
            if len(pieces) > 1 and pieces[-1][1] != view.board.currentPlayer():
                threat_prevention += len(pieces)

        # Combine heuristics with piece values
        evaluation_score = material_advantage + stacking_advantage + threat_prevention+winChance+lossChance+rescueChance
        return evaluation_score
    
def check_row_Score(board,row):
    pieces = [board[row][col][-1] for col in range(4) if board[row][col]]
    counterOfTruth=0
    for piece in pieces:
        if(piece[0]=='white'):
            counterOfTruth+=1
        else:
            counterOfTruth+=10
    return counterOfTruth
    
def check_col_Scores(board, col):
    pieces = [board[row][col][-1] for row in range(4) if board[row][col] ]
    counterOfTruth=0
    for piece in pieces:
        if(piece[0]=='white'):
            counterOfTruth+=1
        else:
            counterOfTruth+=10
    return counterOfTruth
    
def check_diag_ScoresLeft(board):
    pieces = [board[i][i][-1] for i in range(4) if board[i][i]]
    counterOfTruth=0
    for piece in pieces:
        if(piece[0]=='white'):
            counterOfTruth+=1
        else:
            counterOfTruth+=10
    return counterOfTruth
    
def check_diag_Scoresright(board):
    pieces=[]
    counterOfTruth=0
    if(board[0][3]):
        pieces.append(board[0][3][-1])
    if(board[1][2]):
        pieces.append(board[1][2][-1])
    if(board[2][1]):
        pieces.append(board[2][1][-1])
    if(board[3][0]):
        pieces.append(board[3][0][-1])
    for piece in pieces:
        if(piece[0]=='white'):
            counterOfTruth+=1
        else:
            counterOfTruth+=10
    return counterOfTruth
