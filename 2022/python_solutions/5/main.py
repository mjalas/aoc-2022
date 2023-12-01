import re
from dataclasses import dataclass


def parse_row_into_stacks(stacks: list[list[str]], input: str):
    stack_count = len(stacks)
    current_stack = 0
    space_counter = 0
    next_is_crate = False
    spaces_between_crates = 3

    for char in input:
        c = ord(char)
        
        if space_counter > spaces_between_crates:
            # should be next crate, but missing value
            space_counter = 0
            current_stack += 1

        if next_is_crate:
            next_is_crate = False
            if current_stack >= stack_count:
                current_stack = 0
            stacks[current_stack].insert(0, chr(c))
            current_stack += 1
            continue

        match c:
            case 91:    # [
                space_counter = 0
                next_is_crate = True
            case 93:    # ]
                next_is_crate = False
            case 32:    # space
                space_counter += 1
    
    return stacks

def reverse_stacks(stacks):
    for stack in stacks:
        stack.reverse()
    return stacks

@dataclass
class MoveCommand(object):
    count: int
    from_stack: int
    to_stack: int

    def __str__(self):
        return f'move {self.count} from {self.from_stack} to {self.to_stack}'

def parse_move_command(command: str):
    pattern = re.compile(r"move (?P<count>\d+) from (?P<from>\d+) to (?P<to>\d+)")
    m = pattern.search(command)
    return MoveCommand(count=int(m.group('count')), from_stack=int(m.group('from')), to_stack=int(m.group('to')))

def play_command_part1(command: MoveCommand, stacks: list[list[str]]):

    workable_stacks = copy_stacks(stacks)

    for step in range(command.count):
        from_stack = workable_stacks[command.from_stack-1]
        to_stack = workable_stacks[command.to_stack-1]
        val = from_stack.pop()
        to_stack.append(val)
        workable_stacks[command.from_stack-1] = from_stack
        workable_stacks[command.to_stack-1] = to_stack

    return workable_stacks


def play_command_part2(command: MoveCommand, stacks: list[list[str]]):

        workable_stacks = copy_stacks(stacks)

        # pick up crates from stack
        crates_to_move = []
        from_stack = workable_stacks[command.from_stack-1]
        for step in range(command.count):
            crates_to_move.append(from_stack.pop())

        workable_stacks[command.from_stack-1] = from_stack

        # place crates to new stack
        to_stack = workable_stacks[command.to_stack-1]
        crates_to_move.reverse()
        to_stack += crates_to_move
        workable_stacks[command.to_stack-1] = to_stack

        return workable_stacks


def copy_stacks(stacks_to_copy: list[list[str]]):
        copy = []
        for stack in stacks_to_copy:
            copy.append(stack.copy())
            
        return copy


def stacks_to_printable(stacks: list[list[str]]) -> list[str]:
    stacks_to_print = stacks.copy()
    tallest_stack = 0
    for stack in stacks_to_print:
        if len(stack) > tallest_stack:
            tallest_stack = len(stack)

    outcome = []
    level = tallest_stack - 1
    empty_column = '   '
    space_between_columns = ' '
    while level >= 0:
        current_row = []
        for stack in stacks_to_print:
            if (len(stack) - 1) >= level:
                try:
                    current_row.append(f'[{stack[level]}]')
                except IndexError as err:
                    print(f'Index error for {stack} on level {level}')
                    raise err
            else:
                current_row.append(empty_column)
            current_row.append(space_between_columns)
        level -= 1
        outcome.append(''.join(current_row))
    
    return outcome


def display_stacks(stacks: list[list[str]]):
    outcome = stacks_to_printable(stacks)
    for line in outcome:
        print(line)


def get_top_crates(stacks: list[list[str]]) -> str:
    on_top = []
    for stack in stacks:
        on_top.append(stack[-1])
    
    return ''.join(on_top)


def main():
    
    stack_count = 9
    stacks = [[] for i in range(stack_count)]
    part1_stacks = [[] for i in range(stack_count)]
    part2_stacks = [[] for i in range(stack_count)]
    
    with open('input.txt', 'r') as input:
        stack_setup_parsed = False
        for line in input:
            if line.strip() == '':
                continue
            if line.strip().startswith('1') and not stack_setup_parsed:
                stack_setup_parsed = True
                display_stacks(stacks)
                part1_stacks = copy_stacks(stacks)
                part2_stacks = copy_stacks(stacks)
                continue
            
            if not stack_setup_parsed:
                stacks = parse_row_into_stacks(stacks, line)
            
            if line.strip().startswith('move') and not stack_setup_parsed:
                raise IndexError('Parsing commands before stacks are initialized')

            if line.strip().startswith('move'):
                command = parse_move_command(line)
                part1_stacks = play_command_part1(command, part1_stacks)
                part2_stacks = play_command_part2(command, part2_stacks)
    
    print(f'Part 1 result: {get_top_crates(part1_stacks)}')
    print(f'Part 2 result: {get_top_crates(part2_stacks)}')


if __name__ == '__main__':
    main()
