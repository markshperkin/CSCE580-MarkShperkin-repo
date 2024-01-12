import json
import time
from random import randint

from board import Board
from colour import Colour
from strategies import Strategy
from move_not_possible_exception import MoveNotPossibleException

# Define a class named 'ReadOnlyBoard'
class ReadOnlyBoard:
    board: Board

    # Constructor to initialize the class with a board instance
    def __init__(self, board):
        self.board = board

    # Delegate all readonly method calls to the board
    def __getattr__(self, name):
        # If the requested attribute is a callable method in the board, delegate the call
        if hasattr(self.board, name) and callable(getattr(self.board, name)):
            return getattr(self.board, name)

        return super(ReadOnlyBoard, self).__getattr__(name)

    # Method to add many pieces, raising an exception to prevent modification
    def add_many_pieces(self, number_of_pieces, colour, location):
        self.__raise_exception__()

    # Method to move a piece, raising an exception to prevent modification
    def move_piece(self, piece, die_roll):
        self.__raise_exception__()

    # Helper method to raise an exception indicating direct board modification is not allowed
    def __raise_exception__(self):
        raise Exception("Do not try and change the board directly, use the make_move parameter instead")

# Define a class named 'Game'
class Game:
    # Constructor to initialize the game with white and black strategies, and the first player's color
    def __init__(self, white_strategy: Strategy, black_strategy: Strategy, first_player: Colour):
        self.board = Board.create_starting_board()
        self.first_player = first_player
        self.strategies = {
            Colour.WHITE: white_strategy,
            Colour.BLACK: black_strategy
        }

    # Method to run the game, taking optional verbosity parameter
    def run_game(self, verbose=True):
        # Print initial information if verbose is enabled
        if verbose:
            print('%s goes first' % self.first_player)
            self.board.print_board()
        i = self.first_player.value
        moves = []
        full_dice_roll = []

        # Main game loop
        while True:
            previous_dice_roll = full_dice_roll.copy()
            dice_roll = [randint(1, 6), randint(1, 6)]

            # Handle doubles by repeating the same roll four times
            if dice_roll[0] == dice_roll[1]:
                dice_roll = [dice_roll[0]] * 4
            full_dice_roll = dice_roll.copy()
            colour = Colour(i % 2)

            # Print the current player's roll if verbose is enabled
            if verbose:
                print("%s rolled %s" % (colour, dice_roll))

            # Define a function to handle the player's move
            def handle_move(location, die_roll):
                print(f"computer is trying to move {location} piece")
                rolls_to_move = self.get_rolls_to_move(location, die_roll, dice_roll)
                if len(dice_roll) >= 2:
                    print(f"{colour} rolled {dice_roll}")
                if rolls_to_move is None:
                    raise MoveNotPossibleException("You cannot move that piece %d" % die_roll)
                for roll in rolls_to_move:
                    piece = self.board.get_piece_at(location)
                    # original_location = location
                    location = self.board.move_piece(piece, roll)
                    dice_roll.remove(roll)
                    print(f"{colour} moved {roll} spaces from {location-roll} to {location}")

                    self.board.print_board()

                    # Record the move for later analysis
                    # moves.append({'start_location': original_location, 'die_roll': roll, 'end_location': location})
                    # previous_dice_roll.append(roll)
                print("Move successful!")

                return rolls_to_move

            # Snapshot the board state and dice roll before opponents move
            board_snapshot = self.board.to_json()
            dice_roll_snapshot = dice_roll.copy()

            opponents_moves = moves.copy()
            moves.clear()

            # Call the current player's move method from the strategy
            self.strategies[colour].move(
                ReadOnlyBoard(self.board),
                colour,
                dice_roll.copy(),
                lambda location, die_roll: handle_move(location, die_roll),
                {'dice_roll': previous_dice_roll, 'opponents_move': opponents_moves}
            )

            # Print a message if not all moves were made
            if verbose and len(dice_roll) > 0:
                print('FYI not all moves were made. %s playing %s did not move %s' % (
                    colour,
                    self.strategies[colour].__class__.__name__,
                    dice_roll))
                self.board.print_board()
                # Output the game state as JSON for debugging purposes
                state = {
                    'board': json.loads(board_snapshot),
                    'dice_roll': dice_roll_snapshot,
                    'colour_to_move': colour.__str__(),
                    'strategy': self.strategies[colour].__class__.__name__,
                }
                print(json.dumps(state))

            # Print the current board state if verbose is enabled
            if verbose:
                self.board.print_board()
            i = i + 1

            # Check if the game has ended
            if self.board.has_game_ended():
                if verbose:
                    print('%s has won!' % self.board.who_won())
                self.strategies[colour.other()].game_over({
                    'dice_roll': full_dice_roll,
                    'opponents_move': moves
                })
                break

    # Method to determine the rolls required to move a piece to a specific location
    def get_rolls_to_move(self, location, requested_move, available_rolls):
        # This first check ensures we return doing as little work as possible when the requested
        # move is exactly one of the die rolls (to ensure automated experiments don't run slower)
        if available_rolls.__contains__(requested_move):
            if self.board.is_move_possible(self.board.get_piece_at(location), requested_move):
                return [requested_move]
            return None
        if len(available_rolls) == 1:
            return None
        
        # Create a copy of the board for analysis
        board = self.board.create_copy()
        rolls_to_move = []
        current_location = location

        # If the first die roll isn't possible, reverse the dice before starting.
        # This ensures we cover all possible orderings (because doubles will always all be the same number)
        if not board.is_move_possible(board.get_piece_at(current_location), available_rolls[0]):
            available_rolls = available_rolls.copy()
            available_rolls.reverse()

        for roll in available_rolls:
            piece = board.get_piece_at(current_location)
            if not board.is_move_possible(piece, roll):
                break
            current_location = board.move_piece(piece, roll)
            rolls_to_move.append(roll)
            if sum(rolls_to_move) == requested_move:
                return rolls_to_move
        return None

    # Method to get the color of the player who started the game
    def who_started(self):
        return self.first_player

    # Method to get the color of the player who won the game
    def who_won(self):
        return self.board.who_won()
