from copy import deepcopy
from pprint import pprint
import re
from dataclasses import dataclass
from typing import Sequence
import time


@dataclass
class ParsedMapItem:
    destination_start: int
    source_start: int
    range_length: int


def parse_map_items_line(line: str) -> ParsedMapItem:
    pattern = r"\s*(\d+)\s*"
    values = [int(seed) for seed in re.findall(pattern=pattern, string=line)]
    if len(values) != 3:
        raise Exception(
            f"Got more or less than three values on line '{line}', {values}"
        )
    return ParsedMapItem(
        destination_start=values[0], source_start=values[1], range_length=values[2]
    )


def parse_seeds(line: str) -> list[int]:  # TODO: function above could be used instead
    seeds_pattern = r"\s*(\d+)\s*"
    seeds = [int(seed) for seed in re.findall(pattern=seeds_pattern, string=line)]
    return seeds


class SeedPair(object):
    def __init__(self, start, range_length) -> None:
        self.start = start
        self.range_length = range_length

    def iterate(self):
        for i in range(self.range_length):
            yield self.start + i

    def __str__(self) -> str:
        return f"SeedPair(start={self.start}, range_length={self.range_length})"

    def __repr__(self) -> str:
        return self.__str__()


def parse_seeds_part_2(line: str) -> list[SeedPair]:
    pattern = r"\s*((\d+\s+\d+)+)"
    groups = re.findall(pattern=pattern, string=line)
    seeds_pairs = []
    for group in groups:
        parts = group[0].strip().split(" ")
        seeds_pairs.append(SeedPair(start=int(parts[0]), range_length=int(parts[1])))
    return seeds_pairs


def add_map_item_values_to_map(map: dict[int, int], map_item: ParsedMapItem):
    print(map_item)
    # for i in range(map_item.range_length):
    #     map[map_item.source_start + i] = map_item.destination_start + i


class CustomMap(object):
    def __init__(self) -> None:
        self.keys = []
        self.values = []

    def add(self, key: int, value: int):
        self.keys.append(key)
        self.values.append(value)

    def as_dict(self):
        output = dict.fromkeys(self.keys)
        for key, value in zip(self.keys, self.values):
            output[key] = value
        return output


def add_map_item_values_to_map_v2(map: CustomMap, map_item: ParsedMapItem):
    for i in range(map_item.range_length):
        map.add(map_item.source_start + i, map_item.destination_start + i)


@dataclass
class PuzzleInput:
    seeds: list[int]
    seeds_to_soil: dict[int, int]
    soil_to_fertilizer: dict[int, int]
    fertilizer_to_water: dict[int, int]
    water_to_light: dict[int, int]
    light_to_temperature: dict[int, int]
    temperature_to_humidity: dict[int, int]
    humidity_to_location: dict[int, int]


