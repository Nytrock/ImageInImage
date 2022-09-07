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
        pixel_image = Image.open("pixel.jpg")
    except FileNotFoundError:
        write_to_console(
            "Файл 'pixel.jpg' не обнаружен. Проверьте его наличие в папке с программой и запустите её снова.")
        return

    pixels_original = original.load()
    xOrig, yOrig = original.size
    xPixel, yPixel = pixel_image.size

    number_of_pixels = xOrig * xPixel * yOrig * yPixel
    if number_of_pixels >= 10 ** 13:
        if not confirm_working(xOrig * xPixel, yOrig * yPixel, "Это, скорее всего, сожжёт ваш компьютер."):
            write_to_console("Операция прервана.")
            return
    elif number_of_pixels >= 10 ** 10:
        if not confirm_working(xOrig * xPixel, yOrig * yPixel, "Это займёт гигантское количество времени."):
            write_to_console("Операция прервана.")
            return
    elif number_of_pixels >= 10 ** 7:
        if not confirm_working(xOrig * xPixel, yOrig * yPixel, "Это займёт большое количество времени."):
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
        result = Image.new('RGB', (xOrig * xPixel, yOrig * yPixel), color='red')
    except MemoryError:
        write_to_console("Создаваемое изображение является СЛИШКОМ большим. Уменьшите разрешения "
                         "изображений 'pixel.jpg' и 'source.jpg' и попробуйте сначала.")
    pixels = result.load()
    loading_final = (xOrig - 1) / 100

    for x in range(xOrig):
        loading = round(x / loading_final, 3)
        write_to_console(f"Обработка - {loading}%")
        for y in range(yOrig):

            middleR = visible * pixels_original[x, y][0]
            middleG = visible * pixels_original[x, y][1]
            middleB = visible * pixels_original[x, y][2]
            for pixelX in range(xOrig):
                for pixelY in range(yOrig):
                    orig = pixels_original[pixelX, pixelY]
                    pixels[pixelX + xOrig * x, pixelY + yOrig * y] = (
                        int(orig[0] * negative_visible + middleR), int(orig[1] * negative_visible + middleG),
                        int(orig[2] * negative_visible + middleB))
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
