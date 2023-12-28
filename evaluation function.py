def evaluate(board_state):
    """
    Evaluate the given Goblet Game board state.

    Parameters:
    - board_state: Dictionary representing the current state of the game.
    - material_weight: Weight assigned to threats compared to material advantage.


    Returns:
    - A numerical score indicating the desirability of the board state.
    """
    # Extract piece counts from the board state
    P_t, R_t, X_t, Z_t = board_state['XS'], board_state['S'], board_state['M'], board_state['L']
    P_o, R_o, X_o, Z_o = board_state['opponent_XS'], board_state['opponent_S'], board_state['opponent_M'], board_state['opponent_L']

    # Piece values (you can adjust these based on your preferences)
    V_XS, V_S, V_M, V_L = 1, 3, 5, 7

    # Calculate material advantage
    material_advantage = (V_XS * P_t + V_S * R_t + V_M * X_t + V_L * Z_t) - (V_XS * P_o + V_S * R_o + V_M * X_o + V_L * Z_o)

    return material_advantage