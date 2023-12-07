from dataclasses import dataclass
from enum import Enum
import re


cardTypes = [
    "A",
    "K",
    "Q",
    "J",
    "T",
    "9",
    "8",
    "7",
    "6",
    "5",
    "4",
    "3",
    "2",
]

letterCardValues = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
}


@dataclass
class InputLine:
    card_hand: str
    bid: int


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


def get_hand_type(card_hand: str) -> HandType:
    cards = [*card_hand]
    cards_in_hand = dict((i, cards.count(i)) for i in cards)
    sorted_by_counts = dict(
        sorted(cards_in_hand.items(), key=lambda c: c[1], reverse=True)
    )
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


def parse_card_hand_line(line: str) -> CardHand:
    pattern = r"\s*(?P<hand>[0-9AKQJT]+)\s+(?P<bid>\d+)"
    res = re.match(pattern=pattern, string=line)
    if res:
        hand = res.group("hand")
        bid = int(res.group("bid"))
        return CardHand(hand=hand, bid=bid, type=get_hand_type(hand))

    raise Exception(f"Could not parse line {line}")
