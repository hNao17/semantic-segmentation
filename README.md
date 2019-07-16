## Overview
In this repository, I worked with the [KITTI semantic segmentation dataset](http://www.cvlibs.net/datasets/kitti/eval_semseg.php?benchmark=semantics2015) [1] to explore both binary and multi-class segmentation of autonomous driving scenes.

## Data
The semantic segmentation dataset consists of 200 train and test images (each) and can be downloaded [here](http://www.cvlibs.net/download.php?file=data_semantics.zip). Additionally, [a development kit is provided] (https://s3.eu-central-1.amazonaws.com/avg-kitti/devkit_semantics.zip), which offers helper functions that map pixel colours to class labels. There are a total of 35 labeled classes that are unevenly distributed throughout the dataset. The figures below show the distribution of classes on both a per image and per pixel basis.

![alt_text](images/kitti_segmentation_class_distribution_per_image.png)

![alt_text](images/kitti_segmentation_class_distribution_per_pixel.png)

## Architecture
I used an encoder-decoder architecture that was based on the popular U-Net architecture[2]. The network accepts as an input a 3-channel Height x Width x 3 RGB image, downsamples the image with the encoder branch of the network and then recovers the image's original resolution using the network's decoder branch. The final output is a tensor of size Height x Width x NClasses. For binary segmentation, NClasses = 2. 

## Training

## References

[1]: Geiger, Andreas, et al. "Vision meets robotics: The KITTI dataset." The International Journal of Robotics Research 32.11 (2013): 1231-1237.

[2]: Ronneberger, Olaf, Philipp Fischer, and Thomas Brox. "U-net: Convolutional networks for biomedical image segmentation." International Conference on Medical image computing and computer-assisted intervention. Springer, Cham, 2015.
