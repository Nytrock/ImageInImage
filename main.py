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
        return

    try:
        image_for_pixel = Image.open("pixel.jpg")
    except FileNotFoundError:
        write_to_console(
            "The file 'pixel.jpg' was not found. Check for its presence in the folder with the program and run it again.")
        return

    # Loading image pixel lists
    original_width, original_height = original.size
    pixel_image_width, pixel_image_height = image_for_pixel.size

    # Checking the size of the final image and confirming the start of its creation
    number_of_pixels = original_width * pixel_image_width * original_height * pixel_image_height
    if number_of_pixels >= 10 ** 16:
        if not confirm_working(f"An image of size {original_width * pixel_image_width}x"
                               f"{original_height * pixel_image_height} will be created. "
                               f"This will most likely burn your computer."):
            write_to_console("Operation aborted.")
            return
    elif number_of_pixels >= 10 ** 13:
        if not confirm_working(f"An image of size {original_width * pixel_image_width}x"
                               f"{original_height * pixel_image_height} will be created. "
                               f"This will take a gigantic amount of time."):
            write_to_console("Operation aborted.")
            return
    elif number_of_pixels >= 10 ** 10:
        if not confirm_working(f"An image of size {original_width * pixel_image_width}x"
                               f"{original_height * pixel_image_height} will be created. "
                               f"This will take a large amount of time."):
            write_to_console("Operation aborted.")
            return

    write_to_console("Enter the desired title for the final image: ")
    name_result = input()

    # Getting the degree of visibility of the main image
    write_to_console(
        "Enter the degree of 'visibility' of the main image. At 0, the image will not be visible, and at 1 "
        "the image will simply be enlarged by several times. The standard and most optimal value is 0.5.", True)
    while True:
        try:
            visible = float(input())
            # Getting the degree of visibility of the main image
            if not 0 <= visible <= 1:
                text = "less than 0."
                if visible > 1:
                    text = "greater than 1."
                if confirm_working(f"You have chosen a value {text} "
                                   "This can greatly distort the final image and lead to unexpected results."):
                    break
                else:
                    write_to_console(
                        "Enter the degree of 'visibility' of the main image. At 0, the image will not be visible, and at 1 "
                        "the image will simply be enlarged by several times. The standard and most optimal value is 0.5.",
                        True)
            else:
                break
        except ValueError:
            print("Enter the correct answer (real number preferably between 0 and 1)")
    negative_visible = 1 - visible

    # Cut the canvas (if necessary)
    if pixel_image_width != pixel_image_height:
        write_to_console("Cropping the secondary image...")
        if not confirm_working("The image that will replace the pixels is not square, so it will be automatically cropped around the center."):
            write_to_console("Operation aborted.")
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


# Write something to the console
def write_to_console(text: str, end=False) -> None:
    os.system('cls')
    if end:
        print(text)
    else:
        print(text, end='')


# Confirmation of any action
def confirm_working(text: str) -> bool:
    os.system('cls')
    print(
        f"{text} Continue? (n/y)")
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


# Start
if __name__ == '__main__':
    main()
