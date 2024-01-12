# Import necessary classes and modules
from score import Evaluator
from board import BoardState, BoardUtils
from dice import DiceSimulator
from move import MoveUtils

# Constants
MAX_DEPTH = 3
diceSimulator = DiceSimulator.getInstance()

# Function to make an optimal move using Minimax algorithm
def make_optimal_move(state, dice1, dice2, whites_turn):
    # Get all possible move results for the given dice rolls
    states = MoveUtils.get_all_possible_move_results(state, dice1, dice2, whites_turn)
    
    # Initialize variables to track the best score and optimal state
    best_score = -1e9
    optimal_state = None
    
    # Iterate through possible states to find the one with the highest Minimax score
    for bs in states:
        score_for_state = get_minimax_score(bs, not whites_turn, MAX_DEPTH, whites_turn)
        
        # Update the best score and optimal state if a higher score is found
        if best_score < score_for_state:
            best_score = score_for_state
            optimal_state = bs
    
    return optimal_state

# Function to calculate the Minimax score for a given state
def get_minimax_score(state, whites_turn, depth, initial_turn_white):
    # Base case: return the score of the state if depth is 0
    if depth == 0:
        return Evaluator.get_score_of_state_for(state, initial_turn_white)
    
    # Initialize score variable
    score = 0.0
    
    # Iterate through possible dice rolls
    for d1 in range(1, 7):
        for d2 in range(d1, 7):
            # Calculate dice probability
            dice_probability = 1.0 / 36.0 if d1 == d2 else 1.0 / 18.0
            
            # Get all possible move results for the current dice rolls
            states = MoveUtils.get_all_possible_move_results(state, d1, d2, whites_turn)
            
            # Determine whether to minimize or maximize score
            min_flag = (initial_turn_white != whites_turn)
            max_score = -1e9 if not min_flag else 1e9
            
            # Iterate through possible states to find the Minimax score
            for bs in states:
                if not min_flag:
                    max_score = max(max_score, get_minimax_score(bs, not whites_turn, depth - 1, initial_turn_white))
                else:
                    max_score = min(max_score, get_minimax_score(bs, not whites_turn, depth - 1, initial_turn_white))
            
            # Update the overall score with the calculated Minimax score
            score += dice_probability * max_score
    
    return score

# Function to make an optimal move for a 1-ply lookahead
def make_optimal_move_1ply(state, dice1, dice2, whites_turn):
    # Get all possible move results for the given dice rolls
    states = MoveUtils.get_all_possible_move_results(state, dice1, dice2, whites_turn)
    
    # Initialize variables to track the best score and optimal state
    best_score = -1e9
    optimal_state = None
    
    # Iterate through possible states to find the one with the highest Minimax score
    for bs in states:
        score_for_state = get_minimax_score_1ply(bs, not whites_turn, MAX_DEPTH, whites_turn, -1e9, +1e9)
        
        # Update the best score and optimal state if a higher score is found
        if best_score < score_for_state:
            best_score = score_for_state
            optimal_state = bs
    
    return optimal_state

# Function to calculate the Minimax score for a 1-ply lookahead
def get_minimax_score_1ply(state, whites_turn, depth, initial_turn_white, alfa, beta):
    # Base case: return the score of the state if depth is 0
    if depth == 0:
        return Evaluator.get_score_of_state_for(state, initial_turn_white)
    
    # Initialize score variable
    score = 0.0
    
    # Iterate through possible random dice rolls
    for _ in range(14):
        d1, d2 = diceSimulator.get_random_dice(), diceSimulator.get_random_dice()
        dice_probability = 1.0 / 36.0 if d1 == d2 else 1.0 / 18.0
        
        # Get all possible move results for the current dice rolls
        states = MoveUtils.get_all_possible_move_results(state, d1, d2, whites_turn)
        
        # Determine whether to minimize or maximize score
        min_flag = (initial_turn_white != whites_turn)
        max_score = -1e9 if not min_flag else 1e9
        
        # Iterate through possible states to find the Minimax score
        for bs in states:
            if not min_flag:
                max_score = max(max_score, get_minimax_score_1ply(bs, not whites_turn, depth - 1, initial_turn_white, alfa, beta))
                alfa = max_score
            else:
                max_score = min(max_score, get_minimax_score_1ply(bs, not whites_turn, depth - 1, initial_turn_white, alfa, beta))
                beta = max_score
            
            # Alpha-beta pruning
            if beta - alfa <= 0.0001:
                return beta
        
        # Update the overall score with the calculated Minimax score
        score += dice_probability * max_score
    
    return score

# Main function for testing the Minimax algorithm
def main():
    state = BoardUtils.get_starting_position_board()
    whites_turn = True
    
    while True:
        # Get user input for dice rolls
        d1, d2 = map(int, input().split())
        
        # Check if dice rolls are valid
        if d1 < 1 or d2 < 1 or d1 > 6 or d2 > 6:
            print("Try again with correct dice rolls")
            continue
        
        # Make optimal move using the Minimax algorithm
        state = make_optimal_move_1ply(state, d1, d2, whites_turn)
        
        # Toggle turn
        whites_turn = not whites_turn
        
        # Print the current state
        print(state)

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
