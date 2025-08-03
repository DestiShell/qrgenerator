import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageOps, ImageFilter
import os
import io
import random
import math
from typing import Tuple, Optional
import numpy as np


def generate_qr(
        text: str,
        output_path: str = "output.png",
        logo_path: str = None,
        color: str = "#000000",
        bg_color: str = "#FFFFFF",
        size: int = 10,
        border: int = 4,
        error_correction: int = ERROR_CORRECT_H,
        style: str = "default",
        gradient: Tuple[str, str] = None,
        pattern: str = None,
        corner_style: str = "square",
        dot_style: str = "square"
) -> str:
    """
    Генерирует QR-код с расширенными настройками стиля

    :param text: Текст для кодирования
    :param output_path: Путь для сохранения
    :param logo_path: Путь к логотипу
    :param color: Цвет QR-кода (HEX)
    :param bg_color: Цвет фона (HEX)
    :param size: Размер QR-кода
    :param border: Размер границы
    :param error_correction: Уровень коррекции ошибок
    :param style: Стиль QR-кода
    :param gradient: Градиент в виде кортежа (start_color, end_color)
    :param pattern: Паттерн для точек ("circles", "dots", "diamonds", "rounded")
    :param corner_style: Стиль углов ("square", "rounded", "pointed", "circle")
    :param dot_style: Стиль точек ("square", "circle", "rounded", "diamond")
    :return: Путь к сохраненному файлу
    """
    # Создаем объект QRCode
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction,
        box_size=size,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=True)

    # Получаем матрицу QR-кода
    qr_matrix = qr.get_matrix()

    # Применяем стиль
    color, bg_color, gradient, pattern, corner_style, dot_style = apply_style(
        style, color, bg_color, gradient, pattern, corner_style, dot_style
    )

    # Создаем базовое изображение QR-кода с учетом стиля
    img = create_styled_qr(
        qr_matrix=qr_matrix,
        size=size,
        border=border,
        color=color,
        bg_color=bg_color,
        gradient=gradient,
        pattern=pattern,
        corner_style=corner_style,
        dot_style=dot_style
    )

    # Добавляем логотип если указан
    if logo_path and os.path.exists(logo_path):
        img = add_logo(img, logo_path)

    # Применяем эффекты в зависимости от стиля
    img = apply_effects(img, style)

    # Сохраняем результат
    img.save(output_path)
    return output_path


def generate_qr_to_bytes(
        text: str,
        logo_path: str = None,
        color: str = "#000000",
        bg_color: str = "#FFFFFF",
        size: int = 10,
        border: int = 4,
        error_correction: int = ERROR_CORRECT_H,
        style: str = "default",
        gradient: Tuple[str, str] = None,
        pattern: str = None,
        corner_style: str = "square",
        dot_style: str = "square"
) -> bytes:
    """
    Генерирует QR-код и возвращает его как bytes

    :param text: Текст для кодирования
    :param logo_path: Путь к логотипу
    :param color: Цвет QR-кода (HEX)
    :param bg_color: Цвет фона (HEX)
    :param size: Размер QR-кода
    :param border: Размер границы
    :param error_correction: Уровень коррекции ошибок
    :param style: Стиль QR-кода
    :param gradient: Градиент в виде кортежа (start_color, end_color)
    :param pattern: Паттерн для точек ("circles", "dots", "diamonds", "rounded")
    :param corner_style: Стиль углов ("square", "rounded", "pointed", "circle")
    :param dot_style: Стиль точек ("square", "circle", "rounded", "diamond")
    :return: Изображение в виде bytes
    """
    # Создаем временный файл в памяти
    temp_file = io.BytesIO()

    # Генерируем QR-код
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction,
        box_size=size,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=True)

    # Получаем матрицу QR-кода
    qr_matrix = qr.get_matrix()

    # Применяем стиль
    color, bg_color, gradient, pattern, corner_style, dot_style = apply_style(
        style, color, bg_color, gradient, pattern, corner_style, dot_style
    )

    # Создаем базовое изображение QR-кода с учетом стиля
    img = create_styled_qr(
        qr_matrix=qr_matrix,
        size=size,
        border=border,
        color=color,
        bg_color=bg_color,
        gradient=gradient,
        pattern=pattern,
        corner_style=corner_style,
        dot_style=dot_style
    )

    # Добавляем логотип если указан
    if logo_path and os.path.exists(logo_path):
        img = add_logo(img, logo_path)

    # Применяем эффекты в зависимости от стиля
    img = apply_effects(img, style)

    # Сохраняем в bytes
    img.save(temp_file, format='PNG')
    temp_file.seek(0)
    return temp_file.getvalue()


