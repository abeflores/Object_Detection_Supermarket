# Script to create hard links at dir a from files in dir b

import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Moving Data")
    parser.add_argument(
        "data_folder",
        type=str,
        help=("Full path to the directory having all original data"),
    )
    parser.add_argument(
        "destination_folder",
        type=str,
        help=("Full path to the folder where data is going to"),
    )

    args = parser.parse_args()

    return args


def get_data(data_folder, destination_folder):
    # Images
    images_path = os.path.join(data_folder, "images")
    images_list_names = os.listdir(images_path)
    for img in images_list_names:
        orig_img_file = os.path.join(images_path, img)
        dest_img_file = os.path.join(destination_folder, "images", img)
        if not os.path.isfile(dest_img_file):
            os.link(orig_img_file, dest_img_file)
    # Annotations
    annot_path = os.path.join(data_folder, "annotations")
    annot_list_names = os.listdir(annot_path)
    for annot in annot_list_names:
        orig_annot_file = os.path.join(annot_path, annot)
        dest_annot_file = os.path.join(destination_folder, "annotations", annot)
        if not os.path.isfile(dest_annot_file):
            os.link(orig_annot_file, dest_annot_file)


if __name__ == "__main__":
    args = parse_args()
    get_data(args.data_folder, args.destination_folder)
