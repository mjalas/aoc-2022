from dataclasses import dataclass
import re
from enum import Enum


class SystemEntity:
    def __init__(self, name: str, parent: any, size: int) -> None:
        self.name = name
        self.parent = parent
        self.size = size

    def update_size(self, size):
        self.size = size


class SystemFile(SystemEntity):
    def __init__(self, name: str, size: int, parent: SystemEntity) -> None:
        super().__init__(name=name, parent=parent, size=size)

    def __str__(self):
        return f"SystemFile(name={self.name}, size={self.size})"


class SystemDir(SystemEntity):
    def __init__(self, name: str, parent: SystemEntity) -> None:
        super().__init__(name=name, parent=parent, size=0)
        self.children: list[SystemEntity] = []

    def __str__(self):
        return f"SystemDir(name={self.name}, size={self.size})"

    def add_child(self, child: SystemEntity):
        self.children.append(child)

    def navigate(self, name: str):
        if name == "..":
            return self.parent
        else:
            nextEntity = None
            for child in self.children:
                if child.name == name:
                    nextEntity = child
            return nextEntity


class CommandType(Enum):
    CD = "cd"
    LS = "ls"


class Command(object):
    def __init__(self, value: CommandType, parameter: str | None) -> None:
        self.value = value
        self.parameter = parameter

    def __str__(self):
        if self.parameter:
            return f"$ {self.value} {self.parameter}"
        return f"$ {self.value}"


class CDCommand(Command):
    def __init__(self, parameter: str):
        super().__init__(value=CommandType.CD.value, parameter=parameter)


class LSOutputType(Enum):
    FILE = 1
    DIR = 2


@dataclass
class LSOutputLine:
    name: str
    type: LSOutputType
    size: int

    def __str__(self):
        if self.type == LSOutputType.FILE:
            return f"{self.size} {self.name}"
        if self.type == LSOutputType.DIR:
            return f"dir {self.name}"
        raise Exception("File type not supported")


class LSCommand(Command):
    def __init__(self) -> None:
        super().__init__(value=CommandType.LS.value, parameter=None)
        self.outputs: list[LSOutputLine] = []

    def add_output(self, output_line: LSOutputLine):
        self.outputs.append(output_line)

    def __str__(self):
        outputs = "\n".join([str(output) for output in self.outputs])
        return f"$ {self.value}\n{outputs}"


def parse_command(command: str) -> Command:
    if command.strip() == "$ ls":
        # handle list dir
        return LSCommand()

    if command.strip().startswith("$ cd"):
        pattern = re.compile(r"\$ cd (?P<parameter>[a-z|/|..]+)")
        m = pattern.search(command)
        if not m:
            raise Exception(f"Failed to match patter with {command}")
        return CDCommand(parameter=m.group("parameter"))

    raise Exception(f"Non supported command: {input}")


def parse_ls_output_line(line: str) -> LSOutputLine:
    if line.strip().startswith("dir"):
        name = line.strip().split(" ")[1]
        return LSOutputLine(name=name, type=LSOutputType.DIR, size=0)

    pattern = re.compile(r"(?P<size>\d+) (?P<name>[a-z|\.]+)")
    m = pattern.search(line)
    if not m:
        raise Exception(f"Could not match LS input for file {input}")
    return LSOutputLine(
        name=m.group("name"), type=LSOutputType.FILE, size=int(m.group("size"))
    )


def parse_input(input):
    current_command = None
    commands = []
    for line in input:
        if line.startswith("$"):
            current_command = parse_command(line)
            commands.append(current_command)

        else:
            if type(current_command) is LSCommand:
                parsed_line = parse_ls_output_line(line)
                current_command.add_output(parsed_line)
    return commands


def commands_to_output(commands: list[Command]) -> list[str]:
    output = []
    for command in commands:
        if type(command) is CDCommand:
            output.append(str(command))
        elif type(command) is LSCommand:
            command_output = str(command).split("\n")
            output.extend(command_output)

    return output


