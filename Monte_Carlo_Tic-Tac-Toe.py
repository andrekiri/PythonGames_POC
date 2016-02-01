"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 1    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player


# Add your functions here.
def mc_trial(board, player):
    """
    Plays on game randomly
    """
    current_player = player
    while board.check_win() == None :        
        next_square = random.choice(board.get_empty_squares())
        board.move(next_square[0], next_square[1], current_player)
        current_player = provided.switch_player(current_player)

    
def mc_update_scores(scores, board, player):
    """
    Updates the score with the score of the board
    """
    if board.check_win()== player:
        for idx in range(board.get_dim()):
            for jdx in range(board.get_dim()):
                if board.square(idx, jdx) == player:
                    scores[idx][jdx] += MCMATCH
                elif board.square(idx, jdx) == provided.switch_player(player):
                    scores[idx][jdx] -= MCOTHER
    elif board.check_win()== provided.switch_player(player):
        print 
        for idx in range(board.get_dim()):
            for jdx in range(board.get_dim()):
                if board.square(idx, jdx) == player:
                    scores[idx][jdx] -= MCMATCH
                elif board.square(idx, jdx) == provided.switch_player(player):
                    scores[idx][jdx] += MCOTHER         
    
        
    
def get_best_move(board, scores):
    """
    Picks a move rondomly a highest score empty square
    """
    max_list = [board.get_empty_squares()[0]]
    max_score = scores[max_list[0][0]][max_list[0][1]]
    for idx in board.get_empty_squares():
        if scores[idx[0]][idx[1]] > max_score:
            max_list = [idx] 
            max_score = scores[idx[0]][idx[1]]
        elif scores[idx[0]][idx[1]] == max_score :
            max_list.append(idx)
    return random.choice(max_list)
            
    
def mc_move(board, player, trials):
    """
    Applies a move
    """
    scores = [ [0 for dummy_col in range(board.get_dim())] for dummy_row in range(board.get_dim())]
    for dummy_idx in range(trials):
        simulation = board.clone()
        mc_trial(simulation, player)
        mc_update_scores(scores, simulation, player)
    if board.check_win() == None:
        return get_best_move(board, scores)
      
    #player = provided.switch_player(player)
        
#game = provided.TTTBoard(3)
#print game
#for idx in range(5):
#    mc_move(game, PLAYERX, 10)
#    print game
#mc_move(provided.TTTBoard(3, False, [[PLAYERX, PLAYERX, PLAYERO], [EMPTY, PLAYERX, PLAYERX], [PLAYERO, EMPTY, PLAYERO]]), PLAYERO, NTRIALS)
# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
