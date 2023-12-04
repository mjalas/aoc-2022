from utils import find_gears, parse_map, find_part_numbers


def test_parse_map():
    input_str = [
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
        ".....+.58.",
        "..592.....",
        "......755.",
        "...$.*....",
        ".664.598..",
    ]
    expected_sum = 4361
    map = parse_map(input_str=input_str)
    print(map)
    number_parts = find_part_numbers(map=map)
    print(number_parts)
    result = sum(number_parts)
    assert result == expected_sum, f"Got {result} but expected {expected_sum}"


def test_simple_map():
    input_str = [
        "467..114..",
        "...*......",
        "..35..633.",
    ]
    expected_sum = 467 + 35
    map = parse_map(input_str=input_str)
    print(map)
    number_parts = find_part_numbers(map=map)
    print(number_parts)
    result = sum(number_parts)
    assert result == expected_sum, f"Got {result} but expected {expected_sum}"


def test_simple_map_second():
    input_str = [
        "467..114..",
        "...*.3....",
        "..35..633.",
    ]
    expected_sum = 467 + 35
    map = parse_map(input_str=input_str)
    print(map)
    number_parts = find_part_numbers(map=map)
    print(number_parts)
    result = sum(number_parts)
    assert result == expected_sum, f"Got {result} but expected {expected_sum}"


def test_simple_map_two_symbols():
    input_str = [
        "467..114..",
        ".&.*.3....",
        "..35..633.",
    ]
    expected_sum = 467 + 35
    map = parse_map(input_str=input_str)
    print(map)
    number_parts = find_part_numbers(map=map)
    print(number_parts)
    result = sum(number_parts)
    assert result == expected_sum, f"Got {result} but expected {expected_sum}"


def test_simple_map_new_line_end():
    input_str = [
        "467..114.\n",
        ".&.*.3...\n",
        "..35..633\n",
    ]
    expected_sum = 467 + 35
    map = parse_map(input_str=input_str)
    print(map)
    number_parts = find_part_numbers(map=map)
    print(number_parts)
    result = sum(number_parts)
    assert result == expected_sum, f"Got {result} but expected {expected_sum}"


def test_gears():
    input_str = [
        "467..114..\n",
        "...*......\n",
        "..35..633.\n",
        "......#...\n",
        "617*......\n",
        ".....+.58.\n",
        "..592.....\n",
        "......755.\n",
        "...$.*....\n",
        ".664.598..\n",
    ]
    expected_sum = 467835
    map = parse_map(input_str=input_str)
    gears = find_gears(map=map)
    result = sum(gears)
    assert result == expected_sum, f"Got {result} but expected {expected_sum}"


def test_gears_symbol_at_end_of_line():
    input_str = [
        "467...114*\n",
        "...*....20\n",
        "........*.\n",
        "..35..633.\n",
        "......#...\n",
        "617*......\n",
        ".....+.58.\n",
        "..592....&\n",
        "......755.\n",
    ]
    expected_sum = 114 * 20 + 20 * 633
    map = parse_map(input_str=input_str)
    gears = find_gears(map=map)
    result = sum(gears)
    assert result == expected_sum, f"Got {result} but expected {expected_sum}"


def test_gears_symbol_at_beginning_of_line():
    input_str = [
        "*467...114\n",
        "20.*......\n",
        ".*........\n",
        ".135..633.\n",
        "*....#....\n",
        "617*......\n",
        "....12*58.\n",
        "..59*....&\n",
        "......755.\n",
    ]
    expected_sum = 467 * 20 + 20 * 135 + 135 * 617 + 617 * 12 + 12 * 59 + 12 * 58
    map = parse_map(input_str=input_str)
    gears = find_gears(map=map)
    result = sum(gears)
    assert result == expected_sum, f"Got {result} but expected {expected_sum}"


def test_gears_symbol_multi():
    input_str = [
        "....114...\n",
        "...*...*..\n",
        "....123...\n",
        "....*.....\n",
        "....20....\n",
    ]
    expected_sum = 114 * 123 + 114 * 123 + 123 * 20
    map = parse_map(input_str=input_str)
    gears = find_gears(map=map)
    result = sum(gears)
    assert result == expected_sum, f"Got {result} but expected {expected_sum}"
