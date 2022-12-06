import pytest

from solution import find_first_marker, find_first_message_marker

@pytest.mark.parametrize('input, expected', [
    ('bvwbjplbgvbhsrlpgdmjqwftvncz',  5),
    ('nppdvjthqldpwncqszvftbrmjlhg', 6),
    ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 10),
    ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 11),
])
def test_find_first_marker(input, expected):
    
    result = find_first_marker(input)
    assert result == expected


@pytest.mark.parametrize('input, expected', [
    ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 19),
    ('bvwbjplbgvbhsrlpgdmjqwftvncz', 23),
    ('nppdvjthqldpwncqszvftbrmjlhg', 23),
    ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 29),
    ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 26)
])
def test_find_first_message_marker(input, expected):
    
    result = find_first_message_marker(input)
    assert result == expected
