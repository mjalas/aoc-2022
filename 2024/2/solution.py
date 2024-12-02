def is_increasing(first: int, second: int) -> bool:
    return first < second


def are_values_increasing(values: list[int]) -> bool:
    for i in range(len(values) - 1):
        if not is_increasing(values[i], values[i + 1]):
            return False
    return True


def valid_diff(first: int, second: int) -> bool:
    return 1 <= abs(first - second) <= 3


def are_values_decreasing(values: list[int]) -> bool:
    for i in range(len(values) - 1):
        if is_increasing(values[i], values[i + 1]):
            return False
    return True


def are_values_diff_valid(values: list[int]) -> bool:
    for i in range(len(values) - 1):
        if not valid_diff(values[i], values[i + 1]):
            return False
    return True


def is_report_safe(report_values: list[int]) -> bool:

    return are_values_diff_valid(report_values) and (
        are_values_increasing(report_values) or are_values_decreasing(report_values)
    )


def part1(inputs: list[str]) -> int:
    safe_count = 0
    for line in inputs:
        report_values = [int(x) for x in line.strip().split(" ")]
        if is_report_safe(report_values):
            safe_count += 1

    return safe_count


def read_input(challenge_input: str) -> list[str]:
    with open(challenge_input, "r") as src:
        return [line.strip() for line in src]


if __name__ == "__main__":
    challenge_input = "./input.txt"
    inputs = read_input(challenge_input)
    print(f"part 1: {part1(inputs)}")
