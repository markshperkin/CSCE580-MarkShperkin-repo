# Import necessary classes from the strategies, piece, and board modules
from strategies import Strategy
from piece import Piece


# Define a class CompareAllMoves that inherits from the Strategy class
class CompareAllMoves(Strategy):

    # Static method to get the difficulty level of the strategy
    @staticmethod
    def get_difficulty():
        return "Hard"

    # Method to assess the current board state and return relevant statistics
    def assess_board(self, colour, myboard):
        # Get all pieces of the specified colour on the board
        pieces = myboard.get_pieces(colour)
        # Count the number of pieces on the board
        pieces_on_board = len(pieces)
        sum_distances = 0
        number_of_singles = 0
        number_occupied_spaces = 0
        sum_single_distance_away_from_home = 0
        sum_distances_to_endzone = 0

        # Iterate over each piece to calculate various statistics
        for piece in pieces:
            # Calculate the sum of spaces each piece needs to reach home
            sum_distances = sum_distances + piece.spaces_to_home()
            if piece.spaces_to_home() > 6:
                # Calculate the sum of distances beyond the home zone
                sum_distances_to_endzone += piece.spaces_to_home() - 6

        # Iterate over each location on the board
        for location in range(1, 25):
            pieces = myboard.pieces_at(location)
            # Check if the space is occupied by the specified colour
            if len(pieces) != 0 and pieces[0].colour == colour:
                # Check if the space has a single piece
                if len(pieces) == 1:
                    number_of_singles = number_of_singles + 1
                    # Calculate the sum of distances for single pieces away from home
                    sum_single_distance_away_from_home += 25 - pieces[0].spaces_to_home()
                # Check if the space is occupied by multiple pieces
                elif len(pieces) > 1:
                    number_occupied_spaces = number_occupied_spaces + 1

        # Get the number of opponent's taken pieces
        opponents_taken_pieces = len(myboard.get_taken_pieces(colour.other()))
        # Get all pieces of the opponent's colour
        opponent_pieces = myboard.get_pieces(colour.other())
        sum_distances_opponent = 0

        # Calculate the sum of spaces each opponent's piece needs to reach home
        for piece in opponent_pieces:
            sum_distances_opponent = sum_distances_opponent + piece.spaces_to_home()

        # Return a dictionary containing the calculated statistics
        return {
            'number_occupied_spaces': number_occupied_spaces,
            'opponents_taken_pieces': opponents_taken_pieces,
            'sum_distances': sum_distances,
            'sum_distances_opponent': sum_distances_opponent,
            'number_of_singles': number_of_singles,
            'sum_single_distance_away_from_home': sum_single_distance_away_from_home,
            'pieces_on_board': pieces_on_board,
            'sum_distances_to_endzone': sum_distances_to_endzone,
        }

    # Method to make a move on the board based on assessed statistics
    def move(self, board, colour, dice_roll, make_move, opponents_activity):
        # Call the move_recursively method to get the best move
        result = self.move_recursively(board, colour, dice_roll)
        not_a_double = len(dice_roll) == 2

        # Check if it's not a double roll
        if not_a_double:
            new_dice_roll = dice_roll.copy()
            new_dice_roll.reverse()
            result_swapped = self.move_recursively(board, colour, dice_rolls=new_dice_roll)

            # Compare the result with the swapped dice rolls
            if result_swapped['best_value'] < result['best_value'] and \
                    len(result_swapped['best_moves']) >= len(result['best_moves']):
                result = result_swapped

        # Check if there are best moves to make
        if len(result['best_moves']) != 0:
            for move in result['best_moves']:
                make_move(move['piece_at'], move['die_roll'])

    # Method to recursively explore possible moves and find the best move
    def move_recursively(self, board, colour, dice_rolls):
        best_board_value = float('inf')
        best_pieces_to_move = []

        # Get unique piece locations to try
        pieces_to_try = [x.location for x in board.get_pieces(colour)]
        pieces_to_try = list(set(pieces_to_try))

        valid_pieces = []
        for piece_location in pieces_to_try:
            valid_pieces.append(board.get_piece_at(piece_location))

        # Sort valid pieces by spaces_to_home in descending order
        valid_pieces.sort(key=Piece.spaces_to_home, reverse=True)

        # Get the first die roll
        dice_rolls_left = dice_rolls.copy()
        die_roll = dice_rolls_left.pop(0)

        # Iterate over valid pieces and explore possible moves
        for piece in valid_pieces:
            if board.is_move_possible(piece, die_roll):
                board_copy = board.create_copy()
                new_piece = board_copy.get_piece_at(piece.location)
                board_copy.move_piece(new_piece, die_roll)

                # Check if there are remaining dice rolls
                if len(dice_rolls_left) > 0:
                    result = self.move_recursively(board_copy, colour, dice_rolls_left)

                    # If no more best moves can be found, evaluate the current board
                    if len(result['best_moves']) == 0:
                        board_value = self.evaluate_board(board_copy, colour)
                        if board_value < best_board_value and len(best_pieces_to_move) < 2:
                            best_board_value = board_value
                            best_pieces_to_move = [{'die_roll': die_roll, 'piece_at': piece.location}]
                    # If more best moves are found, consider them in the evaluation
                    elif result['best_value'] < best_board_value:
                        new_best_moves_length = len(result['best_moves']) + 1
                        if new_best_moves_length >= len(best_pieces_to_move):
                            best_board_value = result['best_value']
                            move = {'die_roll': die_roll, 'piece_at': piece.location}
                            best_pieces_to_move = [move] + result['best_moves']
                else:
                    # Evaluate the current board if there are no more dice rolls
                    board_value = self.evaluate_board(board_copy, colour)
                    if board_value < best_board_value and len(best_pieces_to_move) < 2:
                        best_board_value = board_value
                        best_pieces_to_move = [{'die_roll': die_roll, 'piece_at': piece.location}]

        # Return the best move information
        return {'best_value': best_board_value,
                'best_moves': best_pieces_to_move}


