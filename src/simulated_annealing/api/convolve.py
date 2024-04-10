""" Implement the convolute command.

The 2D convolution is a fairly simple operation at heart: you start with a kernel,
which is simply a small matrix of weights. This kernel "slides" over the 2D input data,
performing an elementwise multiplication with the part of the input it is currently on,
and then summing up the results into a single output pixel.

https://towardsdatascience.com/intuitively-understanding-convolutions-for-deep-learning-1f6f42faee1
"""
import numpy as np

try:
    # for visual mode. `pip install -e .[visual]`
    import matplotlib.pyplot as plt
    import seaborn as sns
except ModuleNotFoundError:
    plt = None
    sns = None

from ..core.logger import logger


            # plt.plot(steps, delta_history, marker='o')
            # plt.title('Delta E over Time')
            # plt.xlabel('Step')
            # plt.ylabel('Delta E Value')
            # plt.show()

def convolution2D(image2d, kernel3x3) -> np.ndarray:
    """ Execute the command.
    
    :param image2d: Image read into np.ndarray of 2 dimensions.
    :type image2d: np.ndarray
    :param kernel3x3: Convolution kernel of size (3, 3).
    :type kernel3x3: np.ndarray
    :return: The convolved image.
    :rtype: np.ndarray
    """
    convolved2d = np.zeros((len(image2d)-2, len(image2d)-2))
    # TODO: Code here
    return convolved2d


def main(image_filename:str) -> np.ndarray:
    """ Execute the command.
    
    :param image_filename: Name of a file. Use .csv for now.
    :type image_filename: str
    :return: The convolved image.
    :rtype: np.ndarray
    """
    logger.debug('executing convolve command')
    assert image_filename is not None and isinstance(image_filename, str)
    if plt is None:
        logger.warning('Visual mode not installed. `pip install -e .[visual]`')

    # Load image
    image2d = np.loadtxt(image_filename, delimiter=',')
    if plt is not None:
        sns.heatmap(image2d, cmap='gray')
        plt.title(f'Original image - Size = {image2d.shape}')
        plt.show()

    # Kernel
    edge_detect_filter_3x3 = np.array([[-1, -1, -1],[-1, 8, -1],[-1, -1, -1]])

    # Convolution
    for i in range(2):
        convolved_image = convolution2D(image2d, edge_detect_filter_3x3)
        if plt is not None:
            sns.heatmap(convolved_image, cmap='gray')
            plt.title(f'Convolution iteration {i} - Size = {convolved_image.shape}')
            plt.show()
        image2d = convolved_image
    return image2d


if __name__ == '__main__':
    main()
