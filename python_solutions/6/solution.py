
def find_first_marker(input: str) -> int:
    marker = []
    counter = 0
    for c in input:
        counter += 1
        marker.append(c)

        if len(marker) == 4:
            if len(set(marker)) == len(marker):
                return counter
            marker.pop(0)
    return 0


def find_first_message_marker(input: str) -> int:
        marker = []
        counter = 0
        for c in input:
            counter += 1
            marker.append(c)

            if len(marker) == 14:
                if len(set(marker)) == len(marker):
                    return counter
                marker.pop(0)
        return 0


def main():
    with open('input.txt', 'r') as input:
        line = input.readlines()[0]
        marker_end = find_first_marker(line)
        print(f'Part 1: {marker_end}')
        message_marker_end = find_first_message_marker(line)
        print(f'Part 2: {message_marker_end}')


if __name__ == '__main__':
    main()
        