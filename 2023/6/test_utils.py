import re

from utils import parse_lines, get_winning_counts, calculate_margin_of_error

example_input = ["Time:      7  15   30", "Distance:  9  40  200"]


def test_parsing():
    time_values, distance_values = parse_lines(example_input)
    assert time_values == [7, 15, 30]
    assert distance_values == [9, 40, 200]


def test_calculate_results():
    time_values, distance_values = parse_lines(example_input)
    results = get_winning_counts(
        time_values=time_values, distance_values=distance_values
    )

    assert results[0] == [10, 12, 12, 10]

    margin_of_error = calculate_margin_of_error(results)

    assert margin_of_error == 288