def apply_style(
        style: str,
        color: str,
        bg_color: str,
        gradient: Optional[Tuple[str, str]],
        pattern: Optional[str],
        corner_style: str,
        dot_style: str
) -> Tuple[str, str, Optional[Tuple[str, str]], Optional[str], str, str]:
    """Применяет предустановленные стили"""
    style_settings = {
        "default": {
            "color": color,
            "bg_color": bg_color,
            "gradient": None,
            "pattern": None,
            "corner_style": "square",
            "dot_style": "square"
        },
        "instagram": {
            "color": "#E1306C",
            "bg_color": "#FFFFFF",
            "gradient": ("#833AB4", "#FD1D1D"),
            "pattern": "rounded",
            "corner_style": "rounded",
            "dot_style": "rounded"
        },
        "telegram": {
            "color": "#0088cc",
            "bg_color": "#FFFFFF",
            "gradient": ("#0088cc", "#00aced"),
            "pattern": None,
            "corner_style": "rounded",
            "dot_style": "circle"
        },
        "dark": {
            "color": "#FFFFFF",
            "bg_color": "#121212",
            "gradient": None,
            "pattern": None,
            "corner_style": "square",
            "dot_style": "square"
        },
        "neon": {
            "color": "#0ff0fc",
            "bg_color": "#000000",
            "gradient": ("#ff00ff", "#00ffff"),
            "pattern": "diamond",
            "corner_style": "pointed",
            "dot_style": "diamond"
        },
        "vintage": {
            "color": "#8B4513",
            "bg_color": "#F5F5DC",
            "gradient": ("#8B4513", "#A0522D"),
            "pattern": "dots",
            "corner_style": "rounded",
            "dot_style": "circle"
        },
        "minimal": {
            "color": "#000000",
            "bg_color": "#FFFFFF",
            "gradient": None,
            "pattern": None,
            "corner_style": "square",
            "dot_style": "circle"
        },
        "abstract": {
            "color": "#FF5722",
            "bg_color": "#212121",
            "gradient": ("#FF5722", "#FF9800"),
            "pattern": "random",
            "corner_style": "circle",
            "dot_style": "random"
        },
        "watercolor": {
            "color": "#1E88E5",
            "bg_color": "#E3F2FD",
            "gradient": ("#1E88E5", "#64B5F6"),
            "pattern": "watercolor",
            "corner_style": "rounded",
            "dot_style": "rounded"
        },
        "cyber": {
            "color": "#00FF41",
            "bg_color": "#0D0208",
            "gradient": ("#008F11", "#00FF41"),
            "pattern": "cyber",
            "corner_style": "pointed",
            "dot_style": "square"
        },
        "pastel": {
            "color": "#FF9AA2",
            "bg_color": "#FFFFFF",
            "gradient": ("#FFB7B2", "#FFDAC1"),
            "pattern": "rounded",
            "corner_style": "rounded",
            "dot_style": "circle"
        }
    }

    style_data = style_settings.get(style, style_settings["default"])

    return (
        style_data["color"],
        style_data["bg_color"],
        gradient if gradient is not None else style_data["gradient"],
        pattern if pattern is not None else style_data["pattern"],
        corner_style if corner_style != "square" else style_data["corner_style"],
        dot_style if dot_style != "square" else style_data["dot_style"]
    )


