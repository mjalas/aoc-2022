

def main():
    with open('input.txt', 'r') as input:

        columns = 9
        spaces_between_columns = 3
        stacks = [[]] * columns
        print(stacks)

        for line in input:
            if line.startswith('move'):
                break
            print(line.strip())
            char_codes = []
            for char in line.strip():
                char_codes.append(ord(char))
            print(char_codes)
            


if __name__ == '__main__':
    main()
