import os
import sys
import re
import numpy as np
from skimage import io
from skimage.transform import rescale
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor
import argparse
from tqdm import tqdm


'''
    convert jpg to npy on ssd for accelerated loading
'''
parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, required=True)
parser.add_argument('--output', type=str, required=True)

args = parser.parse_args()
img_paths = os.listdir(args.input)

def loadAndSave(img_path):
    img = io.imread(os.path.join(args.input, img_path)).astype(np.float32)
    img = rescale(img, (0.5,0.5,1)).transpose(2,0,1) / 255.0
    img_path = re.sub('.jpg', '.npy', img_path)
    np.save(os.path.join(args.output, img_path), img)

# Process and exec
with ProcessPoolExecutor(max_workers=8) as pool:
    pbar = tqdm(desc='imgs', total=len(img_paths))
    img_run = {}
    for path in img_paths:
        img_run[pool.submit(loadAndSave, path)] = None

    for future in concurrent.futures.as_completed(img_run):
        pbar.update(1)
