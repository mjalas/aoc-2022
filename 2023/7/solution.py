from dataclasses import dataclass
from enum import Enum
import functools
from multiprocessing import Manager, Process
from multiprocessing.managers import ListProxy
import re
import sys
import time
from typing import Callable, Sequence

DEBUG = False

letterCardValues = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
}


class HandType(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


@dataclass
class CardHand:
    hand: str
    bid: int
    type: HandType


def get_cards_in_hand_sorted_by_count(card_hand: str) -> dict[str, int]:
    cards = [*card_hand]
    cards_in_hand = dict((i, cards.count(i)) for i in cards)
    sorted_by_counts = dict(
        sorted(cards_in_hand.items(), key=lambda c: c[1], reverse=True)
    )
    return sorted_by_counts


def get_hand_type_without_jokers(card_hand: str) -> HandType:
    sorted_by_counts = get_cards_in_hand_sorted_by_count(card_hand=card_hand)
    hand_type: HandType
    potential_full_house = False
    potential_two_pair = False
    for card, value in sorted_by_counts.items():
        if value == 5:
            hand_type = HandType.FIVE_OF_A_KIND
            break
        if value == 4:
            hand_type = HandType.FOUR_OF_A_KIND
            break
        if value == 3:
            # either full house or three of a kind
            potential_full_house = True
            continue
        if value == 2:
            if potential_full_house:
                hand_type = HandType.FULL_HOUSE
                break
            elif potential_two_pair:
                hand_type = HandType.TWO_PAIR
                break
            else:
                potential_two_pair = True
        if value == 1:
            if potential_full_house:
                hand_type = HandType.THREE_OF_A_KIND
            elif potential_two_pair:
                hand_type = HandType.ONE_PAIR
            else:
                hand_type = HandType.HIGH_CARD
            break
    return hand_type


def get_hand_type_with_jokers(card_hand: str) -> HandType:
    """Assumption that there is at least one joker"""
    jokers = len([c for c in card_hand if c == "J"])
    if jokers == 5:
        return HandType.FIVE_OF_A_KIND

    joker_free_hand = card_hand.replace("J", "")
    sorted_cards_in_hand = get_cards_in_hand_sorted_by_count(card_hand=joker_free_hand)

    hand_type: HandType = None
    potential_full_house = False
    jokers_in_play = False
    for card, value in sorted_cards_in_hand.items():
        if value + jokers == 5:
            """Options: 4+1 | 3+2 | 2+3 | 1+4 | 0+5"""
            hand_type = HandType.FIVE_OF_A_KIND
            break
        if value + jokers == 4:
            """
            Options: 3+1 | 2+2 | 1+3 | 1+4

            0+4 | 4+0  are not possible options,
            cause either previous would have been true
            and there has to be at least one joker in
            order to end up here
            """
            hand_type = HandType.FOUR_OF_A_KIND
            break
        if not jokers_in_play and value + jokers == 3:
            """
            Options: 2+1 | 1+2

            Other options not possible, since either of previous two would be true
            """
            # either full house or three of a kind
            potential_full_house = True
            jokers_in_play = True
        elif jokers_in_play and potential_full_house and value == 2:
            hand_type = HandType.FULL_HOUSE
            break
        elif not jokers_in_play and value + jokers == 2:
            """Options: 1+1"""
            hand_type = HandType.ONE_PAIR
            break
        elif jokers_in_play and value == 1:
            if potential_full_house:
                hand_type = HandType.THREE_OF_A_KIND
            else:
                hand_type = HandType.HIGH_CARD
            break
    if not hand_type:
        raise Exception(
            f"Could not get hand type for card hand {card_hand}, {jokers=}, {joker_free_hand=}"
        )
    return hand_type


def get_hand_type(card_hand: str, joker: str = "") -> HandType:
    if joker and joker in card_hand:
        # we have joker(s), so handle differently
        return get_hand_type_with_jokers(card_hand)
    else:
        # no joker(s), handle as in part 1
        return get_hand_type_without_jokers(card_hand)


def parse_card_hand_line(line: str, joker: str = "") -> CardHand:
    pattern = r"\s*(?P<hand>[0-9AKQJT]+)\s+(?P<bid>\d+)"
    res = re.match(pattern=pattern, string=line)
    if res:
        hand = res.group("hand")
        bid = int(res.group("bid"))
        return CardHand(
            hand=hand, bid=bid, type=get_hand_type(card_hand=hand, joker=joker)
        )

    raise Exception(f"Could not parse line {line}")


def parse_puzzle_input(
    puzzle_input: Sequence, joker: str = ""
) -> dict[HandType, list[CardHand]]:
    card_hands = {}
    for line in puzzle_input:
        card_hand = parse_card_hand_line(line=line, joker=joker)
        if card_hand.type not in card_hands:
            card_hands[card_hand.type] = []
        card_hands[card_hand.type].append(card_hand)
    return card_hands


def get_card_value(card: str, special_cards: dict[str, int] = {}) -> int:
    if card in special_cards:
        return special_cards[card]

    if card in letterCardValues:
        return letterCardValues[card]

    return int(card)


def get_card_comparer(
    special_cards: dict[str, int]
) -> Callable[[CardHand, CardHand], int]:
    def compare_card_hands_v2(hand_left: CardHand, hand_right: CardHand) -> int:
        for left, right in zip(hand_left.hand, hand_right.hand):
            left_value = get_card_value(left, special_cards=special_cards)
            right_value = get_card_value(right, special_cards=special_cards)
            if left_value != right_value:
                return left_value - right_value
        return 0

    return compare_card_hands_v2


def calculate_winnings_for_hand_type(
    card_hands: list[CardHand],
    start_rank: int,
    special_cards: dict[str, int] = {},
    debug: Callable[[list[str]], None] = None,
):
    card_hands.sort(
        key=functools.cmp_to_key(get_card_comparer(special_cards=special_cards))
    )
    hand_type_winnings = []
    hand_results = []
    for i, hand in enumerate(card_hands):
        rank = start_rank + i
        hand_type_winnings.append(rank * hand.bid)
        if debug:
            hand_results.append(f"{hand.hand}\t{hand.bid}\t{rank}\t{hand.bid*rank}\n")

    if debug:
        debug(hand_results)

    return sum(hand_type_winnings)


def calculate_winnings_for_hand_type_task(
    card_hands: list[CardHand],
    hand_type: HandType,
    start_rank: int,
    results: ListProxy,
    special_cards: dict[str, int] = {},
):
    def debug_calculation(results: list[str]) -> None:
        with open(f"{hand_type.name}.txt", "w") as dest:
            dest.write("Hand\tBid\tRank\t\tScore\n")
            for line in results:
                dest.write(line)

    winnings = calculate_winnings_for_hand_type(
        card_hands=card_hands,
        start_rank=start_rank,
        special_cards=special_cards,
        debug=debug_calculation if DEBUG else None,
    )
    results.append(winnings)


def get_task_result(
    puzzle_input: Sequence, joker: str = "", special_cards: dict[str, int] = {}
) -> None:
    start_time = time.time()
    card_hands = parse_puzzle_input(puzzle_input=puzzle_input, joker=joker)
    manager = Manager()
    results = manager.list()
    processes: list[Process] = []
    start_rank = 1
    try:
        for hand_type in HandType:
            try:
                proc = Process(
                    target=calculate_winnings_for_hand_type_task,
                    args=(
                        card_hands[hand_type],
                        hand_type,
                        start_rank,
                        results,
                        special_cards,
                    ),
                )
                start_rank += len(card_hands[hand_type])
                processes.append(proc)
            except KeyError:
                print(f"Hand type {hand_type} not part of parsed cards")

        for proc in processes:
            proc.start()

        for proc in processes:
            proc.join()
    except KeyboardInterrupt:
        for proc in processes:
            proc.kill()

    winnings = sum(results)
    end_time = time.time()
    print(f"duration: {end_time-start_time}")
    return winnings


def solution_1(puzzle_input: Sequence):
    result = get_task_result(puzzle_input=puzzle_input)
    print(f"solution 1: {result}")


def solution_2(puzzle_input: Sequence):
    result = get_task_result(
        puzzle_input=puzzle_input, joker="J", special_cards={"J": 1}
    )
    print(f"solution 2: {result}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        challenge_input = sys.argv[1]
        with open(challenge_input, "r") as src:
            input_content = src.readlines()
        solution_1(input_content)
        solution_2(input_content)
