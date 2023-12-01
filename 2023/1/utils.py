import re


def find_places_for_digit(line: str, digit: str) -> list[int]:
    locations = []
    str_to_search = line
    print(line)
    prev_index = 0
    while digit in str_to_search:
        i = line.find(digit)
        print(f"found {digit} at {i}")
        locations.append(i+prev_index)
        next_index = i+1
        prev_index = i
        print(f"{next_index}")
        str_to_search = str_to_search[next_index:]
        print(f"next str {str_to_search}")
    return locations


def find_all_digits_in_line(line: str) -> list[str]:
    written_digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    conversion = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}
    
    values = {}
        
    for digit in digits:
        if digit in line:
            #locations = find_places_for_digit(line, digit)
            locations = [m.start() for m in re.finditer(digit, line)]
            for l in locations:
                values[l] = digit
    for digit in written_digits:
        if digit in line:
            #locations = find_places_for_digit(line, digit)
            locations = [m.start() for m in re.finditer(digit, line)]
            for l in locations:
                values[l] = conversion[digit]
    sorted_values = dict(sorted(values.items()))
    res = []
    for key, value in sorted_values.items():
        res.append(value)
    return res