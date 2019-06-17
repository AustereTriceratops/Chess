game_layount = {}   # row : list of pieces in that row

piece_alignments = {}   # row : alignment of all pieces in row  ( king race layout not supported )

common_pieces = {}   # piece_name : move_rule


class game():
    def __init__(self, layout):
        self.uniques = find_unique_pieces(layout)
        move_dict = find_moves_of_all_pieces(uniques)  # move_dict = { piece_name : moves }
        self.instantiate_pieces()
        self.main_board = board()
        pass

    def instantiate_pieces(self):
        pass

    def move_on_board(self, b, movement):  # b is a board, movement is in e2e4 format   # deals with special moves too
        pass

    def create_virtual_board(self, b, m):  # b is board and m is move
        if is_legal_move(b, m):
            result = deep_copy(b)
            self.move_on_board(result, m)
            return result
        else:
            raise Exception('attempting to make board from illegal move')

    def is_legal_move(self, b, m):
        pass


class board():
    def __init__(self):
        self.grid = [[piece(move_dict['__'])]*8 for _ in range(0,8)]
        self.turn_to_move = 'white'
        self.turns = 0


class piece():  # nothing more than data containers
    def __init__(self, piece_name, move_dict):
        self.name = piece_name
        self.moves = move_dict[self.name]
        self.alignment = None     # constant
        self.active = True        # variable
        self.location = location  # variable
        self.basis = None         # constant
        self.index = None         # constant
        self.times_moved = 0      # variable
        self.last_turn_moved = None
