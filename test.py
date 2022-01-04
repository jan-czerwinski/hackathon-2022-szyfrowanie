def main():
    with open('w_pustyni_i_w_puszczy.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        letters = []

        for letter in lines[0]:
            if letter in letters:
                continue
            letters.append(letter)

        print(len(letters))

        letters.sort()
        print(letters)

if __name__ == '__main__':
    main()
