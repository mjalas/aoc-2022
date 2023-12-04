from utils import parse_card_line


def test_example_sol1():
    input_str = [
        "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\n",
        "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19\n",
        "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1\n",
        "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83\n",
        "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36\n",
        "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11\n",
    ]
    expected_per_input_line = [8, 2, 2, 1, 0, 0]
    expected = 13

    scores = []
    for i, line in enumerate(input_str):
        expected_card_score = expected_per_input_line[i]
        card = parse_card_line(line)
        assert (
            card.score == expected_card_score
        ), f"Got {card.score} but expected {expected_card_score}"
        scores.append(card.score)

    result = sum(scores)
    assert result == expected, f"Got total score {result} but expected {expected}"


def test_parse():
    input_str = "Card  1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\n"

    card = parse_card_line(input_str)

    assert card.id == 1
    assert card.winning_numbers == [41, 48, 83, 86, 17]
    assert card.gotten_numbers == [83, 86, 6, 31, 17, 9, 48, 53]


def test_example_sol2():
    input_str = [
        "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\n",
        "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19\n",
        "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1\n",
        "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83\n",
        "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36\n",
        "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11\n",
    ]

    expected_wins_of_each = [4, 2, 2, 1, 0, 0]
    expected_count_of_each = [1, 2, 4, 8, 14, 1]
    expected_total = 30
    card_counts: dict[int, int] = {}
    for i, line in enumerate(input_str):
        expected_win_count = expected_wins_of_each[i]
        card = parse_card_line(line)
        if card.id not in card_counts:
            card_counts[card.id] = 1
        else:
            card_counts[card.id] += 1

        for copy in range(card_counts[card.id]):
            for i in range(card.id + 1, card.id + card.wins + 1):
                if i not in card_counts:
                    card_counts[i] = 1
                else:
                    card_counts[i] += 1

        assert (
            card.wins == expected_win_count
        ), f"Got {card.wins} wins but expected {expected_win_count}"

    for i in range(len(expected_count_of_each)):
        assert card_counts[i + 1] == expected_count_of_each[i], f"Failed for card {i+1}"

    result = sum(list(card_counts.values()))
    assert result == expected_total
