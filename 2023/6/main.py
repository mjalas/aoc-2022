import sys
from typing import Sequence
from utils import (
    get_winning_counts,
    parse_lines,
    calculate_margin_of_error,
    parse_lines_part_2,
    calculate_winnings,
)


def solution_1(puzzle_input: Sequence) -> None:
    time_values, distance_values = parse_lines(puzzle_input)
    results = get_winning_counts(
        time_values=time_values, distance_values=distance_values
    )

    margin_of_error = calculate_margin_of_error(results)
    print(f"solution 1: {margin_of_error}")


def solution_2(puzzle_input: Sequence) -> None:
    time_value, distance_value = parse_lines_part_2(puzzle_input=puzzle_input)
    result = calculate_winnings(time_value=time_value, distance_value=distance_value)
    print(f"solution 2: {len(result)}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        challenge_input = sys.argv[1]
        with open(challenge_input, "r") as src:
            solution_1(src)

        with open(challenge_input, "r") as src:
            solution_2(src)
