import argparse
from generator import generate_qr
from encryptor import encrypt, save_key
import os
from datetime import datetime


def create_parser():
    """Создает парсер аргументов командной строки"""
    parser = argparse.ArgumentParser(description='QRForge - Генератор QR-кодов')

    # Основные параметры
    parser.add_argument('text', type=str, help='Текст для кодирования в QR')
    parser.add_argument('--output', '-o', type=str, default=None,
                       help='Имя выходного файла (по умолчанию: qr_<timestamp>.png)')

    # Внешний вид
    parser.add_argument('--logo', '-l', type=str, default=None,
                       help='Путь к логотипу для вставки в QR-код')
    parser.add_argument('--color', '-c', type=str, default='#000000',
                       help='Цвет QR-кода в HEX (по умолчанию: #000000)')
    parser.add_argument('--bg', '-b', type=str, default='#FFFFFF',
                       help='Цвет фона в HEX (по умолчанию: #FFFFFF)')
    parser.add_argument('--size', '-s', type=int, default=10,
                       help='Размер QR-кода (по умолчанию: 10)')
    parser.add_argument('--border', '-br', type=int, default=4,
                       help='Размер границы (по умолчанию: 4)')
    parser.add_argument('--style', '-st', type=str, default='default',
                       choices=['default', 'instagram', 'telegram', 'dark',
                               'neon', 'vintage', 'minimal', 'abstract',
                               'watercolor', 'cyber', 'pastel'],
                       help='Стиль QR-кода (по умолчанию: default)')
    parser.add_argument('--gradient', '-g', type=str, nargs=2, default=None,
                       help='Градиент в виде двух цветов (start end)')
    parser.add_argument('--pattern', '-p', type=str, default=None,
                       choices=['dots', 'circles', 'diamonds', 'rounded', 'watercolor', 'cyber'],
                       help='Паттерн для точек QR-кода')
    parser.add_argument('--corner-style', '-cs', type=str, default='square',
                       choices=['square', 'rounded', 'pointed', 'circle'],
                       help='Стиль углов QR-кода')
    parser.add_argument('--dot-style', '-ds', type=str, default='square',
                       choices=['square', 'circle', 'rounded', 'diamond'],
                       help='Стиль точек QR-кода')

    # Шифрование
    parser.add_argument('--encrypt', '-e', action='store_true',
                       help='Шифровать текст перед генерацией QR-кода')
    parser.add_argument('--key', '-k', type=str, default=None,
                       help='Ключ для шифрования (если не указан - генерируется новый)')

    # Тип контента
    parser.add_argument('--type', '-t', type=str, default='text',
                       choices=['text', 'url', 'wifi', 'vcard'],
                       help='Тип содержимого QR-кода (по умолчанию: text)')

    return parser


def generate_wifi_config(ssid: str, password: str, security: str = 'WPA') -> str:
    """Генерирует строку конфигурации WiFi для QR-кода"""
    return f"WIFI:T:{security};S:{ssid};P:{password};;"


def generate_vcard(name: str, phone: str, email: str = None, org: str = None) -> str:
    """Генерирует vCard для QR-кода"""
    vcard = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nTEL:{phone}"
    if email:
        vcard += f"\nEMAIL:{email}"
    if org:
        vcard += f"\nORG:{org}"
    vcard += "\nEND:VCARD"
    return vcard


def main():
    parser = create_parser()
    args = parser.parse_args()

    # Обработка типа контента
    content = args.text
    if args.type == 'wifi':
        if ':' not in args.text:
            print("Для WiFi укажите SSID и пароль в формате 'SSID:password'")
            return
        ssid, password = args.text.split(':', 1)
        content = generate_wifi_config(ssid, password)
    elif args.type == 'vcard':
        parts = args.text.split(':')
        if len(parts) < 2:
            print("Для vCard укажите как минимум имя и телефон в формате 'name:phone:email:org'")
            return
        name, phone = parts[0], parts[1]
        email = parts[2] if len(parts) > 2 else None
        org = parts[3] if len(parts) > 3 else None
        content = generate_vcard(name, phone, email, org)

    # Шифрование если нужно
    key = None
    if args.encrypt:
        encrypted_content, key = encrypt(content, args.key)
        content = encrypted_content
        save_key(key)
        print(f"Текст зашифрован. Ключ сохранен в key.txt")

    # Генерация имени файла если не указано
    output_path = args.output
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"qr_{timestamp}.png"

    # Генерация QR-кода
    try:
        result_path = generate_qr(
            text=content,
            output_path=output_path,
            logo_path=args.logo,
            color=args.color,
            bg_color=args.bg,
            size=args.size,
            border=args.border,
            style=args.style,
            gradient=args.gradient,
            pattern=args.pattern,
            corner_style=args.corner_style,
            dot_style=args.dot_style
        )
        print(f"QR-код успешно создан: {result_path}")
    except Exception as e:
        print(f"Ошибка при генерации QR-кода: {str(e)}")


if __name__ == "__main__":
    main()