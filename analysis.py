import chess


# ======= constants ==========
pieces = [i for i in range(1,7)]
piece_counter = {i: 0 for i in pieces}


# ====== functions ===========

def piece_mobility(_board, pieceType, color=True):
    board = _board.copy()
    max_mobilities = {1: 3, 2: 8, 3: 12, 4: 14, 5: 26, 6: 8}
    squares = list(board.pieces(pieceType, color))
    
    if len(squares) == 0:
        return 0
    
    m_max = max_mobilities[pieceType] * len(squares)
    m = 0
    
    if board.turn is not color:
        board.push(chess.Move.null())
        
    for move in list(board.legal_moves):
        for sq in squares:
            if move.from_square == sq:
                m += 1
    
    return m / m_max


def pieces_attacked_by(_board, sq):  # change to take board as an argument
    attacked_squares = list(_board.attacks(sq))
    pieces_sq_attacking = piece_counter.copy()

    for square in attacked_squares:
        piece = _board.piece_type_at(square)
        if _board.color_at(square) != _board.color_at(sq) and piece:
            pieces_sq_attacking[piece] += 1

    return pieces_sq_attacking 


def pieces_defended_by(_board, sq):
    attacked_squares = list(_board.attacks(sq))
    pieces_sq_attacking = piece_counter.copy()

    for square in attacked_squares:
        piece = _board.piece_type_at(square)
        if _board.color_at(square) == _board.color_at(sq) and piece:
            pieces_sq_attacking[piece] += 1

    return pieces_sq_attacking 


def pieces_x_rayed_by(_board, sq):
    piece_type = str(_board.piece_at(sq))
    pieces_sq_x_raying = piece_counter.copy()
    color = _board.color_at(sq)
    x = sq % 8
    
    # === rook moves ===
    if piece_type == "R" or piece_type == "Q":
        s = 0
        for i in range(sq-1, sq-x-1, -1):  # want to go from sq to sq-x
            other_piece_type = _board.piece_type_at(i)
            
            if s > 0 and other_piece_type:
                pieces_sq_x_raying[other_piece_type] += 1
            elif other_piece_type: # true when square is nonempty
                s += 1
            
        s = 0
        for i in range(sq +1, sq - x + 8):
            other_piece_type = _board.piece_type_at(i)
            
            if s > 0 and other_piece_type:
                pieces_sq_x_raying[other_piece_type] += 1
            elif other_piece_type: 
                s += 1
                
        s = 0
        for i in range(sq + 8, 64, 8): 
            other_piece_type = _board.piece_type_at(i)
            
            if s > 0 and other_piece_type:
                pieces_sq_x_raying[other_piece_type] += 1
            elif other_piece_type: 
                s += 1
            
        s = 0
        for i in range(sq -8, -1, -8):
            other_piece_type = _board.piece_type_at(i)
            
            if s > 0 and other_piece_type:
                pieces_sq_x_raying[other_piece_type] += 1
            elif other_piece_type: 
                s += 1
    
    # === bishop moves ===
    if piece_type == "B" or piece_type == "Q":
        s = 0
        for i in range(sq+7, 64, 7): 
            if i % 8 == 7:  # don't let diagonal escape edge and wrap around board
                break
            
            other_piece_type = _board.piece_type_at(i)
            
            if s > 0 and other_piece_type:
                pieces_sq_x_raying[other_piece_type] += 1
            elif other_piece_type: 
                s += 1
            
                
        s = 0
        for i in range(sq-7, -1, -7): 
            if i % 8 == 0:
                break
                
            other_piece_type = _board.piece_type_at(i)
            
            if s > 0 and other_piece_type:
                pieces_sq_x_raying[other_piece_type] += 1
            elif other_piece_type: 
                s += 1
                
        s = 0
        for i in range(sq+9, 64, 9): 
            if i % 8 == 0:  
                break
            
            other_piece_type = _board.piece_type_at(i)
            
            if s > 0 and other_piece_type:
                pieces_sq_x_raying[other_piece_type] += 1
            elif other_piece_type: 
                s += 1
            
                
        s = 0
        for i in range(sq-9, -1, -9): 
            if i % 8 == 7:
                break
                
            other_piece_type = _board.piece_type_at(i)
            
            if s > 0 and other_piece_type:
                pieces_sq_x_raying[other_piece_type] += 1
            elif other_piece_type: 
                s += 1
            
        
    return pieces_sq_x_raying