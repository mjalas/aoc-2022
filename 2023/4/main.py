import sys
from typing import Sequence

from utils import parse_card_line, parse_card_line_v2


def solution_1(puzzle_input: Sequence) -> int:
    cards_scores = []
    for line in puzzle_input:
        card = parse_card_line(line)
        cards_scores.append(card.score)
    return sum(cards_scores)


def solution_2(puzzle_input: Sequence) -> int:
    card_counts: dict[int, int] = {}
    for line in puzzle_input:
        card = parse_card_line_v2(line)
        if card.id not in card_counts:
            card_counts[card.id] = 1
        else:
            card_counts[card.id] += 1

        for copy in range(card_counts[card.id]):
            for i in range(card.id + 1, card.id + card.wins + 1):
                if i not in card_counts:
                    card_counts[i] = 1
                else:
                    card_counts[i] += 1
    return sum(list(card_counts.values()))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        challenge_input = sys.argv[1]

        with open(challenge_input, "r") as src:
            sol_1 = solution_1(src)
        print(f"Solution 1: {sol_1}")

        with open(challenge_input, "r") as src:
            sol_2 = solution_2(src)
        print(f"Solution 2: {sol_2}")
