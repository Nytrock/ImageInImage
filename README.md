<p align="center"><img src="Logo.jpg" alt="Mona Lisa, consisting of Mona Lisa"></p>
<p align="center"><i>An example of how the algorithm works. The image has been artificially compressed for stable display.</i></p>

# Image in image
Have you ever dreamed of creating an image that will not consist of solid pixels, but of smaller images? If it is true,
then this program is just what you need! The "Image in image" program allows you to turn any picture into a real masterpiece, without affecting the
original images. You can create both a picture consisting of the same image, and a picture consisting of completely different images (the location of these images is also customizable, read below).
Also, directly in the program, you can change the visibility of the main image (at 0, the main image will not be visible, at 1 - the secondary image), name of final image, size of main and secondary images 
(not affect original files).
> :exclamation: WARNING :exclamation: Most of the generated images are EXTREMELY heavy and can take a lot of time and computer resources to create. Create large images at your own risk!

# Instructions for use
- Download latest release

- Replace the standard `pixel.jpg` and `source.jpg` with the secondary and main images, respectively (if you do not understand which secondary and main images are talking about, then read the first block!). If you wanna to make an image consisting of DIFFERENT images, then create a folder `pixel` and put all the secondary images there

- Run `main.exe` and follow application instructions

- After the completion of the program, you will receive a finished image

# Instruction for modes and methods
As mentioned above, the program has 2 modes: in the first, the final image consists of many identical images, in the second - from many different images. The second mode also has 3 methods for positioning secondary images on the main one:
1. Random (r). Secondary images are randomly placed
2. Grid (c). Available only if the number of secondary images is two. Secondary images alternate and eventually form something similar to a chessboard
3. Selective (s). For each pixel of the main image, the most suitable secondary image in color is selected (because of this, this method is the slowest)
<p align="center">
  <img src="Examples of using modes/res1.jpg" heigth=auto width=33% alt="Example of using random method">
  <img src="Examples of using modes/res2.jpg" heigth=auto width=33% alt="Example of using grid method">
  <img src="Examples of using modes/res3.jpg" heigth=auto width=33% alt="Example of using selective method">
</p>

<p align="center">
  <i>These are examples of random, grid and selective methods, respectively.</i>
</p>

# Instructions for running the source code
- Clone the repository

```shell
git clone https://github.com/Nytrock/ImageInImage.git
```

- Install dependencies with requirements.txt
```shell
pip install -r requirements.txt
```

- Do the same thing you would do when working with released application
