from PIL import Image
import numpy as np


def read_image(path: str) -> np.ndarray:
    img = Image.open(path)
    img = img.convert('HSV')
    img = np.asarray(img.__array__())
    return img
