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
    numbers = []
    for part in parts:
        if part.isdigit():
            numbers.append(int(part))
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
