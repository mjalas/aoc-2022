

def main():
    input_file = 'input.txt'
    with open(input_file, 'r') as data:
        calorie_items = []
        highest_sum = 0
        sums = []
        for line in data:
            print(line.strip())
            if line.strip():
                val = int(line.strip())
                calorie_items.append(val)
            else:
                sum = 0
                for calorie in calorie_items:
                    sum += calorie
                sums.append(sum)
                if sum > highest_sum:
                    print(f'sum {sum}')
                    highest_sum = sum
                calorie_items = []
        
        sums.sort()
        sums.reverse()
        top_tree = sums[0]
        top_tree += sums[1]
        top_tree += sums[2]
        print(f'top tree: {top_tree}')
        

        print(highest_sum)

if __name__ == '__main__':
    main()
