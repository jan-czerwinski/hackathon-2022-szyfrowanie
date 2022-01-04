import argparse
from utils import (read_image)

def main():
    print('Script started')
    parser = argparse.ArgumentParser(description='CLI argument processing')
    parser.add_argument('--image_path', required=True, help='Path to image that is meant to be processed')
    args = parser.parse_args()

    print('Reading image')
    img = read_image(args.image_path)
    print(f'Read image with shape{img.shape}')

    letters = []

    with open('w_pustyni_i_w_puszczy.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print(len(lines[0]))

        for letter in lines[0]:
            if letter in letters:
                continue
            letters.append(letter)

        print(len(letters))

        letters.sort()
        print(letters)

    letters = letters[1::]

    width = img.shape[1]
    print(f'Image width:{width}')
    height = img.shape[0]
    print(f'Image height:{height}')


    colours = []
    all_colours = []

    for i in range(1):
        for j in range(width):
            if img[i,j,:].tolist() not in colours and img[i,j,:].tolist() != [0,0,0]:
                colours.append(img[i,j,:].tolist())

    for i in range(height):
        for j in range(width):
            if img[i,j,:].tolist() not in all_colours:
                all_colours.append(img[i,j,:].tolist())

    print(f'All colours amount = {len(all_colours)}')
    print(f'All colours = {all_colours}')

    print(f'Colours in row = {colours}')
    print(f'Amount of colours = {len(colours)}')

    parsed_colours = []

    for colour in colours:
        parsed_colours.append(letters[(sum(colour) % 64) - 1])

    print(f'Letters parsed from colours = {parsed_colours}')


if __name__ == '__main__':
    main()
