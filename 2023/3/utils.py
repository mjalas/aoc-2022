from dataclasses import dataclass
from typing import Optional, Tuple
from typing import Sequence


def parse_map_v2(input_str: Sequence):
    map = []
    for i, line in enumerate(input_str):
        for j, c in enumerate(line):
            if c.isdigit():
                value_parts = [c]
                next_char = j + 1
                while line[next_char].isdigit():
                    value_parts.append(line[next_char])
                    next_char += 1

                # calculate location metadata


def parse_map(input_str: Sequence) -> list[list[str]]:
    map: list[list[str]] = []
    for i, line in enumerate(input_str):
        row = []
        for c in line:
            row.append(c)
        map.append(row)
    return map


def symbol_at_coord(map: list[list[str]], x_coord: int, y_coord: int) -> bool:
    is_part_number = False
    try:
        adjacent = map[x_coord][y_coord]
    except IndexError:
        pass
    else:
        if not adjacent.isdigit() and adjacent != "\n" and adjacent != ".":
            # found symbol
            is_part_number = True
    return is_part_number


def get_adjacent_coordinates(x_coord: int, y_coord: int) -> list[Tuple[int, int]]:
    x_above = x_coord - 1
    x_below = x_coord + 1
    y_left = y_coord - 1
    y_right = y_coord + 1
    return [
        (x_above, y_left),
        (x_above, y_coord),
        (x_above, y_right),
        (x_coord, y_left),
        (x_coord, y_right),
        (x_below, y_left),
        (x_below, y_coord),
        (x_below, y_right),
    ]


def coord_has_adjacent_symbol(map: list[list[str]], x_coord: int, y_coord: int):
    has_adjacent_symbol = False
    adjacents = get_adjacent_coordinates(x_coord=x_coord, y_coord=y_coord)
    for coord in adjacents:
        if symbol_at_coord(map=map, x_coord=coord[0], y_coord=coord[1]):
            has_adjacent_symbol = True
            break
    return has_adjacent_symbol


def debug_row(map: list[list[str]], row: int) -> None:
    if (row - 1) > 0:
        print(f"{row-1}: {''.join(map[row - 1])}")
    print(f"{row}: {''.join(map[row ])}")
    if (row + 1) < len(map):
        print(f"{row+1}: {''.join(map[row + 1])}")
    print("")


def find_part_numbers(map: list[list[str]]) -> list[int]:
    number_parts = []
    for i in range(len(map)):
        number_parts_for_row = []
        j = 0
        row_len = len(map[i])
        while j < row_len:
            col = map[i][j]

            if col.isdigit():
                num_chars = [col]
                is_number_part = coord_has_adjacent_symbol(map, i, j)

                next_step = j + 1
                # collect the number

                while next_step < row_len and map[i][next_step].isdigit():
                    num_chars.append(map[i][next_step])
                    if not is_number_part:
                        is_number_part = coord_has_adjacent_symbol(map, i, next_step)
                    next_step += 1
                number_part = int("".join(num_chars))
                if is_number_part:
                    number_parts_for_row.append(number_part)
                j = next_step
            else:
                j += 1
        number_parts.extend(number_parts_for_row)
    return number_parts


@dataclass
class Coordinate:
    x: int
    y: int


@dataclass
class MapNumber:
    value: int
    starting_point: Coordinate
    length: int


def map_number_has_adjacent_symbols(
    map: list[list[str]], map_number: MapNumber
) -> list[Coordinate]:
    adjacent_symbols = []
    adjacents = get_adjacent_coordinates(x_coord=x_coord, y_coord=y_coord)
    for coord in adjacents:
        if symbol_at_coord(map=map, x_coord=coord[0], y_coord=coord[1]):
            adjacent_symbols.append(Coordinate(x=coord[0], y=coord[1]))

    return adjacent_symbols


def get_adjacent_for_map_number(
    map_number: MapNumber, map: list[list[str]]
) -> list[Coordinate]:
    x_above = map_number.starting_point.x - 1
    x_below = map_number.starting_point.x + 1
    y_left = map_number.starting_point.y - 1
    y_right = map_number.starting_point.y + map_number.length

    coordinates = []
    y_start = y_left if y_left >= 0 else map_number.starting_point.y
    y_end = y_right if y_right <= len(map[map_number.starting_point.x]) else y_right - 1

    if x_above >= 0:
        above_coordinates = [
            Coordinate(x=x_above, y=y) for y in range(y_start, y_end + 1, 1)
        ]
        coordinates.extend(above_coordinates)
    if y_left >= 0:
        coordinates.append(Coordinate(x=map_number.starting_point.x, y=y_left))
    if y_right < len(map[map_number.starting_point.x]):
        coordinates.append(Coordinate(x=map_number.starting_point.x, y=y_right))
    if x_below < len(map):
        below_coordinates = [
            Coordinate(x=x_below, y=y) for y in range(y_start, y_end + 1, 1)
        ]
        coordinates.extend(below_coordinates)

    return coordinates


def symbol_at_coord_v2(
    map: list[list[str]], coordinate: Coordinate, symbol: Optional[str] = None
) -> bool:
    is_symbol = False

    try:
        adjacent = map[coordinate.x][coordinate.y]
    except IndexError:
        pass
    else:
        if symbol:
            if adjacent == symbol:
                is_symbol = True
        else:
            if not adjacent.isdigit() and adjacent != "\n" and adjacent != ".":
                # found symbol
                is_symbol = True
    return is_symbol


def find_gears(map: list[list[str]]) -> list[int]:
    symbols_to_numbers: dict[str, list[int]] = {}
    for i in range(len(map)):
        j = 0
        row_len = len(map[i])
        while j < row_len:
            col = map[i][j]

            if col.isdigit():
                num_chars = [col]
                starting_point = Coordinate(x=i, y=j)

                next_step = j + 1
                # collect the number

                while next_step < row_len and map[i][next_step].isdigit():
                    num_chars.append(map[i][next_step])
                    next_step += 1
                number_str = "".join(num_chars)
                number = MapNumber(
                    value=int(number_str),
                    starting_point=starting_point,
                    length=len(number_str),
                )

                adjacents = get_adjacent_for_map_number(map_number=number, map=map)
                symbols = [
                    coord
                    for coord in adjacents
                    if symbol_at_coord_v2(coordinate=coord, map=map, symbol="*")
                ]
                print(symbols)
                for symbol in symbols:
                    key = f"{symbol.x}{symbol.y}"
                    if key not in symbols_to_numbers:
                        symbols_to_numbers[key] = []
                    symbols_to_numbers[key].append(number.value)

                j = next_step
            else:
                j += 1

    gears = []
    print(symbols_to_numbers)
    for key, value in symbols_to_numbers.items():
        if len(value) == 2:
            gears.append(value[0] * value[1])

    return gears
