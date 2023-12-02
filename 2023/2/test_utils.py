from utils import (
    parse_game,
    game_is_possible,
    count_fewest_number_of_cubes_of_each_color,
    count_power_for_game,
    SetsColors,
    Game,
)


def test_game_parsing_1():
    input_line = [
        ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", True),
        ("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", True),
        (
            "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
            False,
        ),
        (
            "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
            False,
        ),
        ("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", True),
    ]

    for line in input_line:
        game_str = line[0]
        expected = line[1]

        game = parse_game(game_str)
        res = game_is_possible(game, SetsColors(red=12, green=13, blue=14))

        assert res == expected, f"Got {res} and expected {expected}: {game_str}"


def test_game_parsing_2():
    input_line = [
        ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", 48),
        ("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", 12),
        (
            "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
            1560,
        ),
        (
            "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
            630,
        ),
        ("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", 36),
    ]

    for line in input_line:
        game_str = line[0]
        expected = line[1]
        game = parse_game(game_str)
        res = count_power_for_game(count_fewest_number_of_cubes_of_each_color(game))
        assert res == expected, f"Got {res} and expected {expected}: {game_str}"
