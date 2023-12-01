
from sys import argv


if __name__ == '__main__':
    if len(argv) < 2 and len(argv) > 4:
        print('Too few or too many arguments')
        exit()
    
    input_file = argv[1]
    print(f'Parsing lines from {input_file}')
    items = []
    with open(input_file, 'r') as source:
        for line in source:
            items.append(f'"{line.strip()}"')
    
    output_file = 'output.py'
    if len(argv) == 3:
        output_file = argv[2]

    with open(output_file, 'w') as dest:
        dest.write('input = [\n')
        for item in items:
            dest.write(f'\t{item},\n')
        dest.write(']\n')

