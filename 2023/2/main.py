import sys
from utils import (
    count_fewest_number_of_cubes_of_each_color,
    count_power_for_game,
    parse_game,
    game_is_possible,
    SetsColors,
)


def solution_1(input_file: str) -> int:
    allowed_set_colors = SetsColors(red=12, green=13, blue=14)
    sum = 0

    with open(input_file, "r") as src:
        for line in src:
            game = parse_game(line)
            if game_is_possible(game, allowed_color_counts=allowed_set_colors):
                sum += game.id

    return sum


def solution_2(input_file: str) -> int:
    total_power = 0

    with open(input_file, "r") as src:
        for line in src:
            game = parse_game(line)
            power = count_power_for_game(
                count_fewest_number_of_cubes_of_each_color(game)
            )
            total_power += power

    return total_power


if __name__ == "__main__":
    if len(sys.argv) == 2:
        challenge_input = sys.argv[1]

        sol_1 = solution_1(challenge_input)
        print(f"sol1: {sol_1}")

        sol_2 = solution_2(challenge_input)
        print(f"sol2: {sol_2}")
    else:
        print("missin input file")
