import os
import glob

import numpy as np
from PIL import Image


def split_file(path, chunk_size=50000000):
    file_number = 1
    filename = os.path.basename(path)
    with open(path, "rb") as f:
        chunk = f.read(chunk_size)
        while chunk:
            with open(
                os.path.join(
                    os.path.dirname(path), filename + ".part" + str(file_number)
                ),
                "wb",
            ) as chunk_file:
                chunk_file.write(chunk)
            file_number += 1
            chunk = f.read(chunk_size)


def merge_files(prefix, dirname):
    """
    Each file has a .part<num> suffix

    prefix: The name of the output merged file
    dirname: Directory containing the split files to be merged

    This function will find all the parts and merge them
    """
    files = glob.glob(os.path.join(dirname, prefix) + "*")
    files = list(files)

    files_sorted = []
    for i in range(1, len(files) + 1):
        part_filename = prefix + ".part" + str(i)
        if os.path.exists(os.path.join(dirname, part_filename)):
            files_sorted.append(os.path.join(dirname, part_filename))

    mergedBytes = b""
    for fn in files_sorted:
        with open(fn, "rb") as fp:
            mergedBytes += fp.read()

    with open(os.path.join(dirname, prefix), "wb") as fp:
        fp.write(mergedBytes)


def u2net_clothes_split_mask(
    image: Image,
    w_split: int = 1,
    h_split: int = 3,
):
    w = image.width // w_split
    h = image.height // h_split

    nd_image = np.array(image)

    image_slices = [
        nd_image[x : x + h, y : y + w]
        for x in range(0, nd_image.shape[0], h)
        for y in range(0, nd_image.shape[1], w)
    ]

    mask_list = []
    for mask in image_slices:
        test_mask = Image.fromarray(mask)

        # checks if any mask are empty (all black/white)
        if not sum(test_mask.convert("L").getextrema()) in (
            0,
            2,
        ):
            mask = Image.fromarray(mask)
            mask_list.append(mask)

    return mask_list
