from evaluate import evaluate
from hashing import *


class Node():
    def __init__(self, board, parent=None, **data):
        self.parent = parent
        self.board = board.copy()
        self.children = []
        self.data = data

    def create_children(self, variation_func):  # variation_func should be Node -> Node[]
        self.children = variation_func(self)

    def function_on_leaves(self, func, *args, **kwargs):
        if not self.children:
            func(self, *args, **kwargs)
        else:
            for child in self.children:
                child.function_on_leaves(func, *args, **kwargs)

    def function_on_tree(self, func, *args, **kwargs):
        func(self, *args, **kwargs)

        for child in self.children:
            child.function_on_tree(func, *args, **kwargs)


def create_variations_2(node):  # Node[]
    variations = []
    board = node.board
    data = node.data.copy()
    zobrist_key = data["zobrist_key"]

    for move in list(board.legal_moves):
        v = board.copy()
        
        data['zobrist_key'] = rehash(zobrist_key, v, move)
        data['hashval'] = data['zobrist_key'] % 10000000
        data["move"] = move
        
        v.push(move)

        variations.append(Node(v, parent=node, **data))

    return variations


def create_variations(node):  # Node[]
    variations = []
    data = node.data.copy()
    board = node.board

    for move in list(board.legal_moves):
        v = board.copy()
        v.push(move)

        data["move"] = move
        variations.append(Node(v, parent=node, **data))

    return variations


def alpha_beta_search_2(node, depth, scoring_dict, variation_func, alpha, beta, 
                        transposition_table={i: None for i in range(10000000)}):
    color = node.board.turn

    if depth == 0 or node.board.is_game_over():
        hashval = node.data['hashval']
        
        if transposition_table[hashval] is None:
            node.data['score'] = evaluate(node.board, scoring_dict)
            transposition_table[hashval] = node.data['score']
            return
        elif transposition_table[hashval] is not None:
            node.data['score'] = transposition_table[hashval]
            return

    if not node.children:
        node.create_children(variation_func)

    if color:
        maxval = -100000000
        best_move = None

        for child in node.children:
            hashval = child.data["hashval"]
            
            if transposition_table[hashval] is None:
                alpha_beta_search_2(
                    child, depth - 1, scoring_dict, variation_func, alpha, beta, 
                    transposition_table=transposition_table)
                transposition_table[hashval] = child.data['score']
                
            elif transposition_table[hashval] is not None:
                #print(child.data["zobrist_key"], hashval, transposition_table[hashval])
                child.data['score'] = transposition_table[hashval]
                
            
            score = child.data['score']    
            maxval = max(maxval, score)

            if maxval == score:
                best_move = child.data['move']

            alpha = max(alpha, score)
            if beta <= alpha:
                break

        node.data['score'] = maxval
        return best_move

    else:
        minval = 100000000
        best_move = None

        for child in node.children:
            hashval = child.data["hashval"]
            
            if transposition_table[hashval] is None:
                alpha_beta_search_2(
                    child, depth - 1, scoring_dict, variation_func, alpha, beta, 
                    transposition_table=transposition_table)
                transposition_table[hashval] = child.data['score']
                
            elif transposition_table[hashval] is not None:
                #print(child.data["zobrist_key"], hashval, transposition_table[hashval])
                child.data['score'] = transposition_table[hashval]
                
                
            score = child.data['score']   
            minval = min(minval, score)

            if minval == score:
                best_move = child.data['move']

            beta = min(beta, score)
            if beta <= alpha:
                break

        node.data['score'] = minval
        return best_move

    
def alpha_beta_search(node, depth, scoring_dict, variation_func, alpha, beta):
    color = node.board.turn

    if depth == 0 or node.board.is_game_over():
        node.data['score'] = evaluate(node.board, scoring_dict)
        return

    if not node.children:
        node.create_children(variation_func)

    if color:
        maxval = -100000000
        best_move = None

        for child in node.children:
            alpha_beta_search(child, depth - 1, scoring_dict, variation_func, alpha, beta)
            score = child.data['score']
            maxval = max(maxval, score)

            if maxval == score:
                best_move = child.data['move']

            alpha = max(alpha, score)
            if beta <= alpha:
                break

        node.data['score'] = maxval
        return best_move

    else:
        minval = 100000000
        best_move = None

        for child in node.children:
            alpha_beta_search(child, depth - 1, scoring_dict, variation_func, alpha, beta)
            score = child.data['score']
            minval = min(minval, score)

            if minval == score:
                best_move = child.data['move']

            beta = min(beta, score)
            if beta <= alpha:
                break

        node.data['score'] = minval
        return best_move