# Define a subclass CompareAllMovesSimple that inherits from CompareAllMoves
class CompareAllMovesSimple(CompareAllMoves):

    # Method to evaluate the board based on simple criteria
    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        # Simple evaluation function based on calculated statistics
        board_value = board_stats['sum_distances'] + 2 * board_stats['number_of_singles'] - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces']
        return board_value


# Define a subclass CompareAllMovesWeightingDistance that inherits from CompareAllMoves
class CompareAllMovesWeightingDistance(CompareAllMoves):

    # Method to evaluate the board with a weight on distances
    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        # Evaluation function with a weight on distances
        board_value = board_stats['sum_distances'] - float(board_stats['sum_distances_opponent']) / 3 + \
                      2 * board_stats['number_of_singles'] - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces']
        return board_value


# Define a subclass CompareAllMovesWeightingDistanceAndSingles that inherits from CompareAllMoves
class CompareAllMovesWeightingDistanceAndSingles(CompareAllMoves):

    # Method to evaluate the board with weights on distances and singles
    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        # Evaluation function with weights on distances and singles
        board_value = board_stats['sum_distances'] - float(board_stats['sum_distances_opponent']) / 3 + \
                      float(board_stats['sum_single_distance_away_from_home']) / 6 - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces']
        return board_value


# Define a subclass CompareAllMovesWeightingDistanceAndSinglesWithEndGame that inherits from CompareAllMoves
class CompareAllMovesWeightingDistanceAndSinglesWithEndGame(CompareAllMoves):

    # Method to evaluate the board with weights on distances, singles, and endgame considerations
    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        # Evaluation function with weights on distances, singles, and endgame considerations
        board_value = board_stats['sum_distances'] - float(board_stats['sum_distances_opponent']) / 3 + \
                      float(board_stats['sum_single_distance_away_from_home']) / 6 - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces'] + \
                      3 * board_stats['pieces_on_board']

        return board_value


# Define a subclass CompareAllMovesWeightingDistanceAndSinglesWithEndGame2 that inherits from CompareAllMoves
class CompareAllMovesWeightingDistanceAndSinglesWithEndGame2(CompareAllMoves):

    # Method to evaluate the board with weights on distances, singles, endgame, and endzone considerations
    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        # Evaluation function with weights on distances, singles, endgame, and endzone considerations
        board_value = board_stats['sum_distances'] - float(board_stats['sum_distances_opponent']) / 3 + \
                      float(board_stats['sum_single_distance_away_from_home']) / 6 - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces'] + \
                      3 * board_stats['pieces_on_board'] + float(board_stats['sum_distances_to_endzone']) / 6

        return board_value
