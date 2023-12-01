import pytest

from main import parse_row_into_stacks, reverse_stacks, parse_move_command, MoveCommand, play_command_part1, play_command_part2, copy_stacks, stacks_to_printable
import re

test_data = [
    ("    [C]         [Q]         [V]     ", [[],    ['C'], [],    [],    ['Q'], [], [],       ['V'], []]),
    ("    [D]         [D] [S]     [M] [Z] ", [[],    ['D'], [],    [],    ['D'], ['S'], [],    ['M'], ['Z']]),
    ("    [G]     [P] [W] [M]     [C] [G] ", [[],    ['G'], [],    ['P'], ['W'], ['M'], [],    ['C'], ['G']]),
    ("    [F]     [Z] [C] [D] [P] [S] [W] ", [[],    ['F'], [],    ['Z'], ['C'], ['D'], ['P'], ['S'], ['W']]),
    ("[P] [L]     [C] [V] [W] [W] [H] [L] ", [['P'], ['L'], [],    ['C'], ['V'], ['W'], ['W'], ['H'], ['L']]),
    ("[G] [B] [V] [R] [L] [N] [G] [P] [F] ", [['G'], ['B'], ['V'], ['R'], ['L'], ['N'], ['G'], ['P'], ['F']]),
    ("[R] [T] [S] [S] [S] [T] [D] [L] [P] ", [['R'], ['T'], ['S'], ['S'], ['S'], ['T'], ['D'], ['L'], ['P']]),
    ("[N] [J] [M] [L] [P] [C] [H] [Z] [R] ", [['N'], ['J'], ['M'], ['L'], ['P'], ['C'], ['H'], ['Z'], ['R']])
]

@pytest.mark.parametrize("input, expected", test_data)
def test_rows_separately(input, expected):

    stacks = [[], [], [], [], [], [], [], [], []]
    result = parse_row_into_stacks(stacks, input)
    
    for i in range(len(stacks)):
        assert result[i] == expected[i]



def test_stacks_to_printable():
    input = [
        "    [C]         [Q]         [V]     ",
        "    [D]         [D] [S]     [M] [Z] ",
        "    [G]     [P] [W] [M]     [C] [G] ",
        "    [F]     [Z] [C] [D] [P] [S] [W] ",
        "[P] [L]     [C] [V] [W] [W] [H] [L] ",
        "[G] [B] [V] [R] [L] [N] [G] [P] [F] ",
        "[R] [T] [S] [S] [S] [T] [D] [L] [P] ",
        "[N] [J] [M] [L] [P] [C] [H] [Z] [R] "
    ]

    stacks = [[] for i in range(9)]
    for line in input:
        stacks = parse_row_into_stacks(stacks, line)
    
    outcome = stacks_to_printable(stacks)
    
    assert len(input) == len(outcome)
    for i in range(len(input)):
        assert outcome[i] == input[i]


def assert_stacks(stacks: list[list[str]], expected: list[list[str]]):
    for stack in range(9):
        assert len(stacks[stack]) == len(expected[stack]), f"Failed on stack {stack}"
        for i in range(len(stacks[stack])):
            assert stacks[stack][i] == expected[stack][i], f'Failed for index {i} on stack {stack}'


def test_row_parsing():
    
    # [G] [B] [V] [R] [L] [N] [G] [P] [F]
    input = [    
        "    [C]         [Q]         [V]     ",
        "    [D]         [D] [S]     [M] [Z] ",
        "    [G]     [P] [W] [M]     [C] [G] ",
        "    [F]     [Z] [C] [D] [P] [S] [W] ",
        "[P] [L]     [C] [V] [W] [W] [H] [L] ",
        "[G] [B] [V] [R] [L] [N] [G] [P] [F] ",
        "[R] [T] [S] [S] [S] [T] [D] [L] [P] ",
        "[N] [J] [M] [L] [P] [C] [H] [Z] [R] ",
        " 1   2   3   4   5   6   7   8   9 "
    ]
    expected = [
        ['N', 'R', 'G', 'P'],
        ['J', 'T', 'B', 'L', 'F', 'G', 'D', 'C'],
        ['M', 'S', 'V'],
        ['L', 'S', 'R', 'C', 'Z', 'P'],
        ['P', 'S', 'L', 'V', 'C', 'W', 'D', 'Q'],
        ['C', 'T', 'N', 'W', 'D', 'M', 'S'],
        ['H', 'D', 'G', 'W', 'P'],
        ['Z', 'L', 'P', 'H', 'S', 'C', 'M', 'V'],
        ['R', 'P', 'F', 'L', 'W', 'G', 'Z']
    ]
    
    stack_count = 9
    stacks = [[] for i in range(stack_count)]

    for line in input:
        if line.strip() == '':
            continue
        if line.strip().startswith('1'):
            continue

        stacks = parse_row_into_stacks(stacks, line)

    assert_stacks(stacks, expected)
    

