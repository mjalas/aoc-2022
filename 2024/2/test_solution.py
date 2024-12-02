import pytest
from solution import is_report_safe, part1

test_input = [
    "7 6 4 2 1",
    "1 2 7 8 9",
    "9 7 6 2 1",
    "1 3 2 4 5",
    "8 6 4 4 1",
    "1 3 6 7 9",
]

part1_inputs_safe = [
    True,
    False,
    False,
    False,
    False,
    True,
]

part1_expected_safe_count = 2


@pytest.mark.parametrize("report,expected", zip(test_input, part1_inputs_safe))
def test_is_report_safe(report, expected):
    report_values = [int(x) for x in report.strip().split(" ")]
    assert (
        is_report_safe(report_values) == expected
    ), f"Failed on line {report} which should be {expected}"


def test_part1():
    assert part1(test_input) == 2
