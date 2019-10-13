# DuckieTown_OD_Movidius

## Used data to teach

The used data originates from the [darknet](https://github.com/marquezo/darknet) github repository. The dataset contains 420 labeled images where the labeling is attached in a separate text file. In order to enlarge the dataset, we use [Augmentor](https://github.com/mdbloice/Augmentor) for generating images with slightly different properties. The tool is able to generate the images on the fly, implementing a keras generator, so storing the generated images is not neccessary. For example import, see the proper example directory.
