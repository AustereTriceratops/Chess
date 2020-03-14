'''

Takes a game in Smith notation and renders it using hte board object.
Right now this doesn't support castling or en passant.

'''

from Chess import game

translate = {
                'a': 0,
                'b': 1,
                'c': 2,
                'd': 3,
                'e': 4,
                'f': 5,
                'g': 6,
                'h': 7,
}

finished_game = '1. d2d4 g8f6    2. c1g5   f6e4 3. g5f4 b8c6'   # Smith notation


# =================== Functions =========================


def remove_spacing(game):
    g = game.split('.')   # removes periods
    size = len(g)
    g2 = []
    for i in range(0, size):      # removes spaces
        g2.append(g[i].split(' '))
        g[i] = g2[i]

    for i in range(0,size):  # removes empty strings
        g[i] = clean(g[i])

    r = []
    for i in range(1, size):  # group turns together
        r.append(g[i][0:2])
    return r


def clean(l):
    r = []
    for member in l:
        if member != '':
            r.append(member)
    return r


def translate_atom(atom):
    square = [translate[atom[0]], int(atom[1]) - 1]
    return square


def to_moves(p):
    max = len(p)
    result = []
    for i in range(0,max):
        for j in range(0,2):
            turn_1 = p[i][j][0:2]
            turn_2 = p[i][j][2:4]
            h = [translate_atom(turn_1), translate_atom(turn_2)]
            result.append(h)
    return result


def decode_game(game):
    parsed = remove_spacing(game)
    result = to_moves(parsed)
    return result


def show_game(smith_notation):   # takes a game in Smith notation and renders it using the board object
    moves = decode_game(smith_notation)
    b = game()
    for i in moves:
        b.move(i[0], i[1])

# ============================================


show_game(finished_game)
