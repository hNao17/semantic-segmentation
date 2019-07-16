import cv2 as cv
import glob
import matplotlib.pyplot as plt
import numpy as np
import os

from kitti_labels import labels

########################################################################################################################
# Helper functions


def calculate_class_frequency(img, id_to_colour, class_frequency_per_img, class_frequency_per_pixel):

    for id in id_to_colour:
        r, g, b = id_to_colour[id]
        colour = [b, g, r]

        mask_channel = np.all(img == colour, axis=-1)
        num_pixels = np.sum(mask_channel > 0)
        if num_pixels > 0:
            class_frequency_per_img[id] += 1
            class_frequency_per_pixel[id] += num_pixels


def plot_histogram(id_to_name, class_frequency_per_img, class_frequency_per_pixel, n_classes, n_images, n_pixels):

    kwargs = {'height': 0.5, 'align': 'center', 'color': 'mediumvioletred'}

    # image frequencies
    plt.figure(0)
    sorted_img_frequencies = sorted(class_frequency_per_img.items(), key=lambda kv: kv[1], reverse=True)
    img_frequencies = [kv[1] for kv in sorted_img_frequencies]
    img_class_names = [id_to_name[kv[0]] for kv in sorted_img_frequencies]

    plt.barh(y=img_class_names, width=img_frequencies, **kwargs)
    plt.xlabel("# of Images", fontsize=24)
    plt.ylabel("Classes", fontsize=24)
    plt.title("Class Distribution per Image", fontsize=28)
    plt.xticks(ticks=range(0, n_images+10, 10), labels=np.arange(0, n_images+10, step=10), fontsize=12, rotation=0)
    plt.yticks(fontsize=12)

    # pixel frequencies
    plt.figure(1)
    sorted_pixel_frequencies = sorted(class_frequency_per_pixel.items(), key=lambda kv: kv[1], reverse=True)
    pixel_frequencies = [100 * kv[1] / n_pixels for kv in sorted_pixel_frequencies]
    pixel_class_names = [id_to_name[kv[0]] for kv in sorted_pixel_frequencies]

    plt.barh(y=pixel_class_names, width=pixel_frequencies, **kwargs)
    plt.xlabel("Pixel Frequency [%]", fontsize=20)
    plt.ylabel("Classes", fontsize=20)
    plt.title("Class Distribution per Pixel", fontsize=28)
    plt.xticks(ticks=range(0, 110, 10), labels=np.arange(0, 110, step=10), fontsize=12, rotation=0)
    plt.yticks(fontsize=12)

    plt.show()

########################################################################################################################
# Main


if __name__ == "__main__":

    # Get class ids / names / colours
    id_to_name_dict = {label.id: label.name for label in labels}
    id_to_colour_dict = {label.id: label.color for label in labels}
    class_frequency_per_img_dict = {label.id: 0 for label in labels}
    class_frequency_per_pixel_dict = {label.id: 0 for label in labels}
    n_classes = len(class_frequency_per_img_dict.keys())
    print("# of classes: {}".format(n_classes))

    # Open images in train folder
    root_dir = "data/Kitti"
    train_dir = "train"
    gt_dir = "semantic_rgb"

    filenames = glob.glob(os.path.join(root_dir, train_dir, gt_dir, "*.png"))
    n_images = len(filenames)
    n_pixels = 0
    for i, fn in enumerate(filenames):
        img = cv.imread(fn)
        pixel_count = img.shape[0] * img.shape[1]
        n_pixels += pixel_count
        calculate_class_frequency(img, id_to_colour_dict, class_frequency_per_img_dict, class_frequency_per_pixel_dict)

    # print class statistics
    print("Total # of images: {}".format(n_images))
    print("Total # of pixels: {}".format(n_pixels))
    for i in range(n_classes):
        name = id_to_name_dict[i]
        img_count = class_frequency_per_img_dict[i] # / n_images
        pixel_count = class_frequency_per_pixel_dict[i] / n_pixels
        print("Class {} - # of Images: {}, Pixel Frequency: {}".format(name, img_count, pixel_count))

    # Visualize class statistics
    plot_histogram(id_to_name_dict,
                   class_frequency_per_img_dict,
                   class_frequency_per_pixel_dict,
                   n_classes, n_images, n_pixels)