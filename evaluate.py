import json
from analysis import piece_mobility


def evaluate(_board, scoring_dict, color=True):  # white: True
    score = 0
    dict_keys = scoring_dict.keys()

    for i in range(1, 7):
        positions = list(_board.pieces(i, color=color))
        opponent_positions = list(_board.pieces(i, color=not color))
        num_pieces_ally = len(positions)
        num_pieces_opponent = len(opponent_positions)

        score += num_pieces_ally * scoring_dict["base_val"][str(i)] - num_pieces_opponent * scoring_dict["base_val"][
            str(i)]

        if "position_val" in dict_keys:
            for p in positions:
                score += scoring_dict["position_val"][str(i)][p]
            for op in opponent_positions:
                score -= scoring_dict["position_val"][str(i)][op]
                
        if "mobility_val" in dict_keys and i in [5, 6]: # only consider queen and king for performance
            score += scoring_dict["mobility_val"][str(i)] * (piece_mobility(_board, i, color=color) - piece_mobility(_board, i, color=not color))

    return score


def json_from_dict(valuation, file_str):
    with open(file_str, "w") as file:
        json.dump(valuation, file)


def scoring_from_json(file_str):
    scorings = None

    with open(file_str, "r") as file:
        scorings = json.load(file)

    return scorings