def parse_puzzle_input(puzzle_input: Sequence) -> PuzzleInput:
    seeds = []

    seeds_to_soil = CustomMap()
    soil_to_fertilizer = CustomMap()
    fertilizer_to_water = CustomMap()
    water_to_light = CustomMap()
    light_to_temperature = CustomMap()
    temperature_to_humidity = CustomMap()
    humidity_to_location = CustomMap()

    current_step = ""

    step_start_time = 0

    for line in puzzle_input:
        clean_line = line.strip()

        if clean_line.startswith("seeds"):
            step_start_time = time.time()
            seeds = parse_seeds(line)
            duration = time.time() - step_start_time
            print(f"parsed seeds, took {duration}s")
            continue

        match clean_line:
            case "seed-to-soil map:":
                current_step = "seeds_to_soil"
                step_start_time = time.time()
                print("parsing seeds_to_soil")
            case "soil-to-fertilizer map:":
                current_step = "soil_to_fertilizer"
                step_start_time = time.time()
                print("parsing soil_to_fertilizer")
            case "fertilizer-to-water map:":
                current_step = "fertilizer_to_water"
                step_start_time = time.time()
                print("parsing fertilizer_to_water")
            case "water-to-light map:":
                current_step = "water_to_light"
                step_start_time = time.time()
                print("parsing water_to_light")
            case "light-to-temperature map:":
                current_step = "light_to_temperature"
                step_start_time = time.time()
                print("parsing light_to_temperature")
            case "temperature-to-humidity map:":
                current_step = "temperature_to_humidity"
                step_start_time = time.time()
                print("parsing temperature_to_humidity")
            case "humidity-to-location map:":
                current_step = "humidity_to_location"
                step_start_time = time.time()
                print("parsing humidity_to_location")
            case "":
                duration = time.time() - step_start_time
                print(f"parsed step, took {duration}s")
            case _:
                map_item = parse_map_items_line(line=line)
                match current_step:
                    case "seeds_to_soil":
                        add_map_item_values_to_map_v2(
                            map=seeds_to_soil, map_item=map_item
                        )
                    case "soil_to_fertilizer":
                        add_map_item_values_to_map_v2(
                            map=soil_to_fertilizer, map_item=map_item
                        )
                    case "fertilizer_to_water":
                        add_map_item_values_to_map_v2(
                            map=fertilizer_to_water, map_item=map_item
                        )
                    case "water_to_light":
                        add_map_item_values_to_map_v2(
                            map=water_to_light, map_item=map_item
                        )
                    case "light_to_temperature":
                        add_map_item_values_to_map_v2(
                            map=light_to_temperature, map_item=map_item
                        )
                    case "temperature_to_humidity":
                        add_map_item_values_to_map_v2(
                            map=temperature_to_humidity, map_item=map_item
                        )
                    case "humidity_to_location":
                        add_map_item_values_to_map_v2(
                            map=humidity_to_location, map_item=map_item
                        )

    return PuzzleInput(
        seeds=seeds,
        seeds_to_soil=seeds_to_soil.as_dict(),
        soil_to_fertilizer=soil_to_fertilizer.as_dict(),
        fertilizer_to_water=fertilizer_to_water.as_dict(),
        water_to_light=water_to_light.as_dict(),
        light_to_temperature=light_to_temperature.as_dict(),
        temperature_to_humidity=temperature_to_humidity.as_dict(),
        humidity_to_location=humidity_to_location.as_dict(),
    )


class MapRange(object):
    def __init__(self, data: ParsedMapItem) -> None:
        self.source_start = data.source_start
        self.source_end = data.source_start + data.range_length - 1
        self.destination_start = data.destination_start
        self.destination_end = data.destination_start + data.range_length - 1
        self.range_length = data.range_length

    @classmethod
    def from_min_range(cls, start: int, end: int):
        range_length = end - start
        return cls(
            ParsedMapItem(
                destination_start=start, source_start=start, range_length=range_length
            )
        )

    def __str__(self) -> str:
        return f"MapRange(source_start={self.source_start}, source_end={self.source_end}, destination_start={self.destination_start}, destination_end={self.destination_end})"

    def __repr__(self) -> str:
        return self.__str__()

    def source_within_range(self, value: int):
        return self.source_start < value < self.source_end

    def get_destination(self, source: int):
        diff = source - self.source_start
        return self.destination_start + diff

    def as_dict(self) -> dict[int, int]:
        keys = [self.source_start + i for i in range(self.range_length)]
        output = dict.fromkeys(keys)
        for i in range(self.range_length):
            output[self.source_start + i] = self.destination_start + i
        return output


class PuzzleInputV2(object):
    def __init__(
        self,
        seeds_part_1: list[int],
        seeds_part_2: list[SeedPair],
        seeds_to_soil: list[MapRange],
        soil_to_fertilizer: list[MapRange],
        fertilizer_to_water: list[MapRange],
        water_to_light: list[MapRange],
        light_to_temperature: list[MapRange],
        temperature_to_humidity: list[MapRange],
        humidity_to_location: list[MapRange],
    ) -> None:
        self.seeds_part_1 = seeds_part_1
        self.seeds_part_2 = seeds_part_2
        self.seeds_to_soil = seeds_to_soil
        self.soil_to_fertilizer = soil_to_fertilizer
        self.fertilizer_to_water = fertilizer_to_water
        self.water_to_light = water_to_light
        self.light_to_temperature = light_to_temperature
        self.temperature_to_humidity = temperature_to_humidity
        self.humidity_to_location = humidity_to_location

    def __str__(self) -> str:
        return f"""PuzzleInput(
            seeds_part_1={self.seeds_part_1},
            seeds_part_2={self.seeds_part_2},
            seeds_to_soil={self.seeds_to_soil},
            soil_to_fertilizers={self.soil_to_fertilizer},
            fertilizer_to_water={self.fertilizer_to_water},
            water_to_light={self.water_to_light},
            light_to_temperature={self.light_to_temperature},
            temperature_to_humidity={self.temperature_to_humidity},
            humidity_to_location={self.humidity_to_location}
        )"""

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def transform_ranges_to_dict(ranges: list[MapRange]):
        result = {}
        for item in ranges:
            result.update(item.as_dict())
        return result

    def seeds_to_soil_as_dict(self):
        return self.transform_ranges_to_dict(self.seeds_to_soil)

    def soil_to_fertilizer_as_dict(self):
        return self.transform_ranges_to_dict(self.soil_to_fertilizer)

    def fertilizer_to_water_as_dict(self):
        return self.transform_ranges_to_dict(self.fertilizer_to_water)

    def water_to_light_as_dict(self):
        return self.transform_ranges_to_dict(self.water_to_light)

    def light_to_temperature_as_dict(self):
        return self.transform_ranges_to_dict(self.light_to_temperature)

    def temperature_to_humidity_as_dict(self):
        return self.transform_ranges_to_dict(self.temperature_to_humidity)

    def humidity_to_location_as_dict(self):
        return self.transform_ranges_to_dict(self.humidity_to_location)