def build_tree(commands: list[Command]) -> SystemDir:
    root = SystemDir(name="/", parent=None)

    current_folder = root

    for command in commands:
        if type(command) is CDCommand:
            if command.parameter == "/":
                current_folder = root
            else:
                nextEntity = current_folder.navigate(command.parameter)
                if nextEntity is None:
                    raise Exception(
                        f"Could not navigate to {command.paramenter} from {current_folder.name}"
                    )
                current_folder = nextEntity

        elif type(command) is LSCommand:
            for output in command.outputs:
                if output.type == LSOutputType.DIR:
                    current_folder.add_child(
                        SystemDir(name=output.name, parent=current_folder)
                    )
                elif output.type == LSOutputType.FILE:
                    current_folder.add_child(
                        SystemFile(
                            name=output.name, size=output.size, parent=current_folder
                        )
                    )
                else:
                    raise Exception(f"LS type {output.type} is not supported")
    return root


def system_entity_to_output(entity: SystemEntity, level=0) -> list[str]:

    parent_tabs = "\t" * level
    output = [f"{parent_tabs}- {entity.name} (dir)"]

    if type(entity) is SystemDir:
        for child in entity.children:
            if type(child) is SystemDir:
                if level < 8:
                    child_output = system_entity_to_output(child, level=level + 1)
                output.extend(child_output)
            if type(child) is SystemFile:
                child_tabs = "\t" * (level + 1)
                output.append(f"{child_tabs}- {child.name} (file, size={child.size})")

    return output


def update_directory_size(entity: SystemDir, level=0) -> int:
    if level >= 15:
        return  # fail safe
    dir_size = 0

    for child in entity.children:
        if type(child) is SystemDir:
            child_dir_size = update_directory_size(child, level=level + 1)
            dir_size += child_dir_size
        if type(child) is SystemFile:
            dir_size += child.size
    entity.update_size(dir_size)
    return dir_size


def get_all_dirs(entity: SystemDir):
    dirs = [entity]

    for child in entity.children:
        if type(child) is SystemDir:
            childs_dirs = get_all_dirs(child)
            dirs.extend(childs_dirs)

    return dirs


def find_directiories_with_max_size(dirs: list[SystemDir], max_size: int):
    result = []
    for dir in dirs:
        if dir.size < max_size:
            result.append(dir)
    return result


def dir_size_less_than_or_equal(size: int):
    def compare(dir: SystemDir):
        return dir.size <= size

    return compare


def get_occupied_space(entity: SystemEntity) -> int:
    """Get occupied space from files in the tree"""
    size = 0
    if type(entity) == SystemFile:
        size += entity.size

    for child in entity.children:
        if type(child) == SystemDir:
            size += get_occupied_space(child)
        if type(child) == SystemFile:
            size += child.size

    return size


def main():
    with open("input.txt", "r") as input:
        commands = parse_input(input)

    root = build_tree(commands)
    update_directory_size(root)
    dirs = get_all_dirs(root)

    part1_dirs = filter(dir_size_less_than_or_equal(100000), dirs)
    part1_sum = 0
    for dir in part1_dirs:
        part1_sum += dir.size

    print(f"Part1: {part1_sum}")

    total_space = 70000000
    needed_free_space = 30000000
    used_space = get_occupied_space(root)
    free_space = total_space - used_space
    minimum_space_to_free = needed_free_space - free_space

    def dirs_bigger_than_or_equal(size: int):
        def compare(entity: SystemDir):
            return entity.size >= size

        return compare

    part2_dirs = list(filter(dirs_bigger_than_or_equal(minimum_space_to_free), dirs))

    def sort_dir(entity: SystemDir):
        return entity.size

    part2_dirs.sort(key=sort_dir)

    part2_res = None
    for dir in part2_dirs:
        if dir.size >= minimum_space_to_free:
            part2_res = dir
            break

    print(f"Part2: {part2_res.size}")


if __name__ == "__main__":
    main()
