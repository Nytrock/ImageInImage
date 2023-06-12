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
            "The file 'source.jpg' was not found. Check for its presence in the folder with the program and run it again.")
        input()
        return

    try:
        image_for_pixel = Image.open("pixel.jpg")
    except FileNotFoundError:
        write_to_console(
            "The file 'pixel.jpg' was not found. Check for its presence in the folder with the program and run it again.")
        input()
        return

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
    if confirm_working(f"Source image size - {original_width}x{original_height}. "
                       f"Pixel image size - {pixel_image_width}x{pixel_image_height}. "
                       f"Final image size - {result_width}x{result_height}. " + size_message +
                       "Do you want to reduce the size of the images (this will not affect the original files)?"):
        write_to_console("Which image do you want to resize? (s - source, p - pixel)")
        while True:
            answer = input()
            if answer == "s" or answer == "p":
                break
            print("Enter the correct answer.")

        # Change scale of chosen image
        if answer == "s":
            scale = get_image_scale(original, image_for_pixel, "source")
            original = original.resize((ceil(original.size[0] / scale), ceil(original.size[1] / scale)))
            next_question = "pixel"
            size = str(pixel_image_width) + "x" + str(pixel_image_height)
        else:
            scale = get_image_scale(image_for_pixel, original, "pixel")
            image_for_pixel = image_for_pixel.resize((ceil(image_for_pixel.size[0] / scale),
                                                      ceil(image_for_pixel.size[1] / scale)))
            next_question = "source"
            size = str(original_width) + "x" + str(original_height)

        # Change scale of another image
        if confirm_working("Do you also want to reduce the size of the " + next_question + " image? His size now - "
                           + size + f", final image now - {original.size[0] * image_for_pixel.size[0]}x"
                                    f"{original.size[1] * image_for_pixel.size[1]}."):
            if answer == "p":
                scale = get_image_scale(original, image_for_pixel, "source")
                original = original.resize((ceil(original.size[0] / scale), ceil(original.size[1] / scale)))
            else:
                scale = get_image_scale(image_for_pixel, original, "pixel")
                image_for_pixel = image_for_pixel.resize((ceil(image_for_pixel.size[0] / scale),
                                                          ceil(image_for_pixel.size[1] / scale)))

        original_width, original_height = original.size
        pixel_image_width, pixel_image_height = image_for_pixel.size


    write_to_console("Enter the desired title for the final image.")
    name_result = input()
    while name_result in ["", "pixel", "source"]:
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
    if pixel_image_width != pixel_image_height:
        write_to_console("Cropping the secondary image...")
        if not confirm_working("The image that will replace the pixels is not square, "
                               "so it will be automatically cropped around the center. Continue?"):
            write_to_console("Operation aborted.")
            input()
            return
        else:
            image_for_pixel = crop_center(image_for_pixel, min(pixel_image_width, pixel_image_height),
                                          min(pixel_image_width, pixel_image_height))
            pixel_image_width, pixel_image_height = image_for_pixel.size

    # Change the transparency of the main image
    write_to_console("Change the transparency of the main image...")
    original = original.convert("RGBA")
    data = original.getdata()
    newData = []
    for item in data:
        newData.append(item[:-1] + (int(256 * visible),))
    original.putdata(newData)

    # Resizing the main image
    write_to_console("Resizing the main image...")
    original = original.resize((original_width * pixel_image_width, original_height * pixel_image_height))

    # Change the transparency of the secondary image
    write_to_console("Change the transparency of the secondary image...")
    image_for_pixel = image_for_pixel.convert("RGBA")
    data = image_for_pixel.getdata()
    newData = []
    for item in data:
        newData.append(item[:-1] + (int(256 * negative_visible),))
    image_for_pixel.putdata(newData)

    # Final image processing
    loading_final = (original_width - 1) / 100
    for x in range(original_width):
        loading = round(x / loading_final, 3)
        write_to_console(f"Processing - {loading}%")
        for y in range(original_height):
            original.paste(image_for_pixel, (pixel_image_width * x, pixel_image_height * y), mask=image_for_pixel)

    # Converting image to RGB and sava in .jpg
    write_to_console("Saving an image...")
    original = original.convert('RGB')
    original.save(f"{name_result}.jpg")
    write_to_console("Image saved.")
    input()


# Write something to the console
def write_to_console(text: str) -> None:
    if os.name == 'nt':
        x = os.system('cls')
    else:
        x = os.system('clear')
    print(text)


# Confirmation of any action
def confirm_working(text: str) -> bool:
    if os.name == 'nt':
        x = os.system('cls')
    else:
        x = os.system('clear')

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
