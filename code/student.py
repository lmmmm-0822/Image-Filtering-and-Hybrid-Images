# Project Image Filtering and Hybrid Images Stencil Code
# Based on previous and current work
# by James Hays for CSCI 1430 @ Brown and
# CS 4495/6476 @ Georgia Tech
import numpy as np
from numpy import pi, exp, sqrt
from skimage import io, img_as_ubyte, img_as_float32
from skimage.transform import rescale

def my_imfilter(image, filter):
    """
  Your function should meet the requirements laid out on the project webpage.
  Apply a filter to an image. Return the filtered image.
  Inputs:
  - image -> numpy nd-array of dim (m, n, c)
  - filter -> numpy nd-array of odd dim (k, l)
  Returns
  - filtered_image -> numpy nd-array of dim (m, n, c)
  Errors if:
  - filter has any even dimension -> raise an Exception with a suitable error message.
  """
    
    im_dim=image.shape
    flt_dim=filter.shape
    filtered_image = np.zeros(image.shape)
    img_dim1=im_dim[0]
    img_dim2=im_dim[1]
    flt_dim1=flt_dim[0]
    flt_dim2=flt_dim[1]
    pad_dim1=int((flt_dim1-1)/2)
    pad_dim2=int((flt_dim2-1)/2)
    pad_mat=np.zeros((img_dim1+2*pad_dim1,img_dim2+2*pad_dim2,3))
    pad_mat[pad_dim1: img_dim1 + pad_dim1, pad_dim2: img_dim2 + pad_dim2] = image
    for d in range(len(image[0][0])):
        for i in range(len(image)):
            for j in range(len(image[0])):
                filtered_image[i][j][d]=sum(sum(np.multiply(filter,pad_mat[i:i+flt_dim1,j:j+flt_dim2,d])))
 
    return filtered_image

def gen_hybrid_image(image1, image2, cutoff_frequency):
    """
     Inputs:
     - image1 -> The image from which to take the low frequencies.
     - image2 -> The image from which to take the high frequencies.
     - cutoff_frequency -> The standard deviation, in pixels, of the Gaussian
                           blur that will remove high frequencies.

     Task:
     - Use my_imfilter to create 'low_frequencies' and 'high_frequencies'.
     - Combine them to create 'hybrid_image'.
    """

    assert image1.shape[0] == image2.shape[0]
    assert image1.shape[1] == image2.shape[1]
    assert image1.shape[2] == image2.shape[2]

    """
     Steps:
     (1) Remove the high frequencies from image1 by blurring it. The amount of
         blur that works best will vary with different image pairs
     generate a 1x(2k+1) gaussian kernel with mean=0 and sigma = s,
     see https://stackoverflow.com/questions/17190649/how-to-obtain-a-gaussian-filter-in-python
    """    
    s, k = cutoff_frequency, cutoff_frequency * 2
    probs = np.asarray([exp(-z * z / (2 * s * s)) / sqrt(2 * pi * s * s) for z in range(-k, k + 1)], dtype=np.float32)
    kernel = np.outer(probs, probs)

    """
     Your code here:
     low_frequencies = np.zeros(image1.shape)  # Replace with your implementation
    """
    
    low_frequencies = my_imfilter(image1, kernel)

    """
     (2) Remove the low frequencies from image2. The easiest way to do this is to
         subtract a blurred version of image2 from the original version of image2.
         This will give you an image centered at zero with negative values.
     Your code here #
     high_frequencies = np.zeros(image1.shape)  # Replace with your implementation
    """
    high_frequencies = image2 - my_imfilter(image2, kernel)
    
    
    # 归一化到[0, 1]
    high_frequencies = np.clip(high_frequencies, 0, 1)
    
    """
     
     (3) Combine the high frequencies and low frequencies
     Your code here #
     hybrid_image = np.zeros(image1.shape)  # Replace with your implementation
     """
    
    hybrid_image = np.add(low_frequencies, high_frequencies, )
    

    """
     (4) At this point, you need to be aware that values larger than 1.0
     or less than 0.0 may cause issues in the functions in Python for saving
     images to disk. These are called in proj1_part2 after the call to 
     gen_hybrid_image().
     One option is to clip (also called clamp) all values below 0.0 to 0.0, 
     and all values larger than 1.0 to 1.0.

    """
    hybrid_image = np.clip(hybrid_image, 0, 1)

    return low_frequencies, high_frequencies, hybrid_image

def vis_hybrid_image(hybrid_image):
  scales = 5
  scale_factor = [0.5, 0.5, 1]
  padding = 5
  original_height = hybrid_image.shape[0]
  num_colors = 1 if hybrid_image.ndim == 2 else 3

  output = np.copy(hybrid_image)
  cur_image = np.copy(hybrid_image)
  for scale in range(2, scales+1):
    # add padding
    output = np.hstack((output, np.ones((original_height, padding, num_colors),
                                        dtype=np.float32)))
    # downsample image
    cur_image = rescale(cur_image, scale_factor, mode='reflect')
    # pad the top to append to the output
    pad = np.ones((original_height-cur_image.shape[0], cur_image.shape[1],
                   num_colors), dtype=np.float32)
    tmp = np.vstack((pad, cur_image))
    output = np.hstack((output, tmp))
  return output

def load_image(path):
  return img_as_float32(io.imread(path))

def save_image(path, im):
  return io.imsave(path, img_as_ubyte(im.copy()))
