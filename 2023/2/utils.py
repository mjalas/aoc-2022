from dataclasses import dataclass
import re


def parse_game_id(first_part: str) -> int:
    pattern = r"Game (?P<id>\d+)"
    res = re.match(pattern=pattern, string=first_part)
    if res:
        id = int(res.group("id"))
        return id
    raise Exception("Could not find match")


@dataclass
class SetsColors:
    red: int
    blue: int
    green: int


@dataclass
class Game:
    id: int
    sets: list[SetsColors]


def parse_sets(sets_part: str) -> list[SetsColors]:
    colors = SetsColors(0, 0, 0)
    pattern = r"((?P<count>\d) (?P<color>\w*),*)+"
    parsed_sets: list[SetsColors] = []
    sets = sets_part.strip().split(";")
    for set in sets:
        items = set.strip().split(",")
        red = 0
        blue = 0
        green = 0
        for item in items:
            parts = item.strip().split(" ")
            count = int(parts[0].strip())
            color = parts[1].strip()

            match color:
                case "blue":
                    blue = count
                case "red":
                    red = count
                case "green":
                    green = count
        parsed_sets.append(SetsColors(red=red, blue=blue, green=green))
    return parsed_sets


def parse_game(game: str) -> Game:
    game_parts = game.split(":")
    id = parse_game_id(game_parts[0])
    sets = parse_sets(game_parts[1])
    return Game(id=id, sets=sets)


def game_is_possible(game: Game, allowed_color_counts: SetsColors):
    possible = True
    for set in game.sets:
        if (
            set.blue > allowed_color_counts.blue
            or set.red > allowed_color_counts.red
            or set.green > allowed_color_counts.green
        ):
            possible = False
            break
    return possible


def count_fewest_number_of_cubes_of_each_color(game: Game) -> SetsColors:
    red = 0
    blue = 0
    green = 0

    for set in game.sets:
        if red < set.red:
            red = set.red
        if blue < set.blue:
            blue = set.blue
        if green < set.green:
            green = set.green

    return SetsColors(red=red, green=green, blue=blue)


def count_power_for_game(set: SetsColors) -> int:
    return set.red * set.blue * set.green
