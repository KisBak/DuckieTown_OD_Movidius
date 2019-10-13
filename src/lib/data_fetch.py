import Augmentor

def get_keras_generator(images_dir, batch_size = 100):
    """Returns default Augmentor which enlarges dataset on-the-fly
    It changes the colors, saturation, contrast,... of the pictures

    Parameters:
    images_dir (string): Path to the pictures directory

    Returns:
    Keras generator: Returns a keras generator

    """

    p = Augmentor.Pipeline(images_dir)

    p.random_distortion(0.3, grid_width=10, grid_height=10, magnitude=10)
    p.greyscale(0.3)
    p.invert(0.05)
    p.random_brightness(0.7)
    p.random_color(0.7, min_factor=0.6, max_factor=1.3)
    p.random_contrast(0.7, min_factor=0.6, max_factor=1.3)
    p.skew(0.3, magnitude=0.1)

    return p.keras_generator(batch_size)
