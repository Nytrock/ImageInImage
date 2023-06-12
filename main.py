import math
import random
from math import ceil

from PIL import Image
import os

Image.MAX_IMAGE_PIXELS = None


def main():
    write_to_console("Preparing for work...")

    # Attempt to open image files, otherwise - error
    try:
        original = Image.open("source.jpg")
    except FileNotFoundError:
        write_to_console(
            "The file 'source.jpg' was not found. Check for its presence in the folder "
            "with the program and run it again.")
        input()
        return

    # Choose mode
    write_to_console("In what mode should the program run? \ns - The final image consists of many identical pictures "
                     "\nm -  The final image consists of many different pictures")
    mode = input()
    while mode not in ["s", "m"]:
        print("Enter the correct answer (s or m)")
        mode = input()
    images = []
    method = ""
    if mode == "s":
        try:
            image_for_pixel = Image.open("pixel.jpg")
        except FileNotFoundError:
            write_to_console(
                "The file 'pixel.jpg' was not found. Check for its presence in the folder "
                "with the program and run it again.")
            input()
            return
        pixel_image_word = "Pixel"
    else:
        # Analyze how many images we have for processing and find smallest
        if not os.path.exists("pixel"):
            write_to_console(
                "Folder 'pixel' not found. Please create a folder 'pixel' and place the images "
                "there that will make up the final image.")
            input()
            return

        content = os.listdir("pixel")
        image_with_min_width = None
        image_with_min_height = None
        for file in content:
            if os.path.isfile("pixel/" + file) and file.endswith('.jpg'):
                image = Image.open("pixel/" + file)
                if image_with_min_width is None or image.width <= image_with_min_width.width:
                    image_with_min_width = image
                if image_with_min_height is None or image.height <= image_with_min_height.height:
                    image_with_min_height = image
                images.append(image)

        if len(images) == 0:
            write_to_console(
                "There no images in 'pixel' folder. Please place in the folder images "
                "there that will make up the final image.")
            input()
            return

        if image_with_min_width.width <= image_with_min_height.height:
            image_for_pixel = image_with_min_width
        else:
            image_for_pixel = image_with_min_height

        # Choosing an image distribution method
        write_to_console("Choose how the pictures will be placed on the final image")
        add_str = ""
        print("r - Images are arranged randomly")
        if len(images) == 2:
            print("c - Images are arranged in a grid (like a chess board)")
            add_str = "c, "
        print("s - The arrangement of images depends on their color matching with the color "
              "of a particular pixel source image (takes the most time)")
        method = input()
        while method not in ["s", "r"]:
            if add_str != "" and method == "c":
                break
            print("Enter the correct answer (r, " + add_str + "s)")
            method = input()
        pixel_image_word = "Smallest pixel"

    # Loading image pixel lists
    original_width, original_height = original.size
    pixel_image_width, pixel_image_height = image_for_pixel.size

    # Checking the size of the final image and changing additional sentence
    size_message = ""
    result_width, result_height = original_width * pixel_image_width, original_height * pixel_image_height
    if result_width * result_height >= 10 ** 16:
        size_message = "This will most likely burn your computer. "
    elif result_width * result_height >= 10 ** 13:
        size_message = "This will take a gigantic amount of time. "
    elif result_width * result_height >= 10 ** 13:
        size_message = "This will take a large amount of time. "

    # Writing about sizes and asking if the images need to be reduced
    if confirm_working(f"Source image size - {original_width}x{original_height}. {pixel_image_word}"
                       f" image size - {pixel_image_width}x{pixel_image_height}. "
                       f"Final image size - {result_width}x{result_height}. {size_message}"
                       "Do you want to reduce the size of the images (this will not affect the original files)?"):
        write_to_console(f"Which image do you want to resize? (s - source, p - {pixel_image_word.lower()})")
        while True:
            answer = input()
            if answer == "s" or answer == "p":
                break
            print("Enter the correct answer.")

        # Change scale of chosen image
        if answer == "s":
            scale = get_image_scale(original, image_for_pixel, "source")
            original = original.resize((ceil(original.size[0] / scale), ceil(original.size[1] / scale)))
            next_question = pixel_image_word.lower()
            size = f"{pixel_image_width}x{pixel_image_height}"
        else:
            scale = get_image_scale(image_for_pixel, original, pixel_image_word.lower())
            image_for_pixel = image_for_pixel.resize((ceil(image_for_pixel.size[0] / scale),
                                                      ceil(image_for_pixel.size[1] / scale)))
            next_question = "source"
            size = f"{original_width}x{original_height}"

        # Change scale of another image
        if confirm_working(f"Do you also want to reduce the size of the {next_question} image? His size now - {size}"
                           f", final image now - {original.size[0] * image_for_pixel.size[0]}x"
                                    f"{original.size[1] * image_for_pixel.size[1]}."):
            if answer == "p":
                scale = get_image_scale(original, image_for_pixel, "source")
                original = original.resize((ceil(original.size[0] / scale), ceil(original.size[1] / scale)))
            else:
                scale = get_image_scale(image_for_pixel, original, pixel_image_word.lower())
                image_for_pixel = image_for_pixel.resize((ceil(image_for_pixel.size[0] / scale),
                                                          ceil(image_for_pixel.size[1] / scale)))

        original_width, original_height = original.size
        pixel_image_width, pixel_image_height = image_for_pixel.size


    write_to_console("Enter the desired title for the final image.")
    name_result = input()
    while name_result in ["", "pixel", "source"] or not is_correct(name_result, "\\|/*<>?:"):
        print("Enter the correct name.")
        name_result = input()


    # Getting the degree of visibility of the main image
    write_to_console(
        "Enter the degree of 'visibility' of the main image. At 0, the image will not be visible, and at 1 "
        "the image will simply be enlarged by several times. The standard and most optimal value is 0.5.")
    while True:
        try:
            visible = float(input())
            if not 0 <= visible <= 1:
                print("Enter a real number BETWEEN 0 and 1.")
            else:
                break
        except ValueError:
            print("Enter the correct answer (real number preferably between 0 and 1)")
    negative_visible = 1 - visible

    # Cut the canvas (if necessary)
    smallest = min(pixel_image_width, pixel_image_height)
    if mode == "s":
        if pixel_image_width != pixel_image_height:
            write_to_console("Cropping the secondary image...")
            image_for_pixel = crop_center(image_for_pixel, smallest, smallest)
            pixel_image_width, pixel_image_height = image_for_pixel.size
    else:
        for i in range(len(images)):
            if images[i].width <= images[i].height:
                images[i] = images[i].resize((pixel_image_width,
                                              int(pixel_image_width / images[i].width * images[i].height)))
            else:
                images[i] = images[i].resize((int(pixel_image_height / images[i].height * images[i].width),
                                              pixel_image_height))
            images[i] = crop_center(images[i], smallest, smallest)
            pixel_image_width, pixel_image_height = images[i].size

    # Change the transparency of the main image
    write_to_console("Change the transparency of the main image...")
    original = original.convert("RGB")
    if method == "s":
        pixels = list(original.getdata())
        origin_colors = [pixels[i * original_width:(i + 1) * original_width] for i in range(original_height)]
    original = original.convert("RGBA")
    data = original.getdata()
    newData = []
    for item in data:
        newData.append(item[:-1] + (int(256 * visible),))
    original.putdata(newData)

    # Resizing the main image
    write_to_console("Resizing the main image...")
    original = original.resize((original_width * pixel_image_width, original_height * pixel_image_height))

    if mode == "s":
        images.append(image_for_pixel)

    # Additional preparation for one of the methods
    images_colors = []
    if method == "s":
        write_to_console("Getting color values for further comparison...")
        for image in images:
            w, h = image.size
            rr, gg, bb = 0, 0, 0
            for x in range(w):
                for y in range(h):
                    r, g, b = image.getpixel((x, y))
                    rr += r
                    gg += g
                    bb += b
            cnt = w * h
            images_colors.append((rr // cnt, gg // cnt, bb // cnt))

    # Change the transparency of all secondary images
    write_to_console(f"Change the transparency of the secondary image{'s' if mode == 'm' else ''}...")
    for i in range(len(images)):
        images[i] = images[i].convert("RGBA")
        data = images[i].getdata()
        newData = []
        for item in data:
            newData.append(item[:-1] + (int(256 * negative_visible),))
        images[i].putdata(newData)

    # Change the transparency of the secondary image
    write_to_console("Change the transparency of the secondary image...")
    image_for_pixel = image_for_pixel.convert("RGBA")
    data = image_for_pixel.getdata()
    newData = []
    for item in data:
        newData.append(item[:-1] + (int(256 * negative_visible),))
    image_for_pixel.putdata(newData)

    # Create a final image depending on the method
    loading_final = (original_width - 1) / 100
    for x in range(original_width):
        loading = round(x / loading_final, 3)
        write_to_console(f"Processing - {loading}%")
        for y in range(original_height):
            if method == "":
                image_to_paste = image_for_pixel
            elif method == "r":
                image_to_paste = random.choice(images)
            elif method == "c":
                image_to_paste = images[(x + y) % 2]
            else:
                target_color = origin_colors[y][x]
                image_to_paste = images[find_closest_color(target_color, images_colors)]
            original.paste(image_to_paste, (pixel_image_width * x, pixel_image_height * y), mask=image_to_paste)


    # Converting image to RGB and sava in .jpg
    write_to_console("Saving an image...")
    original = original.convert('RGB')
    original.save(f"{name_result}.jpg")
    write_to_console("Image saved.")
    input()


# Write something to the console
def write_to_console(text: str) -> None:
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print(text)


# Calculating the distance between colors
def euclidean_distance(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)


# Finding the most similar color
def find_closest_color(target_color, color_list):
    closest_color = None
    min_distance = float('inf')

    for color in color_list:
        distance = euclidean_distance(target_color, color)
        if distance < min_distance:
            min_distance = distance
            closest_color = color

    return color_list.index(closest_color)


# Checking the file name for errors
def is_correct(filename, forbidden_symbols):
    for i in forbidden_symbols:
        if i in filename:
            return False
    return True


# Confirmation of any action
def confirm_working(text: str) -> bool:
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    print(
        f"{text} (n/y)")
    while True:
        answer = input()
        if answer == "n":
            return False
        elif answer == "y":
            return True
        else:
            print("Enter the correct answer (n - no, y - yes)")


# Function for cropping the image in the center
def crop_center(pil_img: Image, crop_width: int, crop_height: int) -> Image:
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


# Getting a new image scale
def get_image_scale(working_image: Image, another_image: Image, image_name: str):
    width, height = working_image.size
    another_width, another_height = another_image.size
    max_scale = min(width, height)

    write_to_console("Enter how many times you want to reduce the size "
                     f"of the " + image_name + f" image (real number between 1 and {max_scale}). "
                                                        f"Image size now - {width}x{height}."
                                                        f" Reducing the size does not affect the original image file. ")

    while True:
        try:
            scale = float(input())
            if 1 <= scale <= max_scale:
                if confirm_working(f"The new size of the " + image_name +
                                   f" image is {int(width // scale)}x{int(height // scale)}, new final image size - "
                                   f"{another_width * int(width // scale)}x{another_height * int(height // scale)}"
                                   f". It suits you?"):
                    break
                else:
                    write_to_console("Enter how many times you want to reduce the size of the "
                                     + image_name + f" image (real number between 1 and {max_scale})")
            else:
                print(f"Enter a real number BETWEEN 1 and {max_scale}.")
        except ValueError:
            print(f"Enter the correct answer (real number between 1 and {max_scale})")

    return scale


# Start
if __name__ == '__main__':
    main()