def parse_puzzle_input_v2(puzzle_input: Sequence) -> PuzzleInputV2:
    seeds_part_1: list[int] = []
    seeds_part_2: list[SeedPair] = []
    seeds_to_soil: list[MapRange] = []
    soil_to_fertilizer: list[MapRange] = []
    fertilizer_to_water: list[MapRange] = []
    water_to_light: list[MapRange] = []
    light_to_temperature: list[MapRange] = []
    temperature_to_humidity: list[MapRange] = []
    humidity_to_location: list[MapRange] = []

    current_step = ""

    step_start_time = 0

    for line in puzzle_input:
        clean_line = line.strip()

        if clean_line.startswith("seeds"):
            step_start_time = time.time()
            seeds_part_1 = parse_seeds(line)
            seeds_part_2 = parse_seeds_part_2(line)
            duration = time.time() - step_start_time
            print(f"parsed seeds, took {duration}s")
            continue

        match clean_line:
            case "seed-to-soil map:":
                current_step = "seeds_to_soil"
                step_start_time = time.time()
                print("parsing seeds_to_soil")
            case "soil-to-fertilizer map:":
                current_step = "soil_to_fertilizer"
                step_start_time = time.time()
                print("parsing soil_to_fertilizer")
            case "fertilizer-to-water map:":
                current_step = "fertilizer_to_water"
                step_start_time = time.time()
                print("parsing fertilizer_to_water")
            case "water-to-light map:":
                current_step = "water_to_light"
                step_start_time = time.time()
                print("parsing water_to_light")
            case "light-to-temperature map:":
                current_step = "light_to_temperature"
                step_start_time = time.time()
                print("parsing light_to_temperature")
            case "temperature-to-humidity map:":
                current_step = "temperature_to_humidity"
                step_start_time = time.time()
                print("parsing temperature_to_humidity")
            case "humidity-to-location map:":
                current_step = "humidity_to_location"
                step_start_time = time.time()
                print("parsing humidity_to_location")
            case "":
                duration = time.time() - step_start_time
                print(f"parsed step, took {duration}s")
            case _:
                map_item = parse_map_items_line(line=line)
                match current_step:
                    case "seeds_to_soil":
                        seeds_to_soil.append(MapRange(map_item))
                    case "soil_to_fertilizer":
                        soil_to_fertilizer.append(MapRange(map_item))
                    case "fertilizer_to_water":
                        fertilizer_to_water.append(MapRange(map_item))
                    case "water_to_light":
                        water_to_light.append(MapRange(map_item))
                    case "light_to_temperature":
                        light_to_temperature.append(MapRange(map_item))
                    case "temperature_to_humidity":
                        temperature_to_humidity.append(MapRange(map_item))
                    case "humidity_to_location":
                        humidity_to_location.append(MapRange(map_item))

    seeds_to_soil.sort(key=lambda item: item.source_start)
    soil_to_fertilizer.sort(key=lambda item: item.source_start)
    fertilizer_to_water.sort(key=lambda item: item.source_start)
    water_to_light.sort(key=lambda item: item.source_start)
    light_to_temperature.sort(key=lambda item: item.source_start)
    temperature_to_humidity.sort(key=lambda item: item.source_start)
    humidity_to_location.sort(key=lambda item: item.source_start)
    return PuzzleInputV2(
        seeds_part_1=seeds_part_1,
        seeds_part_2=seeds_part_2,
        seeds_to_soil=seeds_to_soil,
        soil_to_fertilizer=soil_to_fertilizer,
        fertilizer_to_water=fertilizer_to_water,
        water_to_light=water_to_light,
        light_to_temperature=light_to_temperature,
        temperature_to_humidity=temperature_to_humidity,
        humidity_to_location=humidity_to_location,
    )


