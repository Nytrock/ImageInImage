<p align="center"><img src="Logo.jpg" alt="Мона Лиза, состоящая из Мон Лиз"></p>
<p align="center"><i>An example of how the algorithm works. The image has been artificially compressed for stable display.</i></p>

# Image in image
Have you ever dreamed of creating an image that will not consist of solid pixels, but of smaller images? If it is true,
then this program is just what you need! The "Image in image" program allows you to turn any picture into a real masterpiece, without affecting the
original images. At the moment, only the function of creating an image with customizable secondary
(the one to which the pixels will be "replaced" in the final result) and main (the one that will consist of secondary) images. 
Also, directly in the program, you can change the visibility of the main image (at 0, the main image will not be visible, at 1 - the secondary image) and name of final image.
> :exclamation: WARNING :exclamation: Most of the generated images are EXTREMELY heavy and can take a lot of time and computer resources to create. Create large images at your own risk!

# Startup instructions
- Clone the repository

```shell
git clone https://github.com/Nytrock/Image_In_Image.git
```

- Install dependencies with requirements.txt
```shell
pip install -r requirements.txt
```

- Replace the standard `pixel.jpg` and `source.jpg` with the secondary and main images, respectively (if you do not understand which secondary and main images
are talking about, then read the first block!). The secondary image should preferably be square in order to correctly create the image, but in extreme cases, right in the application, you can crop the secondary image relative to the center (the image file will not change)

- Run the program `main.py` and follow the instructions given in iе

- After the completion of the program, you will receive a finished image

- If the image creating is too slow, then reduce the size of `pixel.jpg` and `source.jpg` and restart the program
