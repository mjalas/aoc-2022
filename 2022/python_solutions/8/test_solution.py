import pytest

from solution import (
    parse_input,
    find_visible_edge_trees_count,
    find_visible_middle_trees_count,
    check_left,
    check_right,
    check_up,
    check_down,
    count_scenic_score_for_tree,
    find_highest_scenic_score,
)


test_input_grid = ["30373", "25512", "65332", "33549", "35390"]


def test_parse_grid():
    input = test_input_grid

    expected = [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]

    grid = parse_input(input)

    assert len(grid) == len(expected)
    for row in range(len(grid)):
        assert len(grid[row]) == len(expected[row])
        for col in range(len(grid[row])):
            assert grid[row][col] == expected[row][col]


def test_find_visible_edge_trees():
    input = [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]

    res = find_visible_edge_trees_count(input)

    assert res == 16


def test_find_middle_corner_tree_indexes():
    input = [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]

    upper_left = input[1][1]
    upper_right = input[1][-2]
    bottom_left = input[-2][1]
    bottom_right = input[-2][-2]

    assert upper_left == 5
    assert upper_right == 1
    assert bottom_left == 3
    assert bottom_right == 4


@pytest.mark.parametrize(
    "input, start, expected",
    [
        ([3, 0, 3, 7, 3], 0, True),
        ([3, 0, 3, 7, 3], 1, False),
        ([3, 0, 3, 7, 3], 3, True),
        ([3, 3, 5, 4, 9], 4, True),
    ],
)
def test_check_left(input, start, expected):

    res = check_left(input, start, input[start])

    assert res == expected, f"Should have been {expected} in {input} with start {start}"


@pytest.mark.parametrize(
    "input, start, expected",
    [
        ([3, 0, 3, 7, 3], 0, False),
        ([3, 0, 3, 7, 3], 1, False),
        ([3, 0, 3, 7, 3], 3, True),
        ([3, 3, 5, 4, 9], 4, True),
        ([3, 3, 5, 4, 9], 2, False),
    ],
)
def test_check_right(input, start, expected):

    tree_height = input[start]
    res = check_right(input, start, tree_height)

    assert (
        res == expected
    ), f"Should have been {expected} with height {tree_height} in {input} with start {start}"


@pytest.mark.parametrize(
    "input, start, expected",
    [
        ([3, 0, 3, 7, 3], 0, True),
        ([3, 0, 3, 7, 3], 1, False),
        ([3, 0, 3, 7, 3], 3, True),
        ([3, 3, 5, 4, 9], 4, True),
        ([3, 3, 5, 4, 9], 2, True),
    ],
)
def test_check_up(input, start, expected):
    grid = []
    for i in input:
        grid.append([i])

    tree_height = grid[start][0]
    res = check_up(input=grid, row=start, column=0, val=tree_height)

    assert (
        res == expected
    ), f"Should have been {expected} with height {tree_height} in {input} with start {start}"


@pytest.mark.parametrize(
    "input, start, expected",
    [
        ([3, 0, 3, 7, 3], 0, False),
        ([3, 0, 3, 7, 3], 1, False),
        ([3, 0, 3, 7, 3], 3, True),
        ([3, 3, 5, 4, 9], 4, True),
        ([3, 3, 5, 4, 9], 2, False),
    ],
)
def test_check_down(input, start, expected):
    grid = []
    for i in input:
        grid.append([i])

    tree_height = grid[start][0]
    res = check_down(input=grid, row=start, column=0, val=tree_height)

    assert (
        res == expected
    ), f"Should have been {expected} with height {tree_height} in {input} with start {start}"


def test_find_visible_middle_trees():
    input = [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]
    res = find_visible_middle_trees_count(input)

    assert res == 5


def test_count_scenic_score_for_tree():
    input = [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]
    expected_score = 8
    row = 3
    column = 2
    height = input[row][column]
    res = count_scenic_score_for_tree(grid=input, row=row, column=column, val=height)

    assert (
        res == expected_score
    ), f"Expected score {expected_score}, but got {res} for tree {height} at ({row},{column})"


def test_find_highest_scenic_score():
    input = [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]

    res = find_highest_scenic_score(grid=input)

    assert res == 8
