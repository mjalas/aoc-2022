from utils import find_all_digits_in_line


def test_get_all_digits_written_digits():
    test_data = [
        ("two1nine",["2","1","9"]),
        ("eightwothree",["8","2", "3"]),
        ("abcone2threexyz",["1", "2","3"]),
        ("xtwone3four", ["2","1", "3", "4"]),
        ("4nineeightseven2", ["4", "9", "8", "7", "2"]),
        ("zoneight234", ["1", "8", "2", "3", "4"]),
        ("7pqrstsixteen", ["7", "6"]),
        ("7pqrstsixteensix", ["7", "6", "6"]),
        ("7pqrst7sixteen", ["7", "7", "6"])
    ]

    for data in test_data:
        line = data[0]
        print(line)
        res = find_all_digits_in_line(line=line)
        expected = data[1]
        assert res == expected, f"failed on line {line}"

            