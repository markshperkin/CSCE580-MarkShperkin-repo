from enum import Enum

# Define a custom Enum named 'Colour'
class Colour(Enum):
    # Define enum members with assigned integer values (WHITE = 0, BLACK = 1)
    WHITE = 0
    BLACK = 1

    # Define a method 'other()' that returns the opposite color
    def other(self):
        # If the current color is WHITE, return BLACK; otherwise, return WHITE
        if self == Colour.WHITE:
            return Colour.BLACK
        else:
            return Colour.WHITE

    # Define a string representation of the enum members
    def __str__(self):
        # If the current color is WHITE, return 'white'; otherwise, return 'black'
        if self == Colour.WHITE:
            return 'white'
        else:
            return 'black'

    # Define a static method 'load' to convert a string representation to a Colour enum
    @staticmethod
    def load(str):
        # Check the input string and return the corresponding Colour enum
        if str == 'black':
            return Colour.BLACK
        elif str == 'white':
            return Colour.WHITE
        else:
            # Raise an exception for an invalid color string
            raise Exception("%s is not a valid colour" % str)