def test_reverse_stacks():
    input = [
        ['N', 'R', 'G', 'P'],
        ['J', 'T', 'B', 'L', 'F', 'G', 'D', 'C'],
        ['M', 'S', 'V'],
        ['L', 'S', 'R', 'C', 'Z', 'P'],
        ['P', 'S', 'L', 'V', 'C', 'W', 'D', 'Q'],
        ['C', 'T', 'N', 'W', 'D', 'M', 'S'],
        ['H', 'D', 'G', 'W', 'P'],
        ['Z', 'L', 'P', 'H', 'S', 'C', 'M', 'V'],
        ['R', 'P', 'F', 'L', 'W', 'G', 'Z']
    ]

    expected = [
        ['P', 'G', 'R', 'N'], 
        ['C', 'D', 'G', 'F', 'L', 'B', 'T', 'J'], 
        ['V', 'S', 'M'], 
        ['P', 'Z', 'C', 'R', 'S', 'L'],
        ['Q', 'D', 'W', 'C', 'V', 'L', 'S', 'P'],
        ['S', 'M', 'D', 'W', 'N', 'T', 'C'],
        ['P', 'W', 'G', 'D', 'H'],
        ['V', 'M', 'C', 'S', 'H', 'P', 'L', 'Z'],
        ['Z', 'G', 'W', 'L', 'F', 'P', 'R']
    ]
    

    
    result = reverse_stacks(input)

    assert_stacks(result, expected)


command_test_data = [
    ("move 2 from 4 to 6", 2, 4, 6),
    ("move 4 from 5 to 3", 4, 5, 3),
    ("move 6 from 6 to 1", 6, 6, 1),
    ("move 4 from 1 to 4", 4, 1, 4)

]

@pytest.mark.parametrize("input, expectedCount, expectedFrom, expectedTo", command_test_data)
def test_parse_move_command(input, expectedCount, expectedFrom, expectedTo):
    
    
    res = parse_move_command(input)
    assert res.count == expectedCount
    assert res.from_stack == expectedFrom
    assert res.to_stack == expectedTo


def test_play_command_part1():
    stacks = [
        ['N', 'R', 'G', 'P'],
        ['J', 'T', 'B', 'L', 'F', 'G', 'D', 'C'],
        ['M', 'S', 'V'],
        ['L', 'S', 'R', 'C', 'Z', 'P'],
        ['P', 'S', 'L', 'V', 'C', 'W', 'D', 'Q'],
        ['C', 'T', 'N', 'W', 'D', 'M', 'S'],
        ['H', 'D', 'G', 'W', 'P'],
        ['Z', 'L', 'P', 'H', 'S', 'C', 'M', 'V'],
        ['R', 'P', 'F', 'L', 'W', 'G', 'Z']
    ]
    
    expected = [
        ['N', 'R'],
        ['J', 'T', 'B', 'L', 'F', 'G', 'D', 'C'],
        ['M', 'S', 'V', 'P', 'G'],
        ['L', 'S', 'R', 'C', 'Z', 'P'],
        ['P', 'S', 'L', 'V', 'C', 'W', 'D', 'Q'],
        ['C', 'T', 'N', 'W', 'D', 'M', 'S'],
        ['H', 'D', 'G', 'W', 'P'],
        ['Z', 'L', 'P', 'H', 'S', 'C', 'M', 'V'],
        ['R', 'P', 'F', 'L', 'W', 'G', 'Z']
    ]

    command = MoveCommand(count=2, from_stack=1, to_stack=3)
    result = play_command_part1(command, stacks)
    
    assert_stacks(result, expected)

def test_play_command_part1():
    stacks = [
        ['N', 'R', 'G', 'P'],
        ['J', 'T', 'B', 'L', 'F', 'G', 'D', 'C'],
        ['M', 'S', 'V'],
        ['L', 'S', 'R', 'C', 'Z', 'P'],
        ['P', 'S', 'L', 'V', 'C', 'W', 'D', 'Q'],
        ['C', 'T', 'N', 'W', 'D', 'M', 'S'],
        ['H', 'D', 'G', 'W', 'P'],
        ['Z', 'L', 'P', 'H', 'S', 'C', 'M', 'V'],
        ['R', 'P', 'F', 'L', 'W', 'G', 'Z']
    ]
    
    expected = [
        ['N', 'R'],
        ['J', 'T', 'B', 'L', 'F', 'G', 'D', 'C'],
        ['M', 'S', 'V', 'G', 'P'],
        ['L', 'S', 'R', 'C', 'Z', 'P'],
        ['P', 'S', 'L', 'V', 'C', 'W', 'D', 'Q'],
        ['C', 'T', 'N', 'W', 'D', 'M', 'S'],
        ['H', 'D', 'G', 'W', 'P'],
        ['Z', 'L', 'P', 'H', 'S', 'C', 'M', 'V'],
        ['R', 'P', 'F', 'L', 'W', 'G', 'Z']
    ]

    command = MoveCommand(count=2, from_stack=1, to_stack=3)
    result = play_command_part2(command, stacks)
    
    assert_stacks(result, expected)


def test_copy_stacks():
    stacks = [
        ['P', 'G', 'R', 'N'], 
        ['C', 'D', 'G', 'F', 'L', 'B', 'T', 'J'], 
        ['V', 'S', 'M'], 
        ['P', 'Z', 'C', 'R', 'S', 'L'],
        ['Q', 'D', 'W', 'C', 'V', 'L', 'S', 'P'],
        ['S', 'M', 'D', 'W', 'N', 'T', 'C'],
        ['P', 'W', 'G', 'D', 'H'],
        ['V', 'M', 'C', 'S', 'H', 'P', 'L', 'Z'],
        ['Z', 'G', 'W', 'L', 'F', 'P', 'R']]

    copied_stacks = copy_stacks(stacks)

    copied_stacks[0].append('S')
    
    assert stacks[0] != copied_stacks[0]
