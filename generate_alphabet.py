
def generate_alphabet_list():
    alphabet = []
    for i in range(97, 123):
        alphabet.append(chr(i))
    return alphabet

def generate_day_3_priorities():
    alphabet = []
    priority = 1
    for i in range(97, 123):
        alphabet.append((chr(i), priority))
        priority += 1
    for i in range(65, 91):
        alphabet.append((chr(i), priority))
        priority += 1
    
    with open('output.py', 'w') as dest:
        dest.write('priorities = {\n')
        for item in alphabet:
            dest.write(f'\t"{item[0]}": {item[1]},\n')
        dest.write('}')
    return alphabet

if __name__ == '__main__':
    alphabet = generate_day_3_priorities()
    print(alphabet)