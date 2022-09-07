from PIL import Image
import os

Image.MAX_IMAGE_PIXELS = None


def main():
    write_to_console("Подготовка к работе...")

    try:
        original = Image.open("source.jpg")
    except FileNotFoundError:
        write_to_console(
            "Файл 'source.jpg' не обнаружен. Проверьте его наличие в папке с программой и запустите её снова.")
        return

    try:
        image_for_pixel = Image.open("pixel.jpg")
    except FileNotFoundError:
        write_to_console(
            "Файл 'pixel.jpg' не обнаружен. Проверьте его наличие в папке с программой и запустите её снова.")
        return

    original_pixels = original.load()
    original_width, original_height = original.size
    pixel_image_width, pixel_image_height = image_for_pixel.size

    number_of_pixels = original_width * pixel_image_width * original_height * pixel_image_height
    if number_of_pixels >= 10 ** 13:
        if not confirm_working(original_width * pixel_image_width, original_height * pixel_image_height, "Это, скорее всего, сожжёт ваш компьютер."):
            write_to_console("Операция прервана.")
            return
    elif number_of_pixels >= 10 ** 10:
        if not confirm_working(original_width * pixel_image_width, original_height * pixel_image_height, "Это займёт гигантское количество времени."):
            write_to_console("Операция прервана.")
            return
    elif number_of_pixels >= 10 ** 7:
        if not confirm_working(original_width * pixel_image_width, original_height * pixel_image_height, "Это займёт большое количество времени."):
            write_to_console("Операция прервана.")
            return

    write_to_console("Введите желаемое название конечного изображения: ")
    name_result = input()

    write_to_console("Введите степень 'видимости' основного изображения. При 0 изображения не будет видно, а при 1 "
                     "изображение просто увеличится в несколько раз. Стандартным и самым оптимальным является значение 0.5.", True)

    while True:
        try:
            visible = float(input())
            break
        except ValueError:
            pass
    negative_visible = 1 - visible

    write_to_console("Создание изображения нужных размеров...")
    result = Image.new('RGB', (1, 1), color='red')
    try:
        result = Image.new('RGB', (original_width * pixel_image_width, original_height * pixel_image_height), color='red')
    except MemoryError:
        write_to_console("Создаваемое изображение является СЛИШКОМ большим. Уменьшите разрешения "
                         "изображений 'pixel.jpg' и 'source.jpg' и попробуйте сначала.")
    pixels = result.load()
    loading_final = (original_width - 1) / 100

    for x in range(original_width):
        loading = round(x / loading_final, 3)
        write_to_console(f"Обработка - {loading}%")
        for y in range(original_height):
            r_original = visible * original_pixels[x, y][0]
            g_original = visible * original_pixels[x, y][1]
            b_original = visible * original_pixels[x, y][2]
            for pixelX in range(original_width):
                for pixelY in range(original_height):
                    pixel = original_pixels[pixelX, pixelY]
                    pixels[pixelX + original_width * x, pixelY + original_height * y] = (
                        int(pixel[0] * negative_visible + r_original), int(pixel[1] * negative_visible + g_original),
                        int(pixel[2] * negative_visible + b_original))
    write_to_console("Сохранение изображения...")
    result.save(f"{name_result}.jpg")
    write_to_console("Изображение сохранено.")


def write_to_console(text, end=False):
    os.system('cls')
    if end:
        print(text)
    else:
        print(text, end='')


def confirm_working(sizeX, sizeY, text):
    os.system('cls')
    print(
        f"Будет создано изображение размером {sizeX}x{sizeY}. {text} Продолжить? (n/y)")
    while True:
        answer = input()
        if answer == "n":
            return False
        elif answer == "y":
            return True
        else:
            print("Введите корректный ответ (n - нет, y - да)")


if __name__ == '__main__':
    main()
