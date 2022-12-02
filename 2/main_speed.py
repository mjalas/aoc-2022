from enum import Enum
import asyncio
from input import input

class Choice(Enum):
    Rock = 1
    Paper = 2
    Scissor = 3

class ExpectedOutcome(Enum):
    Win = 6
    Tie = 3
    Loose = 0


options = {
    'A X': Choice.Scissor.value + ExpectedOutcome.Loose.value,
    'A Y': Choice.Rock.value + ExpectedOutcome.Tie.value,
    'A Z': Choice.Paper.value + ExpectedOutcome.Win.value,
    'B X': Choice.Rock.value + ExpectedOutcome.Loose.value,
    'B Y': Choice.Paper.value + ExpectedOutcome.Tie.value,
    'B Z': Choice.Scissor.value + ExpectedOutcome.Win.value,
    'C X': int(Choice.Paper.value) + int(ExpectedOutcome.Loose.value),
    'C Y': int(Choice.Scissor.value) + int(ExpectedOutcome.Tie.value),
    'C Z': int(Choice.Rock.value) + int(ExpectedOutcome.Win.value)
}


def main():
    result = 0
    for line in input:
        score = options[line.strip()]
        result += score
    print(result)

if __name__ == '__main__':
    main()