def create_styled_qr(
        qr_matrix,
        size: int,
        border: int,
        color: str,
        bg_color: str,
        gradient: Optional[Tuple[str, str]],
        pattern: Optional[str],
        corner_style: str,
        dot_style: str
) -> Image.Image:
    """Создает QR-код с применением стилей"""
    # Размеры изображения
    matrix_size = len(qr_matrix)
    img_size = matrix_size * size + 2 * border * size
    img = Image.new("RGB", (img_size, img_size), bg_color)
    draw = ImageDraw.Draw(img)

    # Функция для определения цвета с учетом градиента
    def get_color(x: int, y: int) -> str:
        if not gradient:
            return color

        # Преобразуем HEX в RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

        start_rgb = hex_to_rgb(gradient[0])
        end_rgb = hex_to_rgb(gradient[1])

        # Интерполяция цвета
        ratio = (x + y) / (img_size * 2)
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
        h = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)

        return f"#{r:02x}{g:02x}{h:02x}"

    # Рисуем QR-код с учетом стиля
    for y in range(matrix_size):
        for x in range(matrix_size):
            if qr_matrix[y][x]:
                pixel_color = get_color(x * size, y * size)
                left = x * size + border * size
                top = y * size + border * size
                right = left + size
                bottom = top + size

                # Определяем стиль углов (для позиционных узоров)
                is_corner = (
                        (x < 8 and y < 8) or
                        (x < 8 and y >= matrix_size - 8) or
                        (x >= matrix_size - 8 and y < 8)
                )

                current_style = corner_style if is_corner else dot_style

                # Рисуем элемент в соответствии со стилем
                if current_style == "circle":
                    draw.ellipse([left, top, right, bottom], fill=pixel_color)
                elif current_style == "rounded":
                    radius = size // 4
                    draw.rounded_rectangle([left, top, right, bottom], radius=radius, fill=pixel_color)
                elif current_style == "diamond":
                    draw.polygon(
                        [(left + size // 2, top), (right, top + size // 2),
                         (left + size // 2, bottom), (left, top + size // 2)],
                        fill=pixel_color
                    )
                elif current_style == "pointed":
                    if is_corner:
                        # Для углов делаем заостренные углы
                        if x < 8 and y < 8:  # Левый верхний угол
                            draw.polygon(
                                [(left, top + size), (left + size, top), (left + size, top + size)],
                                fill=pixel_color
                            )
                        elif x < 8 and y >= matrix_size - 8:  # Левый нижний угол
                            draw.polygon(
                                [(left, top), (left + size, top + size), (left + size, top)],
                                fill=pixel_color
                            )
                        elif x >= matrix_size - 8 and y < 8:  # Правый верхний угол
                            draw.polygon(
                                [(left, top), (left + size, top + size), (left, top + size)],
                                fill=pixel_color
                            )
                        else:
                            draw.rectangle([left, top, right, bottom], fill=pixel_color)
                    else:
                        draw.rectangle([left, top, right, bottom], fill=pixel_color)
                elif current_style == "random":
                    shapes = ["square", "circle", "diamond"]
                    chosen_style = random.choice(shapes)
                    if chosen_style == "square":
                        draw.rectangle([left, top, right, bottom], fill=pixel_color)
                    elif chosen_style == "circle":
                        draw.ellipse([left, top, right, bottom], fill=pixel_color)
                    elif chosen_style == "diamond":
                        draw.polygon(
                            [(left + size // 2, top), (right, top + size // 2),
                             (left + size // 2, bottom), (left, top + size // 2)],
                            fill=pixel_color
                        )
                else:  # square по умолчанию
                    draw.rectangle([left, top, right, bottom], fill=pixel_color)

    # Применяем паттерны если нужно
    if pattern == "dots":
        img = apply_dots_pattern(img, color)
    elif pattern == "watercolor":
        img = apply_watercolor_effect(img)
    elif pattern == "cyber":
        img = apply_cyber_effect(img)

    return img


def add_logo(img: Image.Image, logo_path: str) -> Image.Image:
    """Добавляет логотип в центр QR-кода"""
    logo = Image.open(logo_path)

    # Рассчитываем размер логотипа (15-25% от размера QR)
    qr_width, qr_height = img.size
    logo_size = min(qr_width, qr_height) // 4

    # Масштабируем логотип
    logo.thumbnail((logo_size, logo_size), Image.LANCZOS)

    # Создаем маску для круглого логотипа
    if logo.mode != 'RGBA':
        mask = Image.new("L", logo.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, logo.size[0], logo.size[1]), fill=255)
        logo.putalpha(mask)

    # Позиционируем логотип по центру
    pos = ((qr_width - logo.size[0]) // 2, (qr_height - logo.size[1]) // 2)

    # Вставляем логотип
    img.paste(logo, pos, logo)
    return img


def apply_effects(img: Image.Image, style: str) -> Image.Image:
    """Применяет дополнительные эффекты в зависимости от стиля"""
    if style == "watercolor":
        # Эффект акварели
        img = img.filter(ImageFilter.GaussianBlur(radius=1))
        img = Image.blend(img, Image.new("RGB", img.size, "#FFFFFF"), 0.1)
    elif style == "cyber":
        # Добавляем сетку
        draw = ImageDraw.Draw(img)
        width, height = img.size
        grid_size = 20
        for x in range(0, width, grid_size):
            draw.line([(x, 0), (x, height)], fill="#00FF41", width=1)
        for y in range(0, height, grid_size):
            draw.line([(0, y), (width, y)], fill="#00FF41", width=1)
    elif style == "abstract":
        # Добавляем случайные круги на фон
        draw = ImageDraw.Draw(img)
        for _ in range(20):
            x = random.randint(0, img.width)
            y = random.randint(0, img.height)
            radius = random.randint(5, 30)
            color = random.choice(["#FF5722", "#FF9800", "#FFC107", "#FFEB3B"])
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color)
    elif style == "neon":
        # Добавляем свечение
        glow = img.filter(ImageFilter.GaussianBlur(radius=3))
        img = Image.blend(img, glow, 0.7)

    return img


def apply_dots_pattern(img: Image.Image, color: str) -> Image.Image:
    """Применяет точечный паттерн к QR-коду"""
    width, height = img.size
    pattern = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(pattern)

    # Рисуем точки
    dot_size = 2
    spacing = 4
    for y in range(0, height, spacing):
        for x in range(0, width, spacing):
            draw.ellipse([x, y, x + dot_size, y + dot_size], fill=color)

    # Накладываем паттерн на QR-код
    img = Image.blend(img, pattern, 0.2)
    return img


def apply_watercolor_effect(img: Image.Image) -> Image.Image:
    """Создает эффект акварели"""
    # Преобразуем изображение в массив numpy
    arr = np.array(img)

    # Добавляем шум
    noise = np.random.randint(-20, 20, arr.shape, dtype=np.int32)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)

    # Создаем новое изображение
    watercolor_img = Image.fromarray(arr)

    # Добавляем размытие
    watercolor_img = watercolor_img.filter(ImageFilter.GaussianBlur(radius=1))

    return watercolor_img


def apply_cyber_effect(img: Image.Image) -> Image.Image:
    """Создает киберпанк эффект"""
    # Преобразуем изображение в массив numpy
    arr = np.array(img)

    # Усиливаем зеленый канал
    arr[:, :, 1] = np.clip(arr[:, :, 1] * 1.5, 0, 255)

    # Создаем новое изображение
    cyber_img = Image.fromarray(arr)

    return cyber_img