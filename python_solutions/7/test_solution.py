import pytest


from solution import (
    parse_input,
    commands_to_output,
    parse_command,
    Command,
    LSCommand,
    CDCommand,
    parse_ls_output_line,
    LSOutputLine,
    LSOutputType,
    system_entity_to_output,
    build_tree,
    update_directory_size,
    get_all_dirs,
    dir_size_less_than_or_equal,
)


@pytest.mark.parametrize(
    "input, expected",
    [
        ("$ cd /", CDCommand(parameter="/")),
        ("$ cd ..", CDCommand(parameter="..")),
        ("$ cd a", CDCommand(parameter="a")),
        ("$ cd abc", CDCommand(parameter="abc")),
        ("$ ls", LSCommand()),
    ],
)
def test_parse_command(input: str, expected: Command):
    result = parse_command(input)
    assert result.value == expected.value
    assert result.parameter == expected.parameter


@pytest.mark.parametrize(
    "input, expected",
    [
        ("dir a", LSOutputLine(name="a", type=LSOutputType.DIR, size=0)),
        (
            "14848514 b.txt",
            LSOutputLine(name="b.txt", type=LSOutputType.FILE, size=14848514),
        ),
        (
            "8504156 c.dat",
            LSOutputLine(name="c.dat", type=LSOutputType.FILE, size=8504156),
        ),
    ],
)
def test_parse_ls_output_line(input: str, expected):

    result = parse_ls_output_line(input)

    assert str(result) == str(expected)


def test_input_parsing():
    input = [
        "$ cd /",
        "$ ls",
        "dir a",
        "14848514 b.txt",
        "8504156 c.dat",
        "dir d",
        "$ cd a",
        "$ ls",
        "dir e",
        "29116 f",
        "2557 g",
        "62596 h.lst",
        "$ cd e",
        "$ ls",
        "584 i",
        "$ cd ..",
        "$ cd ..",
        "$ cd d",
        "$ ls",
        "4060174 j",
        "8033020 d.log",
        "5626152 d.ext",
        "7214296 k",
    ]

    commands = parse_input(input)

    output = commands_to_output(commands)

    assert len(input) == len(output)

    for i in range(len(input)):
        assert input[i] == output[i]


def test_parse_input_to_tree():
    input = [
        "$ cd /",
        "$ ls",
        "dir a",
        "14848514 b.txt",
        "8504156 c.dat",
        "dir d",
        "$ cd a",
        "$ ls",
        "dir e",
        "29116 f",
        "2557 g",
        "62596 h.lst",
        "$ cd e",
        "$ ls",
        "584 i",
        "$ cd ..",
        "$ cd ..",
        "$ cd d",
        "$ ls",
        "4060174 j",
        "8033020 d.log",
        "5626152 d.ext",
        "7214296 k",
    ]

    expected = [
        "- / (dir)",
        "\t- a (dir)",
        "\t\t- e (dir)",
        "\t\t\t- i (file, size=584)",
        "\t\t- f (file, size=29116)",
        "\t\t- g (file, size=2557)",
        "\t\t- h.lst (file, size=62596)",
        "\t- b.txt (file, size=14848514)",
        "\t- c.dat (file, size=8504156)",
        "\t- d (dir)",
        "\t\t- j (file, size=4060174)",
        "\t\t- d.log (file, size=8033020)",
        "\t\t- d.ext (file, size=5626152)",
        "\t\t- k (file, size=7214296)",
    ]

    commands = parse_input(input)
    root = build_tree(commands)

    outcome = system_entity_to_output(root)
    assert len(outcome) == len(expected)

    for i in range(len(outcome)):
        assert outcome[i] == expected[i]


def test_find_directories_with_max_size_of_100000():
    input = [
        "$ cd /",
        "$ ls",
        "dir a",
        "14848514 b.txt",
        "8504156 c.dat",
        "dir d",
        "$ cd a",
        "$ ls",
        "dir e",
        "29116 f",
        "2557 g",
        "62596 h.lst",
        "$ cd e",
        "$ ls",
        "584 i",
        "$ cd ..",
        "$ cd ..",
        "$ cd d",
        "$ ls",
        "4060174 j",
        "8033020 d.log",
        "5626152 d.ext",
        "7214296 k",
    ]

    expected_directories = ["a", "e"]

    commands = parse_input(input)
    root = build_tree(commands)

    update_directory_size(root)
    dirs = get_all_dirs(root)

    expected = {"e": 584, "a": 94853, "d": 24933642, "/": 48381165}

    for dir in dirs:
        assert dir.size == expected[dir.name]

    matching_dirs = filter(dir_size_less_than_or_equal(100000), dirs)

    size_sums = 0
    for dir in matching_dirs:
        size_sums += dir.size
        assert dir.name in expected_directories

    assert size_sums == 95437
