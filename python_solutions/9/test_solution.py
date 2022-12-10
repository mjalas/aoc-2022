from solution import parse_input_part1, parse_input_part1_v2


def test_parse_input():
    input = ["R 4", "U 4", "L 3", "D 1", "R 4", "D 1", "L 5", "R 2"]

    head_locations, tail_locations = parse_input_part1(input)

    print(head_locations)
    tail_unique_locations = list(set(tail_locations))

    assert len(tail_unique_locations) == 13


def test_parse_input_part1_v2():
    input = ["R 4", "U 4", "L 3", "D 1", "R 4", "D 1", "L 5", "R 2"]

    head_locations, tail_locations = parse_input_part1_v2(input)

    print(head_locations)
    tail_unique_locations = list(set(tail_locations))

    assert len(tail_unique_locations) == 13
