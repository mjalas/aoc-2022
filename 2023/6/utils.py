from typing import Sequence
import re


def parse_values(line: str) -> list[int]:
    pattern = r"\s*(\d+)\s*"
    values = [int(value) for value in re.findall(pattern=pattern, string=line)]
    return values


def parse_lines(puzzle_input: Sequence) -> tuple[list[int], list[int]]:
    time_values = None
    distance_values = None
    for line in puzzle_input:
        if line.startswith("Time"):
            time_values = parse_values(line)
        elif line.startswith("Distance"):
            distance_values = parse_values(line)

    if not time_values or not distance_values:
        raise Exception("Failed to parse input")

    if len(time_values) != len(distance_values):
        raise Exception("Input lists of different sizes")
    return time_values, distance_values


def parse_values_part_2(line: str) -> int:
    pattern = r"\s*(\d+)\s*"
    values: list[str] = re.findall(pattern=pattern, string=line)
    return int("".join(values))


def parse_lines_part_2(puzzle_input: Sequence) -> tuple[list[int], list[int]]:
    time_value = None
    distance_value = None
    for line in puzzle_input:
        if line.startswith("Time"):
            time_value = parse_values_part_2(line)
        elif line.startswith("Distance"):
            distance_value = parse_values_part_2(line)

    if not time_value or not distance_value:
        raise Exception("Failed to parse input")

    return time_value, distance_value


def calculate_winnings(time_value: int, distance_value: int) -> list[int]:
    winning_distances = []
    for push_duration in range(time_value + 1):
        move_duration = time_value - push_duration
        speed = push_duration
        distance = move_duration * speed
        if distance > distance_value:
            winning_distances.append(distance)
    return winning_distances


def get_winning_counts(time_values: list[int], distance_values: list[int]):
    results = []
    for time_value, distance_value in zip(time_values, distance_values):
        winning_distances = calculate_winnings(
            time_value=time_value, distance_value=distance_value
        )
        results.append(winning_distances)
    return results


def calculate_margin_of_error(results: list[list[int]]):
    score = 0
    for result in results:
        if score == 0:
            score = len(result)
        else:
            score *= len(result)
    return score
