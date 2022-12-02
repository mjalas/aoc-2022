from enum import Enum


class Choice(Enum):
    Rock = 1
    Paper = 2
    Scissor = 3

class ExpectedOutcome(Enum):
    Win = 1
    Tie = 2
    Loose = 3

opponent_choices = {
    'A': Choice.Rock,
    'B': Choice.Paper,
    'C': Choice.Scissor
}

you_choices = {
    'X': Choice.Rock,
    'Y': Choice.Paper,
    'Z': Choice.Scissor
}

expected_outcomes = {
    'X': ExpectedOutcome.Loose,
    'Y': ExpectedOutcome.Tie,
    'Z': ExpectedOutcome.Win
}

def battle_part1(opponent: Choice, you: Choice) -> int:
    match opponent:
        case Choice.Rock:
            match you:
                case Choice.Rock:
                    return 3
                case Choice.Paper:
                    return 6
                case Choice.Scissor:
                    return 0
        case Choice.Paper:
            match you:
                case Choice.Rock:
                    return 0
                case Choice.Paper:
                    return 3
                case Choice.Scissor:
                    return 6
        case Choice.Scissor:
            match you:
                case Choice.Rock:
                    return 6
                case Choice.Paper:
                    return 0
                case Choice.Scissor:
                    return 3

def figure_out_choice(opponent: Choice, outcome: ExpectedOutcome) -> Choice:
    match opponent:
        case Choice.Rock:
            match outcome:
                case ExpectedOutcome.Win:
                    return Choice.Paper
                case ExpectedOutcome.Tie:
                    return Choice.Rock
                case ExpectedOutcome.Loose:
                    return Choice.Scissor
        case Choice.Paper:
            match outcome:
                case ExpectedOutcome.Win:
                    return Choice.Scissor
                case ExpectedOutcome.Tie:
                    return Choice.Paper
                case ExpectedOutcome.Loose:
                    return Choice.Rock
        case Choice.Scissor:
            match outcome:
                case ExpectedOutcome.Win:
                    return Choice.Rock
                case ExpectedOutcome.Tie:
                    return Choice.Scissor
                case ExpectedOutcome.Loose:
                    return Choice.Paper

def main():
    with open('input.txt', 'r') as data:
        your_score = 0
        for line in data:
            choices = line.strip().split(' ')
            opponents_choice = opponent_choices[choices[0]]
            your_choice = figure_out_choice(opponent=opponents_choice, outcome=expected_outcomes[choices[1]])
            your_score += your_choice.value + battle_part1(opponents_choice, your_choice)
        
        print(f'Your score {your_score}')


if __name__ == '__main__':
    main()
