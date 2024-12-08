import barcode
from barcode.writer import ImageWriter
from PIL import Image
import win32print
import win32ui

# Генерация штрихкода EAN-13
ean = barcode.get_barcode_class('ean13')
barcode_data = "123456789012"  # Пример EAN-13 кода
barcode_image = ean(barcode_data, writer=ImageWriter())

# Сохранение штрихкода в файл
barcode_image.save("barcode_ean13")

# Открытие изображения с помощью PIL
image = Image.open("barcode_ean13.png")

# Изменение размера изображения до нужных 58мм x 30мм (примерно 228x118 пикселей для разрешения 300 dpi)
image = image.resize((228, 118))

# Сохранение измененного изображения
image.save("barcode_resized.png")

# Печать на принтере
printer_name = win32print.GetDefaultPrinter()  # Получаем имя принтера

# Получаем контекст устройства для принтера
printer = win32ui.CreateDC()
printer.CreatePrinterDC(printer_name)

# Открытие изображения для печати
image_to_print = Image.open("barcode_resized.png")

# Конвертация изображения в формат для печати
image_to_print.show()

# Печать
printer.StartDoc("Barcode Print")
printer.StartPage()

# Печать изображения
printer.DrawBitmap(image_to_print, (0, 0))

# Завершение печати
printer.EndPage()
printer.EndDoc()