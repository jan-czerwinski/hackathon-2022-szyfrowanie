import argparse
from utils import (read_image)
from PIL import Image
import numpy as np

def main():
    print('Script started')
    parser = argparse.ArgumentParser(description='CLI argument processing')
    parser.add_argument('--image_path', required=True, help='Path to image that is meant to be processed')
    args = parser.parse_args()

    print('Reading image')
    img = read_image(args.image_path)
    print(f'Read image with shape{img.shape}')

    letters = []

    # with open('w_pustyni_i_w_puszczy.txt', 'r', encoding='utf-8') as f:
    #     lines = f.readlines()
    #     print(len(lines[0]))

    #     for letter in lines[0]:
    #         if letter in letters:
    #             continue
    #         letters.append(letter)

    #     print(len(letters))

    #     letters.sort()
    #     print(letters)

    letters = letters[1::]

    width = img.shape[1]
    height = img.shape[0]
    # print(f'Image width:{width}')
    # print(f'Image height:{height}')

    all_colours = []

    for i in range(height):
        for j in range(width):
            if img[i,j,:].tolist() not in all_colours:
                # print(f'({i}, {j})')
                all_colours.append(img[i,j,:].tolist())

    # vertices = detect_vertices(img)

    # for pair in vertices:
    #     img[pair[0], pair[1]] = [255, 255, 255]

    # img_with_letters = Image.fromarray(img)
    # img_with_letters.save('vertices.png')

    stats = colors_statistics(img)
    print(stats)

    img_after_detection = detect_words(img, stats, treshold=800)
    img = Image.fromarray(img_after_detection)
    img.save('detected.png')

def colors_statistics(img):
    width = img.shape[1]
    height = img.shape[0]

    statistics = {}

    for i in range(height):
        for j in range(width):
            color = np.array2string(img[i,j,:])
            if color not in statistics:
                statistics[color] = 1
            else:
                statistics[color] += 1

    return statistics

def slice_to_chunks(img):
    print(img.shape)
    height, width = img.shape[:2]
    chunks_amount_w = width // 50
    chunks_amount_h = height // 50

    for i in range(chunks_amount_h-1):
        for j in range(chunks_amount_w-1):
            chunk = img[i * 50:(i+1)*50, j*50:(j+1)*50]
            im = Image.fromarray(chunk)
            im.save(f'chunks/{i}__{j}.png')

def check_to_group(c1, c2, diff=1):
    if abs(c1[0] - c2[0]) <= diff and c1[0] != c2[0]:
        return True
    
    if abs(c1[1] - c2[1]) <= diff and c1[1] != c2[1]:
        return True
    
    if abs(c1[2] - c2[2]) <= diff and c1[2] != c2[2]:
        return True

    return False
    
def group_colors(all_colors):
    grouped_colors = []
    grouped_id = []

    for i in range(len(all_colors) - 1):
        tmp_group = [all_colors[i]]
        for j in range(i + 1, len(all_colors)):
            if check_to_group(all_colors[i], all_colors[j]):
                if j not in grouped_id:
                    grouped_id.append(j)
                else:
                    continue
                tmp_group.append(all_colors[j])

        grouped_colors.append(tmp_group)

    return grouped_colors

def sum_neighbors(chunk):
    sum = 0

    for i in range(chunk.shape[0]):
        for j in range(chunk.shape[1]):
            if chunk[i, j].tolist() != chunk[1, 1].tolist():
                sum += 1

    return sum

def check_if_edge(chunk):
    # left top
    if chunk[0, 0].tolist() != chunk[1,1].tolist() and chunk[0,1].tolist() != chunk[1,1].tolist() and chunk[1,0].tolist() != chunk[1,1].tolist():
        return False
    # right top
    if chunk[0, 2].tolist() != chunk[1,1].tolist() and chunk[0,1].tolist() != chunk[1,1].tolist() and chunk[1,2].tolist() != chunk[1,1].tolist():
        return False
    # left bottom
    if chunk[2, 0].tolist() != chunk[1,1].tolist() and chunk[1,0].tolist() != chunk[1,1].tolist() and chunk[2,1].tolist() != chunk[1,1].tolist():
        return False
    # right bottom
    if chunk[2, 1].tolist() != chunk[1,1].tolist() and chunk[2,2].tolist() != chunk[1,1].tolist() and chunk[1,2].tolist() != chunk[1,1].tolist():
        return False

    return True
    

def detect_vertices(img):
    height, width = img.shape[:2]
    vertices = []

    for i in range(height):
        for j in range(width):
            if i == 0 or i == height - 1:
                pass

            if j == 0 or j == width - 1:
                pass
            
            chunk = img[i-1:i+2, j-1:j+2]
            if sum_neighbors(chunk) >= 3:
                if not check_if_edge(chunk):
                    vertices.append((i, j))
                    
    return vertices

def detect_words(img, stats, treshold=1000):
    height, width = img.shape[:2]

    for i in range(height):
        for j in range(width):
            if i == 0 or i == height - 1:
                pass

            if j == 0 or j == width - 1:
                pass
            
            color = np.array2string(img[i,j,:])
            if stats[color] <= treshold:
                img[i,j,:] = [255,255,255]

    return img
                    
            

if __name__ == '__main__':
    main()
