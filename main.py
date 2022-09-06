from PIL import Image
Image.MAX_IMAGE_PIXELS = None

print("Подготовка к работе...", end='')
original = Image.open("source.jpg")
pixel_image = Image.open("pixel.jpg")
pixels_original = original.load()
xOrig, yOrig = original.size
xPixel, yPixel = pixel_image.size

print('\033[F\033[K', end='')
print("Создание изображения нужных размеров...", end='')
result = Image.new('RGB', (xOrig * xPixel, yOrig * yPixel), color='red')
pixels = result.load()
loading_final = (xOrig - 1) / 100

for x in range(xOrig):
    loading = round(x / loading_final, 3)
    print('\033[F\033[K', end='')
    print("Обработка -", str(loading) + "%", end='')
    for y in range(yOrig):
        visible = 0.5
        middleR = visible * pixels_original[x, y][0]
        middleG = visible * pixels_original[x, y][1]
        middleB = visible * pixels_original[x, y][2]
        negative_visible = 1 - visible
        for pixelX in range(xOrig):
            for pixelY in range(yOrig):
                orig = pixels_original[pixelX, pixelY]
                pixels[pixelX + xOrig * x, pixelY + yOrig * y] = (
                    int(orig[0] * negative_visible + middleR), int(orig[1] * negative_visible + middleG), int(orig[2] * negative_visible + middleB))
print('\033[F\033[K', end='')
print("Сохранение изображения...", end='')
result.save("result.jpg")
print('\033[F\033[K', end='')
print("Изображение сохранено.", end='')
