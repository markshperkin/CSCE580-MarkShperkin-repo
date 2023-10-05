#written by Mark Shperkin
class Responses:
    def __init__(self):
        self.intro = '''Backgammon is a classic board game that involves strategy, skill, and a bit of luck. Here's a step-by-step guide on how to play Backgammon:
        please tell me what do you want to know
        type: 
        Objective, Setup, Basic Rules, Hitting and Entering, Bearing Off, Winning, Doubling Cube.
        or just type: give me all the rules'''
        self.objective = '''The objective of Backgammon is to move all your checkers off the board before your opponent does, while also trying to block your opponent's progress.'''
        self.setup = '''Start with a Backgammon board, which consists of 24 narrow triangles or points, divided into four quadrants, with each quadrant having six points.
        Each player has 15 checkers (usually in two contrasting colors, like white and black) and places them on the board as follows:
        Two checkers on your 24-point.
        Five checkers on your 13-point.
        Three checkers on your 8-point.
        Five checkers on your 6-point.'''
        self.basicRules = '''Players take turns rolling two six-sided dice and move their checkers according to the numbers rolled.
        You can move a checker forward the number of spaces indicated on each die separately, or you can choose to move one checker the total number on both dice.
        You can only move to an open point (a point not occupied by two or more of your opponent's checkers).
        If you roll the same number on both dice, you get to move double the number. For example, rolling two 3s allows you to move four checkers forward 3 spaces each.
        You can "bear off" your checkers only when they are all in your home board (the last six points on your side of the board).
        To bear off, you need to roll a number that corresponds to the point where your checker is located. For example, if you have a checker on your 3-point, you need to roll a 3 to bear it off.
        If you roll a number that can't be legally moved (e.g., all your checkers are blocked, or you have no checkers on the higher-numbered points), you forfeit your turn.'''
        self.hittingAndEntering = '''If your opponent has a single checker on a point, you can land on that point, which sends your opponent's checker to the bar (the center of the board). They must re-enter that checker into their home board before making any other moves.
        To re-enter a checker, your roll must correspond to an open point in your home board. If you can't re-enter, you forfeit your turn.'''
        self.bearingOff = '''To bear off a checker, it must be in your home board, and you need to roll the exact number to remove it.
        You can bear off checkers from the higher-numbered points first if possible.
        If you have a checker on a higher point and roll a number higher than the highest checker, you must bear off a lower checker if possible.'''
        self.winning = '''The first player to bear off all their checkers wins the game.
        If one player bears off all their checkers while their opponent has checkers on the bar or in their home board, the game is a gammon and worth double the normal stakes.
        If one player bears off all their checkers while their opponent still has checkers in the player's home board or on the bar, it's a backgammon and worth triple the normal stakes.'''
        self.doublingCube = '''In more advanced games, players can use a doubling cube to increase the stakes of the game. A player may offer to double the current stake, and their opponent can either accept (in which case the game is played for double the current value) or decline (in which case they forfeit the current game, and the opponent wins the value of the cube).
        These are the basic rules of Backgammon. The game can become quite strategic as you gain experience, and there are many variations and strategies to explore. Enjoy playing Backgammon!'''
