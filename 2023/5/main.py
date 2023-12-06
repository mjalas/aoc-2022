from multiprocessing.managers import ListProxy
import sys
import asyncio
import time
from utils import (
    MapRange,
    PuzzleInputV2,
    SeedPair,
    parse_puzzle_input_v2,
    get_location_for_seed_v2,
)
from multiprocessing import Process, Manager


def solution_1(puzzle_input: PuzzleInputV2):
    locations = []
    print("starting locations finding")
    for seed in puzzle_input.seeds_part_1:
        print(f"finding for {seed=}")
        location = get_location_for_seed_v2(puzzle_data=puzzle_input, seed=seed)
        locations.append(location)

    locations.sort()
    print(f"solution 1: {locations[0]}")


def find_lowest_location_for_seed_pair(
    seed_pair: SeedPair, puzzle_input: PuzzleInputV2, results: ListProxy
):
    lowest_location = None
    for seed in seed_pair.iterate():
        print(f"finding for {seed=}")
        location = get_location_for_seed_v2(puzzle_data=puzzle_input, seed=seed)
        if not lowest_location or location < lowest_location:
            lowest_location = location
    results.append(lowest_location)


def solution_2(puzzle_input: PuzzleInputV2):
    lowest_location = None
    print("starting locations finding")
    manager = Manager()
    results = manager.list()
    processes: list[Process] = []
    try:
        for seed_pair in puzzle_input.seeds_part_2:
            proc = Process(
                target=find_lowest_location_for_seed_pair,
                args=(seed_pair, puzzle_input, results),
            )
            processes.append(proc)
            proc.start()

        for proc in processes:
            proc.join()
    except KeyboardInterrupt:
        for proc in processes:
            proc.kill()

    print(results)
    print(f"solution 2: {lowest_location}")


def push_values_through_pipes(seed: SeedPair, map: list[MapRange]) -> list[SeedPair]:
    """
    Map has to be sorted by lowest source start first in list
    """
    seed_start = seed.start
    seed_end = seed.start + seed.range_length - 1
    outputs: list[SeedPair] = []
    for i in range(len(map)):
        pipe = map[i]
        if i == 0 and seed_start < pipe.source_start:
            # we have a gap in front
            if seed_end < pipe.source_start:
                # whole pair fits
                outputs.append(
                    SeedPair(start=seed_start, range_length=seed_end - seed_start + 1)
                )
            else:
                # push through part that fits and move start to pipe start
                new_end = pipe.source_start - 1
                outputs.append(
                    SeedPair(start=seed_start, range_length=new_end - seed_start + 1)
                )
                seed_start = pipe.source_start

        if seed_start >= pipe.source_start:
            if seed_end <= pipe.source_end:
                # the whole pair fit into the pipe -> pushing straight through
                outputs.append(
                    SeedPair(
                        start=pipe.destination_start,
                        range_length=pipe.destination_end - pipe.destination_start + 1,
                    )
                )
            else:
                # could not fit the whole pair -> push through what fits
                range_length = pipe.source_end - seed_start + 1
                outputs.append(SeedPair(start=seed_start, range_length=range_length))
                # move start to one after pipes end
                seed_start = pipe.source_end + 1

                try:
                    next_pipe = map[i + 1]

                    if next_pipe.source_start - pipe.source_end > 1:
                        # we found a gap
                        if seed_end <= next_pipe.source_start:
                            # whole pair fits
                            outputs.append(
                                SeedPair(
                                    start=seed_start,
                                    range_length=seed_end - seed_start + 1,
                                )
                            )
                        else:
                            new_end = next_pipe.source_start - 1
                            outputs.append(
                                SeedPair(
                                    start=seed_start,
                                    range_length=new_end - seed_start + 1,
                                )
                            )
                            seed_start = next_pipe.source_start

                except IndexError:
                    outputs.append(
                        SeedPair(
                            start=seed_start, range_length=seed_end - seed_start + 1
                        )
                    )
                    seed_start = next_pipe.source_start

    return outputs


def pipeline(seed: SeedPair, puzzle_input: PuzzleInputV2, results):
    start_time = time.time()

    soils = push_values_through_pipes(seed, puzzle_input.seeds_to_soil)

    print(f"pushing soils, {len(soils)}")
    for soil in soils:
        fertilizers = push_values_through_pipes(soil, puzzle_input.soil_to_fertilizer)
        print(f"pushing fertilizers, {len(fertilizers)}")
        for fertilizer in fertilizers:
            waters = push_values_through_pipes(
                fertilizer, puzzle_input.fertilizer_to_water
            )
            print(f"pushing waters, {len(waters)}")
            for water in waters:
                lights = push_values_through_pipes(water, puzzle_input.water_to_light)
                print(f"pushing lights, {len(lights)}")
                for light in lights:
                    temperatures = push_values_through_pipes(
                        light, puzzle_input.light_to_temperature
                    )
                    print(f"pushing temperatures, {len(temperatures)}")
                    for temperature in temperatures:
                        humidities = push_values_through_pipes(
                            temperature, puzzle_input.temperature_to_humidity
                        )
                        print(f"pushing humidities, {len(humidities)}")

                        for humidity in humidities:
                            locations = push_values_through_pipes(
                                humidity, puzzle_input.humidity_to_location
                            )
                            sub_minimi = None
                            for location in locations:
                                if not sub_minimi or sub_minimi > location.start:
                                    sub_minimi = location.start
                            if sub_minimi not in results:
                                results.append(sub_minimi)
    end_time = time.time()
    print(f"{SeedPair} duration: {end_time-start_time}")


def solution_2_v2(puzzle_input: PuzzleInputV2):
    results = []
    start_time = time.time()
    manager = Manager()
    results = manager.list()
    processes: list[Process] = []

    try:
        for seed_pair in puzzle_input.seeds_part_2:
            proc = Process(
                target=pipeline,
                args=(seed_pair, puzzle_input, results),
            )
            processes.append(proc)
            proc.start()

        for proc in processes:
            proc.join()
    except KeyboardInterrupt:
        for proc in processes:
            proc.kill()

    # print(f"pushing seeds, {len(puzzle_input.seeds_part_2)}")
    # for seed in puzzle_input.seeds_part_2:
    #     result = pipeline(seed=seed, puzzle_input=puzzle_input)
    #     results.extend(result)
    #     break

    end_time = time.time()
    print(f"duration: {end_time-start_time}")
    results.sort()
    print(f"results: {results}")
    print(f"solution 2: {results[0]}")


def assert_map(data: list[MapRange]):
    length = len(data)
    for i in range(length):
        if i + 1 >= length:
            break
        assert data[i].source_start < data[i + 1].source_start


if __name__ == "__main__":
    if len(sys.argv) == 2:
        challenge_input = sys.argv[1]
        with open(challenge_input, "r") as src:
            puzzle_data = parse_puzzle_input_v2(puzzle_input=src)
        # solution_1(puzzle_input=puzzle_data)
        # print(puzzle_data)
        print("checking maps are sorted... ", end="")
        assert_map(puzzle_data.seeds_to_soil)
        assert_map(puzzle_data.soil_to_fertilizer)
        assert_map(puzzle_data.fertilizer_to_water)
        assert_map(puzzle_data.water_to_light)
        assert_map(puzzle_data.light_to_temperature)
        assert_map(puzzle_data.temperature_to_humidity)
        assert_map(puzzle_data.humidity_to_location)
        print("passed")
        solution_2_v2(puzzle_input=puzzle_data)
