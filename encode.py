from PIL import Image
import numpy as np


def main():
    width, height = 500, 600

    img = Image.new(mode="RGB", size=(width, height))
    img = np.asarray(img.__array__())
    print(img)

    img.save("debug.png")

if __name__ == '__main__':
    main()
