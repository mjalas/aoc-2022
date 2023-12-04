import sys
from utils import find_gears, parse_map, find_part_numbers


def solution_1(input_file: str) -> int:
    number_parts = 0
    with open(input_file, "r") as src:
        map = parse_map(input_str=src)
        # print(map)
        number_parts = find_part_numbers(map=map)
        # print(number_parts)
    result = sum(number_parts)
    return result


def solution_2(input_file: str) -> str:
    with open(input_file, "r") as src:
        map = parse_map(input_str=src)
        gears = find_gears(map=map)
    result = sum(gears)
    return result


if __name__ == "__main__":
    if len(sys.argv) == 2:
        challenge_input = sys.argv[1]

        sol_1 = solution_1(challenge_input)
        print(f"sol1: {sol_1}")
        sol_2 = solution_2(challenge_input)
        print(f"sol2: {sol_2}")
