
priorities = {
	"a": 1,
	"b": 2,
	"c": 3,
	"d": 4,
	"e": 5,
	"f": 6,
	"g": 7,
	"h": 8,
	"i": 9,
	"j": 10,
	"k": 11,
	"l": 12,
	"m": 13,
	"n": 14,
	"o": 15,
	"p": 16,
	"q": 17,
	"r": 18,
	"s": 19,
	"t": 20,
	"u": 21,
	"v": 22,
	"w": 23,
	"x": 24,
	"y": 25,
	"z": 26,
	"A": 27,
	"B": 28,
	"C": 29,
	"D": 30,
	"E": 31,
	"F": 32,
	"G": 33,
	"H": 34,
	"I": 35,
	"J": 36,
	"K": 37,
	"L": 38,
	"M": 39,
	"N": 40,
	"O": 41,
	"P": 42,
	"Q": 43,
	"R": 44,
	"S": 45,
	"T": 46,
	"U": 47,
	"V": 48,
	"W": 49,
	"X": 50,
	"Y": 51,
	"Z": 52,
}

def split_into_compartments(line: str):
    cleaned_line = line.strip()
    half = len(cleaned_line) // 2
    compartment1, compartment2 = cleaned_line[:half], cleaned_line[half:]
    return compartment1, compartment2


def parse_line_for_part_1(line: str):
    duplicates = [] 
    rucksack_priority_sum = 0
    compartment1, compartment2 = split_into_compartments(line)
    for char in compartment1:
        if char in compartment2:
            duplicates.append(char)
    
    for duplicate in set(duplicates):
        rucksack_priority_sum += priorities[duplicate]

    return rucksack_priority_sum




def parse_line_for_part_2(line: str, counter, group_rucksacks, group_points):

    group_rucksacks.append(line.strip())

    counter += 1
    if counter == 3:

        common = [char for char in group_rucksacks[0] if char in group_rucksacks[1] and char in group_rucksacks[2]]
        group_points.append(priorities[common[0]])
        counter = 0
        group_rucksacks = []
    return group_rucksacks, counter, group_points

def main():
    with open('input.txt', 'r') as input:
        part1_sum = 0
        part2_group_rucksacks = []
        part2_counter = 0
        part2_group_points = []
        
        for line in input:
            part1_sum += parse_line_for_part_1(line)
            part2_group_rucksacks, part2_counter, part2_group_points = parse_line_for_part_2(line, part2_counter, part2_group_rucksacks, part2_group_points)

        print(f'Part 1: sum of priorities: {part1_sum}')
        print(f'Part 2: sum of priorities: {sum(part2_group_points)}')

if __name__ == '__main__':
    main()
