from solution import (
    parse_card_hand_line,
    CardHand,
    get_hand_type_without_jokers,
    HandType,
    parse_puzzle_input,
    calculate_winnings_for_hand_type,
)

example_input = ["32T3K 765", "T55J5 684", "KK677 28", "KTJJT 220", "QQQJA 483"]


def test_parse_input():
    input_lines: list[CardHand] = []
    for line in example_input:
        input_lines.append(parse_card_hand_line(line))

    assert input_lines[0].hand == "32T3K"
    assert input_lines[0].bid == 765


def test_get_hand_type():
    test_data = [
        ("32T3K", HandType.ONE_PAIR),
        ("T55J5", HandType.THREE_OF_A_KIND),
        ("KK677", HandType.TWO_PAIR),
        ("KTJJT", HandType.TWO_PAIR),
        ("QQQQA", HandType.FOUR_OF_A_KIND),
        ("AAAAA", HandType.FIVE_OF_A_KIND),
        ("AAAKK", HandType.FULL_HOUSE),
        ("AKQJT", HandType.HIGH_CARD),
    ]

    for data in test_data:
        hand_type = get_hand_type_without_jokers(data[0])
        assert hand_type == data[1], f"Failed for hand {data[0]}"


def test_get_result_part1():
    expected = 6440
    card_hands = parse_puzzle_input(example_input)
    results = []
    start_rank = 1
    for hand_type in HandType:
        try:
            result = calculate_winnings_for_hand_type(
                card_hands=card_hands[hand_type], start_rank=start_rank
            )
            start_rank += len(card_hands[hand_type])
            results.append(result)
        except KeyError:
            print(f"Hand type {hand_type} not part of parsed cards")
    assert sum(results) == expected


def test_get_result_part2():
    expected = 5905
    card_hands = parse_puzzle_input(example_input, joker="J")
    results = []
    start_rank = 1
    for hand_type in HandType:
        try:
            result = calculate_winnings_for_hand_type(
                card_hands=card_hands[hand_type],
                start_rank=start_rank,
                special_cards={"J": 1},
            )
            start_rank += len(card_hands[hand_type])
            results.append(result)
        except KeyError:
            print(f"Hand type {hand_type} not part of parsed cards")
    assert sum(results) == expected
