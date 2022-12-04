def contains(elf1: list[str], elf2: list[str]):
    return int(elf1[0]) >= int(elf2[0]) and int(elf1[1]) <= int(elf2[1])
    

def fully_contained(elf1: list[str], elf2: list[str]):
    return contains(elf1, elf2) or contains(elf2, elf1)    

def overlaps(elf1: list[str], elf2: list[str]):
    first_overlaps = int(elf1[0]) >= int(elf2[0]) and int(elf1[0]) <= int(elf2[1])
    second_overlaps = int(elf1[1]) >= int(elf2[0]) and int(elf1[0]) <= int(elf2[1])
    return first_overlaps or second_overlaps 


def main():
    with open('input.txt', 'r') as input:

        part1_fully_contained_counter = 0
        part2_overlaps_counter = 0
        for line in input:
            elf1_range, elf2_range = [elf_pair.split('-') for elf_pair in line.strip().split(',')]
            if fully_contained(elf1_range, elf2_range):
                part1_fully_contained_counter += 1

            if overlaps(elf1_range, elf2_range):
                part2_overlaps_counter += 1

        print(f'Part 1 result: {part1_fully_contained_counter}')
        print(f'Part 2 result: {part2_overlaps_counter}')



if __name__ == '__main__':
    main()
