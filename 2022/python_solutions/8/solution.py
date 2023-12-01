def parse_input(input) -> list[list[int]]:
    grid = []
    row = []
    for line in input:
        for char in line.strip():
            row.append(int(char))
        grid.append(row)
        row = []

    return grid


def find_visible_edge_trees_count(input: list[list[int]]) -> int:
    return len(input) * 2 + (len(input[0]) - 2) * 2


def check_left(input: list[int], column: int, val: int) -> bool:
    next_tree_on_left = column - 1
    if next_tree_on_left < 0:
        return True
    tree_on_left = input[next_tree_on_left]
    if tree_on_left < val:
        return check_left(input=input, column=next_tree_on_left, val=val)

    else:
        return False


def count_left(input: list[int], column: int, val: int) -> bool:
    next_tree_on_left = column - 1
    if next_tree_on_left < 0:
        return 0
    tree_on_left = input[next_tree_on_left]

    if tree_on_left < val:
        return 1 + count_left(input=input, column=next_tree_on_left, val=val)

    else:
        return 1


def check_right(input: list[int], column: int, val: int) -> bool:
    next_tree_on_right = column + 1
    if next_tree_on_right >= len(input):
        return True
    tree_on_right = input[next_tree_on_right]
    if tree_on_right < val:
        return check_right(input=input, column=next_tree_on_right, val=val)

    else:
        return False


def count_right(input: list[int], column: int, val: int) -> bool:

    next_tree_on_right = column + 1
    if next_tree_on_right >= len(input):
        return 0
    tree_on_right = input[next_tree_on_right]
    if tree_on_right < val:
        return 1 + count_right(input=input, column=next_tree_on_right, val=val)

    else:
        return 1


def check_up(input: list[list[int]], row: int, column: int, val: int) -> bool:
    next_tree_index = row - 1
    if next_tree_index < 0:
        return True
    next_tree = input[next_tree_index][column]
    if next_tree < val:
        return check_up(input=input, row=next_tree_index, column=column, val=val)

    else:
        return False


def count_up(input: list[list[int]], row: int, column: int, val: int) -> bool:
    next_tree_index = row - 1
    if next_tree_index < 0:
        return 0
    next_tree = input[next_tree_index][column]
    if next_tree < val:
        return 1 + count_up(input=input, row=next_tree_index, column=column, val=val)

    else:
        return 1


def check_down(input: list[list[int]], row: int, column: int, val: int) -> bool:
    next_tree_index = row + 1
    if next_tree_index >= len(input):
        return True
    next_tree = input[next_tree_index][column]
    if next_tree < val:
        return check_down(input=input, row=next_tree_index, column=column, val=val)

    else:
        return False


def count_down(input: list[list[int]], row: int, column: int, val: int) -> bool:
    next_tree_index = row + 1
    if next_tree_index >= len(input):
        return 0
    next_tree = input[next_tree_index][column]
    if next_tree < val:
        return 1 + count_down(input=input, row=next_tree_index, column=column, val=val)

    else:
        return 1


def count_scenic_score_for_tree(grid: list[list[int]], row: int, column: int, val: int):
    return (
        count_up(input=grid, row=row, column=column, val=val)
        * count_down(input=grid, row=row, column=column, val=val)
        * count_left(input=grid[row], column=column, val=val)
        * count_right(input=grid[row], column=column, val=val)
    )


def print_grid(grid: list[list[int]]):
    for row in grid:
        print(row)


def find_highest_scenic_score(grid: list[list[int]]) -> int:
    highest_score = 0

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            score = count_scenic_score_for_tree(
                grid=grid, row=row, column=col, val=grid[row][col]
            )
            if score > highest_score:
                highest_score = score

    return highest_score


def find_visible_middle_trees_count(input: list[list[int]]) -> int:
    count = 0

    for row in range(1, len(input) - 1):
        for col in range(1, len(input[row]) - 1):
            current_tree = input[row][col]
            up = check_up(input=input, row=row, column=col, val=current_tree)
            down = check_down(input=input, row=row, column=col, val=current_tree)
            left = check_left(input=input[row], column=col, val=current_tree)
            right = check_right(input=input[row], column=col, val=current_tree)

            if up or down or left or right:
                count += 1

    return count


def main():
    with open("input.txt", "r") as input:
        grid = parse_input(input)

    edge_trees_visible = find_visible_edge_trees_count(input=grid)
    middle_trees_visible = find_visible_middle_trees_count(input=grid)

    part1 = edge_trees_visible + middle_trees_visible
    print(f"Part 1: {part1}")

    part2 = find_highest_scenic_score(grid)
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
