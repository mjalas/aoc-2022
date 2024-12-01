from collections import Counter

challenge_input = "./input.txt"


def read_input():
    with open(challenge_input, "r") as src:
        return [line.strip() for line in src]


def parse_input_to_columns(input_lines: list[str]) -> tuple[list[str], list[str]]:
    leftCol = []
    rightCol = []

    for line in input_lines:
        parts = [x for x in line.strip().split(" ") if len(x) > 0]
        if len(parts) != 2:
            print(parts)
            print("Invalid input")
            return 1
        leftCol.append(parts[0])
        rightCol.append(parts[1])

    return leftCol, rightCol


def part1(input_lines: list[str]) -> int:

    leftCol, rightCol = parse_input_to_columns(input_lines)
    leftCol = sorted(leftCol)
    rightCol = sorted(rightCol)
    distance_sum = 0
    for items in zip(leftCol, rightCol):
        distance = abs(int(items[0]) - int(items[1]))

        distance_sum += distance

    return distance_sum


def part2(input_lines: list[str]) -> int:
    similarityScoreSum = 0
    leftCol, rightCol = parse_input_to_columns(input_lines)
    appearences = Counter(rightCol)
    # print(appearences)
    for item in leftCol:
        score = int(item) * appearences[item]
        similarityScoreSum += score

    return similarityScoreSum


def main():
    input_lines = read_input()
    sol1 = part1(input_lines)
    print(f"Part 1: {sol1}")
    sol2 = part2(input_lines)
    print(f"Part 2: {sol2}")


if __name__ == "__main__":
    main()
