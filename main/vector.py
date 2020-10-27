import cv2
from pathlib import Path
import numpy as np
from main.settings import load_config


def create_vector(filename):
    path = Path(__file__).parent / f'upload/{filename}'
    img = cv2.imread(str(path))
    size = load_config().get('size')
    img = cv2.resize(img, size)

    arr = np.asarray(img, dtype='uint8')
    norm_arr = np.reshape(arr / 255., size[0] * size[1] * 3)
    return norm_arr


def euclidean(a, b):
    a = np.array(a)
    b = np.array(b)
    dist = np.linalg.norm(a - b)
    return dist
