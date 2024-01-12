class ReadOnlyBoard:
    board: 'Board'

    def __init__(self, board):
        self.board = board

    # Delegate all readonly method calls to the board
    def __getattr__(self, name):
        from board import Board  # Import inside the method
        if hasattr(self.board, name) and callable(getattr(self.board, name)):
            return getattr(self.board, name)

        return super(ReadOnlyBoard, self).__getattr__(name)