def get_destination_for_source(map: dict[int, int], source: int) -> int:
    if source in map:
        return map[source]
    return source


def get_location_for_seed(puzzle_data: PuzzleInput, seed: int):
    step_start_time = time.time()
    print(f"finding location for seed {seed=}")
    soil = get_destination_for_source(puzzle_data.seeds_to_soil, seed)
    fertilizer = get_destination_for_source(puzzle_data.soil_to_fertilizer, soil)
    water = get_destination_for_source(puzzle_data.fertilizer_to_water, fertilizer)
    light = get_destination_for_source(puzzle_data.water_to_light, water)
    temperature = get_destination_for_source(puzzle_data.light_to_temperature, light)
    humidity = get_destination_for_source(
        puzzle_data.temperature_to_humidity, temperature
    )
    location = get_destination_for_source(puzzle_data.humidity_to_location, humidity)
    duration = time.time() - step_start_time
    print(f"looked for location, took {duration}s")
    return location


def get_destination_for_source_v2(map: list[MapRange], source: int):
    for mapRange in map:
        if mapRange.source_within_range(source):
            return mapRange.get_destination(source)
    return source


def get_location_for_seed_v2(puzzle_data: PuzzleInputV2, seed: int):
    step_start_time = time.time()
    print(f"finding location for seed {seed=}")

    soil = get_destination_for_source_v2(puzzle_data.seeds_to_soil, seed)
    fertilizer = get_destination_for_source_v2(puzzle_data.soil_to_fertilizer, soil)
    water = get_destination_for_source_v2(puzzle_data.fertilizer_to_water, fertilizer)
    light = get_destination_for_source_v2(puzzle_data.water_to_light, water)
    temperature = get_destination_for_source_v2(puzzle_data.light_to_temperature, light)
    humidity = get_destination_for_source_v2(
        puzzle_data.temperature_to_humidity, temperature
    )
    location = get_destination_for_source_v2(puzzle_data.humidity_to_location, humidity)

    duration = time.time() - step_start_time
    print(f"looked for location, took {duration}s")
    return location


def find_min_and_max_seeds(seedPairs: list[SeedPair]) -> tuple[int, int]:
    min = None
    for pair in seedPairs:
        if not min or min > pair.start:
            min = pair.start

    max = None
    for pair in seedPairs:
        pair_max = pair.start + pair.range_length - 1
        if not max or max < pair_max:
            max = pair_max
    return min, max


@dataclass
class StageBoundaries:
    source_min: int
    source_max: int
    destination_min: int
    destination_max: int


def find_min_and_max_for_stage(map: list[MapRange]) -> StageBoundaries:
    src_min = None
    src_max = None
    dest_min = None
    dest_max = None
    for item in map:
        if not src_min or src_min > item.source_start:
            src_min = item.source_start
        if not src_max or src_max < item.source_end:
            src_max = item.source_end
        if not dest_min or dest_min > item.destination_start:
            dest_min = item.destination_start
        if not dest_max or dest_max < item.destination_end:
            dest_max = item.destination_end
    return StageBoundaries(
        source_min=src_min,
        source_max=src_max,
        destination_min=dest_min,
        destination_max=dest_max,
    )


def get_ranges_from_min_to_max(map: list[MapRange]) -> list[MapRange]:
    boundaries = find_min_and_max_for_stage(map)

    min_dest = boundaries.destination_min
    min_src = boundaries.source_min
    lowest = min_dest if min_dest < min_src else min_src
    lowest_range = MapRange.from_min_range(start=0, end=lowest)
    map_to_modify = deepcopy(map)
    map_to_modify.append(lowest_range)
    map_to_modify.sort(key=lambda item: item.destination_start)
    return map_to_modify
