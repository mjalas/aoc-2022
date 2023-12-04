import re
from dataclasses import dataclass


def parse_card_id(input_str: str) -> int:
    id_pattern = r"Card (?P<id>\s*\d+)"
    res = re.match(id_pattern, input_str)
    if res:
        card_id = int(res.group("id"))
        return card_id
    raise Exception("Could not parse card id")


def parse_numbers_str_collection(numbers_str: str) -> list[int]:
    parts = numbers_str.strip().split(" ")
    numbers = [int(part) for part in parts if part.isdigit()]
    return numbers


def parse_numbers_str_collection_v2(numbers_str: str) -> list[int]:
    numbers_pattern = r"\s*(\d+)\s*"
    numbers = [int(num) for num in re.findall(numbers_pattern, numbers_str)]
    return numbers


@dataclass
class Card:
    id: int
    winning_numbers: list[int]
    gotten_numbers: list[int]
    wins: int
    score: int


def parse_card_line(line: str) -> Card:
    parts = line.strip().split(":")
    card_id = parse_card_id(parts[0])
    number_parts = parts[1].strip().split("|")
    winning_numbers = parse_numbers_str_collection(number_parts[0])
    gotten_numbers = parse_numbers_str_collection(number_parts[1])
    wins, score = calculate_card_wins_and_score(
        gotten_numbers=gotten_numbers, winning_numbers=winning_numbers
    )
    return Card(
        id=card_id,
        winning_numbers=winning_numbers,
        gotten_numbers=gotten_numbers,
        wins=wins,
        score=score,
    )


def parse_card_line_v2(line: str) -> Card:
    pattern = r"Card\s+(?P<id>\d+)\s*:\s+(?P<winnings>(?:\s*\d+\s)+)\s*\|\s*(?P<gotten>(?:\s*\d+\s*)+)\s*"
    parts = re.match(pattern=pattern, string=line.strip())
    if parts:
        card_id = int(parts.group("id"))
        winning_numbers = parse_numbers_str_collection_v2(parts.group("winnings"))
        gotten_numbers = parse_numbers_str_collection_v2(parts.group("gotten"))
        wins, score = calculate_card_wins_and_score(
            gotten_numbers=gotten_numbers, winning_numbers=winning_numbers
        )
        return Card(
            id=card_id,
            winning_numbers=winning_numbers,
            gotten_numbers=gotten_numbers,
            wins=wins,
            score=score,
        )
    raise Exception(f"Could not match number pattern for {line}")


def calculate_card_wins_and_score(
    gotten_numbers: list[int], winning_numbers: list[int]
) -> int:
    first = True
    score = 0
    wins = 0
    for number in gotten_numbers:
        if number in winning_numbers:
            wins += 1
            if first:
                score = 1
                first = False
            else:
                score *= 2
    return wins, score
