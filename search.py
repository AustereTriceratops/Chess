from evaluate import evaluate


class Node():
    def __init__(self, parent=None, **data):
        self.parent = parent
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


def create_variations(node):  # Node[]
    variations = []
    data = node.data.copy()
    board = data["board"]

    for move in list(board.legal_moves):
        v = board.copy()
        v.push(move)

        data["board"] = v
        data["move"] = move
        variations.append(Node(parent=node, **data))

    return variations


def alpha_beta_search(node, depth, scoring_dict, variation_func, alpha, beta):
    color = node.data["board"].turn

    if depth == 0 or node.data['board'].is_game_over():
        node.data['score'] = evaluate(node.data["board"], scoring_dict)
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
