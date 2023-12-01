import sys
from utils import find_all_digits_in_line

def first_challenge(challenge_input) -> int:
    
    with open(challenge_input, "r") as src:
        sum = 0
        rows = 0
        for line in src:
            #print(line)
            first_int = ""
            last_int = ""
            for c in line:
                if c.isdigit():
                    if first_int == "":
                        first_int = c
                    last_int = c
            
            num = int(f"{first_int}{last_int}")
            sum += num
            #print(num)
            
        return sum

def second_challenge(challenge_input) -> int:
    sum = 0
    with open(challenge_input, "r") as src:
        for line in src:
            digits = find_all_digits_in_line(line)
            first = digits[0]
            last = digits[-1]
            num = int(f"{first}{last}")
            sum += num

    return sum

if __name__ == "__main__":
    if len(sys.argv) == 2:
        challenge_input = sys.argv[1]
        res_1 = first_challenge(challenge_input=challenge_input)
        print(f"first: {res_1}")
        res_2 = second_challenge(challenge_input=challenge_input)
        print(f"second: {res_2}")