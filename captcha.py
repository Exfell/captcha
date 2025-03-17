import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Генерация текста
text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

# Параметры изображения
width, height = 200, 80
image = Image.new('RGB', (width, height), (255, 255, 255))
draw = ImageDraw.Draw(image)

# Шрифт
font = ImageFont.truetype("arial.ttf", 40)

# Рисуем символы с наклоном
for i, char in enumerate(text):
    # Новый слой для каждого символа
    char_image = Image.new('RGBA', (60, 60), (255, 255, 255, 0))  # Прозрачный фон
    char_draw = ImageDraw.Draw(char_image)

    # Рисуем символ на отдельном слое
    char_draw.text((10, 5), char, font=font, fill=(random.randint(0, 150), random.randint(0, 150), random.randint(0, 150)))

    # Поворачиваем символ на случайный угол
    rotated_char = char_image.rotate(random.randint(-45, 45), resample=Image.BICUBIC, expand=1)

    # Вставляем на основное изображение
    x = 20 + i * 35
    y = random.randint(5, 20)
    image.paste(rotated_char, (x, y), rotated_char)  # Маска = rotated_char (альфа-канал)

# Линии и точки для шума
for _ in range(5):
    draw.line(((random.randint(0, width), random.randint(0, height)),
               (random.randint(0, width), random.randint(0, height))),
              fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), width=2)

for _ in range(100):
    draw.point((random.randint(0, width), random.randint(0, height)),
               fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

# Фильтр размытия
image = image.filter(ImageFilter.GaussianBlur(1))

# Сохраняем или показываем
image.save("captcha_with_rotation.png")
image.show()

print(f"Правильный ответ: {text}")
