
from random import randint
from colour import Colour
from board import Board
from game import Game
from strategy_factory import StrategyFactory
from strategies import HumanStrategy

if __name__ == '__main__':
    userInput = input("press c for compare option\nor press enter")
    if userInput == 'c':
        print("Available Strategies:")
        strategies = [x for x in StrategyFactory.get_all() if x.__name__ != HumanStrategy.__name__]
        for i, strategy in enumerate(strategies):
            print("[%d] %s (%s)" % (i, strategy.__name__, strategy.get_difficulty()))

        strategy_index1 = int(input('Pick a strategy for player number one\n'))
        strategy_index2 = int(input('Pick a strategy for player number two\n'))

        chosen_strategy_one = StrategyFactory.create_by_name(strategies[strategy_index1].__name__)
        chosen_strategy_two = StrategyFactory.create_by_name(strategies[strategy_index2].__name__)

        numGames = int(input("Enter the number of games: "))
        strategyOne = 0
        strategyTwo = 0

        for _ in range(numGames):  # Use range to iterate the specified number of times
            # Create a new game for each iteration
            game = Game(
                black_strategy=chosen_strategy_one,
                white_strategy=chosen_strategy_two,
                first_player=Colour(randint(0, 1))
            )

            # Run the game
            game.run_game(verbose=False)
            
            # Update the win counts based on the game result
            if game.who_won() == Colour.BLACK:
                strategyOne += 1
            elif game.who_won() == Colour.WHITE:
                strategyTwo += 1
            print("%s won!" % game.who_won())


        print(f"Strategy {chosen_strategy_one.__class__.__name__} won {strategyOne} times")
        print(f"Strategy {chosen_strategy_two.__class__.__name__} won {strategyTwo} times")


    else:
        name = input('What is your name?\n')

        print("Available Strategies:")
        strategies = [x for x in StrategyFactory.get_all() if x.__name__ != HumanStrategy.__name__]
        for i, strategy in enumerate(strategies):
            print("[%d] %s (%s)" % (i, strategy.__name__, strategy.get_difficulty()))

        strategy_index = int(input('Pick a strategy:\n'))

        chosen_strategy = StrategyFactory.create_by_name(strategies[strategy_index].__name__)

        game = Game(
            # black_strategy=HumanStrategy(name),
            # white_strategy=chosen_strategy,
            
            black_strategy=chosen_strategy,
            white_strategy=HumanStrategy(name),
            
            # first_player=Colour(randint(0, 1))
            first_player=Colour.BLACK  #computer starts
        )

        game.run_game(verbose=False)

        print("%s won!" % game.who_won())
        game.board.print_board()
