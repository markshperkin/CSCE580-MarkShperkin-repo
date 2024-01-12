# Import necessary classes from the strategies and board modules
from random import randint
from strategies import Strategy
from board import ReadOnlyBoard
from piece import Colour, Piece


# Define a class MinMaxStrategy that inherits from the Strategy class
class MinMaxStrategy(Strategy):
    # Constructor method for initializing the MinMaxStrategy object with a specified depth
    def __init__(self, depth=1):
        self.depth = depth

    # Static method to get the difficulty level of the strategy
    @staticmethod
    def get_difficulty():
        return "Super hard"

    # Implementation of the move method required by the parent Strategy class
    def move(self, board, colour, dice_roll, make_move, opponents_activity):
        # Create a read-only version of the board for Minimax computation

        read_only_board = ReadOnlyBoard(board)
        
        # Find the best move using Minimax
        # Make the best move on the actual board for each die roll
        print("dice roll is:")
        print(dice_roll)
        # Find the best move using Minimax
        best_moves = self.minimax(read_only_board, colour, dice_roll, self.depth)
        print("this is the final best move:")
        print(best_moves)

            # Access the 'possible_moves' field
        try:
            possible_moves = best_moves.get('possible_moves', [])
        except AttributeError as e:
            print("there is only one move or none")
            # Define the move logic
        if best_moves == None:
            return
        elif len(best_moves) == 1:
            single_move = best_moves[0]
            piece_at = single_move.get('piece_at')
            roll_at = single_move.get('die_roll')
            if piece_at:
                make_move(piece_at, roll_at)
        elif possible_moves == None:
            return
        else:
            for move in possible_moves:
                print("printing move and board that about to move")
                board.print_board()
                print(move)
                piece_at = move.get('piece_at')
                roll_at = move.get('die_roll')
                if piece_at:
                    make_move(piece_at, roll_at)
        # self.make_moves(best_moves)
        # dice_amount = len(dice_roll)
        # if len(best_moves['possible_moves']) == 1:
        #     possible_move = best_moves['possible_moves'][0]
        #     if possible_move:
        #         piece_at = possible_move.get('piece_at')
        #         roll_at = possible_move.get('die_roll')
        #         if piece_at:
        #             make_move(piece_at, roll_at)

        # else:
        #     for i in range(dice_amount):
        #         possible_moves = best_moves.get('possible_moves', [i])
        #         selected_move = possible_moves[i]

        #         if selected_move:
        #             piece_at = selected_move.get('piece_at')
        #             roll_at = selected_move.get('die_roll')
        #             if piece_at:
        #                 make_move(piece_at, roll_at)

    # Implementation of the Minimax algorithm to find the best move
    def minimax(self, board, colour, dice_roll, depth):
        if depth == 0 or board.has_game_ended():
            return {'value': self.evaluate_board(board, colour), 'possible_moves': []}
        
        current_board_state = board.get_board()
        result = self.get_state(current_board_state)
        print(result)
        valid_moves = self.get_possible_moves(board, colour, dice_roll)
        print("valid moves are:")
        print(valid_moves)
        
        if not valid_moves:
            print(f"No valid moves for {colour}. Skipping turn.")
            return  # Skip to the next player's turn        

        # breakpoint()
        if not valid_moves:
            # No valid moves, return a dummy move
            return {'value': 0, 'possible_moves': []}
        
        best_moves_combo = self.evaluate_moves(valid_moves, board, colour, result, dice_roll)
        # go through moves
        # new_board = board.create_copy()
        # moves = best_moves_combo['possible_moves']
        # for move in moves:
        #     piece_at = move['piece_at']
        #     piece_at = new_board.get_piece_at(piece_at)
        #     die = move['die_roll']
        #     new_board.move_piece(piece_at, die)
        # random_dice_rolls = [randint(1, 6), randint(1, 6)]
        # assumed_moves = self.get_possible_moves(new_board, colour.other, random_dice_rolls)
        # opponents_best_moves_combo = self.evaluate_moves(assumed_moves, new_board, colour, result, random_dice_rolls)
        # moves = opponents_best_moves_combo['possible_moves']
        # print("test")
        # print(moves)
        # for move in moves:
        #     piece_at = move['piece_at']
        #     piece_at = new_board.get_piece_at(piece_at)
        #     die = move['die_roll']
        #     new_board.move_piece(piece_at, die)
        # self.minimax(new_board, colour, dice_roll, depth-1)
        print("best move combo")
        print(best_moves_combo)
        return best_moves_combo
    
    def evaluate_move(self, move, board, colour, state):
    # Evaluate the move based on its impact on the overall board state
    # You can customize this function for a more sophisticated evaluation
        try:
            new_board = board.create_copy()
            new_piece = new_board.get_piece_at(move['piece_at'])
            new_board.move_piece(new_piece, move['die_roll'])
            score = move['die_roll']
        # Check if the move makes a vulnerable piece (count changes from 1 to 2)
            new_location = move['piece_at'] - move['die_roll']   #todo add one for white player
            old_location = move['piece_at']
            num = board.pieces_at(new_location)
            num2 = new_board.pieces_at(new_location)
            old_location = board.pieces_at(old_location)
            old_location = len(old_location)
            num = len(num)
            num2 = len(num2)
            if num == 1 and num2 == 2 and old_location != 2:
                score += 100
            # check if move captured opponent
            old_board = board.create_copy()
            try:
                piece_at_location = old_board.get_piece_at(new_location)
                if piece_at_location.get_colour() == Colour.WHITE:
                    # print("testing loop")
            # Check if there is only one piece at the location
                    if len(old_board.pieces_at(new_location)) == 1:
                        # print("testing inside loop")
                        score += 200
            except AttributeError as e:
                # Handle the AttributeError (e.g., print an error message)
                print(f"AttributeError: {e}")
        except AttributeError as e:
            print("moves number is lower than expected")
            return 0
        return score
    
    def evaluate_moves(self, moves, board, colour, state, dice_roll):
        random_dice_rolls = [randint(1, 6), randint(1, 6)]
        best_move1 = None
        best_move2 = None
        best_move3 = None
        best_move4 = None
        best_moves = {'value': 0, 'possible_moves': []}
        if len(moves) == 1:
            return moves
        elif len(dice_roll) == 2:
            # best_move1 = 0
            # best_move2 = 0
            for move1 in moves:
                if move1['die_roll'] == dice_roll[0]:
                    print("outer loop: checking this move:")
                    print(move1)
                    first_score = self.evaluate_move(move1, board, colour, state)
                    new_board = board.create_copy()
                    # best_piece = best_moves['possible_moves'][0]
                    piece_at = move1['piece_at']    #line 199
                    die = move1['die_roll']
                    piece_at = new_board.get_piece_at(piece_at)
                    new_board.move_piece(piece_at, die)
                    print("testing first")
                    new_board.print_board()
                    moves = self.get_possible_moves(new_board, colour, dice_roll[1])
                for move2 in moves:
                    # if move2['die_roll'] == dice_roll[1]:
                        print("inner loop: checking this move:")
                        print(move2)
                        second_score = self.evaluate_move(move2, new_board, colour, state)
                        
                        # temp_moves = [move1, move2]


                        # piece_at = move2['piece_at']
                        # # piece_at = new_board.get_piece_at(piece_at)
                        # die = move2['die_roll']
                        # print("testing")
                        # print(piece_at)
                        # print(move2)
                        # new_board.print_board()
                        # new_board.move_piece(piece_at, die)
                            
                        # assumed_moves = self.get_possible_moves(new_board, colour.other, random_dice_rolls)
                        # opponents_best_moves = self.evaluate_opponents_moves(assumed_moves, new_board, colour.other, state, random_dice_rolls)
                        
                        # print("testing opponents moves in 2 loop:")
                        # print(assumed_moves)
                        # print(opponents_best_moves)
                        
                        # moves = opponents_best_moves['possible_moves']
                        # for move in moves:
                        #     piece_at = move['piece_at']
                        #     piece_at = new_board.get_piece_at(piece_at)
                        #     die = move['die_roll']
                        #     new_board.move_piece(piece_at, die) 
                        # opponents_score = opponents_best_moves['value']
                        
                        # final_score = first_score + second_score - opponents_score
                        final_score = first_score + second_score

                        
                        if final_score > best_moves['value']:  # check if move value is bigger than best move and update if so
                            print("new best score and move in inner loop:")
                            best_moves['value'] = final_score                       
                            print(move1)
                            print(move2)
                            print(final_score)
                            best_moves['possible_moves'] = [move1, move2]
                            
                            
                            
        elif len(dice_roll) == 4:
            final_score = 0
            for move1 in moves:
                print("first loop: checking this move:")
                print(move1)
                first_score = self.evaluate_move(move1, board, colour, state)
                new_board = board.create_copy()
                # best_piece = best_moves['possible_moves'][0]
                piece_at = move1['piece_at']    #line 199
                die = move1['die_roll']
                piece_at = new_board.get_piece_at(piece_at)
                new_board.move_piece(piece_at, die)
                new_board.print_board()
                # dice_roll.pop(0)
                moves2 = self.get_possible_moves(new_board, colour, dice_roll)
                print("printing moves after first evaluation")
                print(moves2)
                for move2 in moves2:
                    
                    print("second loop: checking this move:")
                    print(move2)
                    second_score = self.evaluate_move(move2, new_board, colour, state)
                    # best_piece = best_moves['possible_moves'][0]
                    piece_at = move2['piece_at']
                    piece_at = new_board.get_piece_at(piece_at)
                    print("test")
                    print(move2)
                    print(piece_at)
                    new_board.move_piece(piece_at, die)
                    new_board.print_board()
                    # dice_roll.pop(0)
                    moves = self.get_possible_moves(new_board, colour, dice_roll)
                    print("printing moves after second evaluation")
                    print(moves)
                    for move3 in moves:
                        print("third loop: checking this move:")
                        print(move3)
                        third_score = self.evaluate_move(move3, new_board, colour, state)
                        # best_piece = best_moves['possible_moves'][0]
                        piece_at = move3['piece_at']    #line 199
                        piece_at = new_board.get_piece_at(piece_at)
                        new_board.move_piece(piece_at, die)
                        # dice_roll.pop(0)
                        new_board.print_board()
                        moves = self.get_possible_moves(new_board, colour, dice_roll)
                        print("printing moves after third evaluation")
                        print(moves)
                        for move4 in moves:
                            print("fouroth and final loop: checking this move:")
                            print(move4)
                            fourth_score = self.evaluate_move(move4, new_board, colour, state)
                            

                            # piece_at = move4['piece_at']
                            # piece_at = new_board.get_piece_at(piece_at)
                            # die = move4['die_roll']
                            # new_board.move_piece(piece_at, die)
                            # assumed_moves = self.get_possible_moves(new_board, colour.other, random_dice_rolls)
                            # print("testing opponents moves in 4 loop:")
                            # print(assumed_moves)
                            # opponents_best_moves = self.evaluate_opponents_moves(assumed_moves, new_board, colour.other, state, random_dice_rolls)
                            # print(opponents_best_moves)
                            # moves = opponents_best_moves['possible_moves']
                            # for move in moves:
                            #     piece_at = move['piece_at']
                            #     piece_at = new_board.get_piece_at(piece_at)
                            #     die = move['die_roll']
                            #     new_board.move_piece(piece_at, die) 
                            # opponents_score = opponents_best_moves['value']
                            
                            # final_score = first_score + second_score + third_score + fourth_score - opponents_score
                            final_score = first_score + second_score + third_score + fourth_score
                            print("this is final score")
                            print(final_score)
                            print("this is best moves score:")
                            print(best_moves['value'])
                            if final_score > best_moves['value']:  # check if move value is bigger than best move and update if so
                                print("new best score and move in inner loop:")
                                best_moves['value'] = final_score                  
                                print(move1)
                                print(move2)
                                print(move3)
                                print(move4)
                                print(final_score)
                                best_moves['possible_moves'] = [move1, move2, move3, move4]
                                board.print_board()
                                breakpoint()
        
        print("best moves are after evaluation:")
        print(best_moves)
        return best_moves
        
            
    def evaluate_opponents_moves(self, moves, board, colour, state, dice_roll):
        print("opponents dice roll:")
        print(dice_roll)
        best_moves = {'value': float('-inf'), 'possible_moves': []}
        if len(dice_roll) == 2:
            # best_move1 = 0
            # best_move2 = 0
            for move1 in moves:
                if move1['die_roll'] == dice_roll[0]:
                    print("outer loop: checking this move:")
                    print(move1)
                    first_score = self.evaluate_move(move1, board, colour, state)
                    new_board = board.create_copy()
                    # best_piece = best_moves['possible_moves'][0]
                    piece_at = move1['piece_at']    #line 199
                    die = move1['die_roll']
                    piece_at = new_board.get_piece_at(piece_at)
                    new_board.move_piece(piece_at, die)
                for move2 in moves:
                    if move2['die_roll'] == dice_roll[1]:
                        print("inner loop: checking this move:")
                        print(move2)
                        second_score = self.evaluate_move(move2, new_board, colour, state)
                        final_score = first_score + second_score
                        if final_score > best_moves['value']:  # check if move value is bigger than best move and update if so
                            print("new best score and move in inner loop:")
                            best_moves['value'] = final_score
                            best_move1 = move1
                            best_move2 = move2                        
                            print(move1)
                            print(move2)
                            print(final_score)

                            best_moves['possible_moves'].append(best_move1)
                            best_moves['possible_moves'].append(best_move2)
                            
                            moves = best_moves['possible_moves']
                            for move in moves:
                                piece_at = move['piece_at']
                                piece_at = new_board.get_piece_at(piece_at)
                                die = move['die_roll']
                                new_board.move_piece(piece_at, die)
                            random_dice_rolls = [randint(1, 6), randint(1, 6)]
                            assumed_moves = self.get_possible_moves(new_board, colour.other, random_dice_rolls)
                            opponents_best_moves = self.evaluate_moves(assumed_moves, new_board, colour, state, random_dice_rolls)
                            moves = opponents_best_moves['possible_moves']
                            for move in moves:
                                piece_at = move['piece_at']
                                piece_at = new_board.get_piece_at(piece_at)
                                die = move['die_roll']
                                new_board.move_piece(piece_at, die)
                            
                            
        if len(dice_roll) == 4:
            for move1 in moves:
                print("first loop: checking this move:")
                print(move1)
                first_score = self.evaluate_move(move1, board, colour, state)
                new_board = board.create_copy()
                # best_piece = best_moves['possible_moves'][0]
                piece_at = move1['piece_at']    #line 199
                die = move1['die_roll']
                piece_at = new_board.get_piece_at(piece_at)
                new_board.move_piece(piece_at, die)
                # dice_roll.pop(0)
                moves = self.get_possible_moves(new_board, colour, dice_roll)
                for move2 in moves:
                    print("second loop: checking this move:")
                    print(move2)
                    second_score = self.evaluate_move(move2, new_board, colour, state)
                    # best_piece = best_moves['possible_moves'][0]
                    piece_at = move2['piece_at']    #line 199
                    piece_at = new_board.get_piece_at(piece_at)
                    new_board.move_piece(piece_at, die)
                    # dice_roll.pop(0)
                    moves = self.get_possible_moves(new_board, colour, dice_roll)
                    for move3 in moves:
                        print("third loop: checking this move:")
                        print(move3)
                        third_score = self.evaluate_move(move3, new_board, colour, state)
                        # best_piece = best_moves['possible_moves'][0]
                        piece_at = move3['piece_at']    #line 199
                        piece_at = new_board.get_piece_at(piece_at)
                        new_board.move_piece(piece_at, die)
                        # dice_roll.pop(0)
                        moves = self.get_possible_moves(new_board, colour, dice_roll)
                        for move4 in moves:
                            print("fourth and final loop: checking this move:")
                            print(move4)
                            fourth_score = self.evaluate_move(move4, new_board, colour, state)
                            final_score = first_score + second_score + third_score + fourth_score
                            if final_score > best_moves['value']:  # check if move value is bigger than best move and update if so
                                print("new best score and move in inner loop:")
                                best_moves['value'] = final_score
                                best_move1 = move1
                                best_move2 = move2    
                                best_move3 = move3
                                best_move4 = move4                    
                                print(move1)
                                print(move2)
                                print(move3)
                                print(move4)
                                print(final_score)
                                best_moves['possible_moves'].append(best_move1)
                                best_moves['possible_moves'].append(best_move2)
                                best_moves['possible_moves'].append(best_move3)
                                best_moves['possible_moves'].append(best_move4)
        print("best opponents moves are after evaluation:")
        print(best_moves)
        return best_moves

        
    
    # def safe_chance(self, board, piece, colour):
    #     new_board = board.create_copy()
    #     for d1 in range(1, 7):
    #         for d2 in range(1, 7):
    #             moves = self.get_possible_moves(new_board, colour.other, (d1,d2))
    #             for move in moves:
    #                 if is #not done
    
    # def is_safe(self, board, piece, colour):
    #     if #need to implement
    #     return True
    
    # def is_safe(self, board, piece, colour):
    #     if 
    #     return True


    # Evaluation function that determins the distance of all pieces from home of each color
    def evaluate_board(self, board, colour):
        total_distance = 0
        pieces = board.get_pieces(colour)
        for piece in pieces:
            piece_distance = piece.spaces_to_home()
            total_distance += piece_distance
        return total_distance

        
            

    # Get all possible moves for a player given the current board state and dice roll

    def get_possible_moves(self, board, colour, dice_roll):
        moves = []
        pieces = board.get_pieces(colour)
        print("testing")
        print(dice_roll)
        if isinstance(dice_roll, int):
            for piece in pieces:
                if any(move['piece_at'] == piece.location and move['die_roll'] == dice_roll for move in moves):
                    continue
                if board.is_move_possible(piece, dice_roll):
                        moves.append({'piece_at': piece.location, 'die_roll': dice_roll})
        else:
            for die_roll in dice_roll:
                for piece in pieces:
                    if any(move['piece_at'] == piece.location and move['die_roll'] == die_roll for move in moves):
                        continue
                    if board.is_move_possible(piece, die_roll):
                            moves.append({'piece_at': piece.location, 'die_roll': die_roll})
        return moves
    
    def get_state(self, board):
        if board.get(24, {}).get('count', 0) == 2 and board.get(13, {}).get('count', 0) == 5 \
                and board.get(8, {}).get('count', 0) == 3 and board.get(6, {}).get('count', 0) == 5:
            return "first_turn"
        elif board.get(25, {}).get('count', 0) > 0:
            return "computer_in_bar"
        elif board.get(0, {}).get('count', 0) > 0:
            return "opponent_in_bar"
        # elif self.helper_to_opponent_stuck_behind(board):
        #     return "opponent_stuck_behind"
        # elif self.helper_to_computer_stuck_behind(board):
        #     return "computer_stuck_behind"
        # elif self.helper_to_dice_game_state(board):
        #     print("dice state has choosen")
        #     return "dice_game"
        else:
            return "mid_game"

    def helper_to_opponent_stuck_behind(self, board):
        for i in range(1, 5):
            if board[i].get('count', 0) >= 1 and board[i].get('colour') == 'white':
                for j in range(2, 12):
                    print("testing")
                    if board.get(j, {}).get('count', 0) >= 2 and \
                    board.get(j + 1, {}).get('count', 0) >= 2 and \
                    board.get(j + 2, {}).get('count', 0) >= 2 and \
                    board.get(j + 3, {}).get('count', 0) >= 2 and \
                    board.get(j, {}).get('colour') == 'black' and \
                    board.get(j + 1, {}).get('colour') == 'black' and \
                    board.get(j + 2, {}).get('colour') == 'black' and \
                    board.get(j + 3, {}).get('colour') == 'black':
                        return True
        return False


    def helper_to_computer_stuck_behind(self, board):
        for i in range(20, 24):
            if board[i].get('count', 0) >= 1 and board[i].get('colour') == 'black':
                for j in range(13, 23):
                    if board.get(j, {}).get('count', 0) >= 2 and \
                    board.get(j + 1, {}).get('count', 0) >= 2 and \
                    board.get(j + 2, {}).get('count', 0) >= 2 and \
                    board.get(j + 3, {}).get('count', 0) >= 2 and \
                    board.get(j, {}).get('colour') == 'white' and \
                    board.get(j + 1, {}).get('colour') == 'white' and \
                    board.get(j + 2, {}).get('colour') == 'white' and \
                    board.get(j + 3, {}).get('colour') == 'white':
                        return True
        return False

            
    def helper_to_dice_game_state(self, board):
        # Check if the computer has moved its pieces away from the opponent
        computer_positions = set(piece.location for piece in board.get_pieces(Colour.BLACK))
        opponent_positions = set(piece.location for piece in board.get_pieces(Colour.WHITE))

        # Check if there is no overlap between computer and opponent positions
        if not any(position in opponent_positions for position in computer_positions):
            return True  # Dice game state reached
        else:
            return False



