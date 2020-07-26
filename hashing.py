import random as r


zobrist_keys = [[r.randint(1, 2**64 - 1) for _ in range(12)] for _ in range(64)]


def hash_board(board):  # chess.Boars
    key = 0

    for i in range(64):
        if board.color_at(i) is not None:
            ind = board.piece_type_at(i) + 6 * board.color_at(i) - 1  #abuse of type coercion
            key ^= zobrist_keys[i][ind]
            
    return key


def rehash(h_0, board, move):  # pre-move board, chess.Move
    newhash = h_0
    from_sq = move.from_square
    to_sq = move.to_square
    ind = board.piece_type_at(from_sq) + 6 * board.color_at(from_sq) - 1
    
    if ind in [5, 11] and from_sq in [4, 60]:
        newhash = hash_board(board)
        return newhash 
    
    newhash ^= zobrist_keys[from_sq][ind]
    newhash ^= zobrist_keys[to_sq][ind]
    return newhash