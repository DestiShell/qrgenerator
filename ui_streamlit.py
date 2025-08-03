import streamlit as st
from generator import generate_qr_to_bytes
from encryptor import encrypt, save_key
import os
from datetime import datetime
import base64


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


def get_image_download_link(img_bytes, filename):
    """Генерирует ссылку для скачивания изображения"""
    b64 = base64.b64encode(img_bytes).decode()
    return f'<a href="data:image/png;base64,{b64}" download="{filename}">Скачать QR-код</a>'


def main():
    st.set_page_config(page_title="QRForge", page_icon="🔳", layout="centered")
    st.title("🔳 QRForge - Генератор QR-кодов")

    # Сайдбар с настройками
    with st.sidebar:
        st.header("Настройки QR-кода")

        # Выбор типа контента
        content_type = st.selectbox(
            "Тип содержимого",
            ["Текст", "URL", "WiFi", "vCard"],
            index=0
        )

        # Цвета
        col1, col2 = st.columns(2)
        with col1:
            color = st.color_picker("Цвет QR-кода", "#000000")
        with col2:
            bg_color = st.color_picker("Цвет фона", "#FFFFFF")

        # Градиент
        use_gradient = st.checkbox("Использовать градиент")
        if use_gradient:
            col1, col2 = st.columns(2)
            with col1:
                gradient_start = st.color_picker("Начало градиента", "#833AB4")
            with col2:
                gradient_end = st.color_picker("Конец градиента", "#FD1D1D")
            gradient = (gradient_start, gradient_end)
        else:
            gradient = None

        # Размер и граница
        size = st.slider("Размер", 5, 20, 10)
        border = st.slider("Граница", 1, 10, 4)

        # Стиль
        style = st.selectbox(
            "Стиль",
            ["По умолчанию", "Instagram", "Telegram", "Темный",
             "Неоновый", "Винтажный", "Минимализм", "Абстрактный",
             "Акварель", "Киберпанк", "Пастельный"],
            index=0
        )
        style_map = {
            "По умолчанию": "default",
            "Instagram": "instagram",
            "Telegram": "telegram",
            "Темный": "dark",
            "Неоновый": "neon",
            "Винтажный": "vintage",
            "Минимализм": "minimal",
            "Абстрактный": "abstract",
            "Акварель": "watercolor",
            "Киберпанк": "cyber",
            "Пастельный": "pastel"
        }

        # Дополнительные стили
        st.subheader("Дополнительные стили")
        col1, col2 = st.columns(2)
        with col1:
            corner_style = st.selectbox(
                "Стиль углов",
                ["Квадратные", "Закругленные", "Заостренные", "Круглые"],
                index=0
            )
            corner_style_map = {
                "Квадратные": "square",
                "Закругленные": "rounded",
                "Заостренные": "pointed",
                "Круглые": "circle"
            }
        with col2:
            dot_style = st.selectbox(
                "Стиль точек",
                ["Квадратные", "Круглые", "Закругленные", "Ромбы"],
                index=0
            )
            dot_style_map = {
                "Квадратные": "square",
                "Круглые": "circle",
                "Закругленные": "rounded",
                "Ромбы": "diamond"
            }

        # Паттерны
        pattern = st.selectbox(
            "Паттерн",
            ["Нет", "Точки", "Круги", "Ромбы", "Закругленные", "Акварель", "Кибер"],
            index=0
        )
        pattern_map = {
            "Нет": None,
            "Точки": "dots",
            "Круги": "circles",
            "Ромбы": "diamonds",
            "Закругленные": "rounded",
            "Акварель": "watercolor",
            "Кибер": "cyber"
        }

        # Шифрование
        encrypt_data = st.checkbox("Шифровать данные")
        if encrypt_data:
            key = st.text_input("Ключ шифрования (оставьте пустым для автоматической генерации)")

    # Основная форма
    with st.form("qr_form"):
        # Поля ввода в зависимости от типа контента
        if content_type == "Текст":
            content = st.text_area("Введите текст", "Hello, World!")
        elif content_type == "URL":
            content = st.text_input("Введите URL", "https://example.com")
            if not content.startswith(('http://', 'https://')):
                content = f"https://{content}"
        elif content_type == "WiFi":
            col1, col2 = st.columns(2)
            with col1:
                ssid = st.text_input("Название сети (SSID)")
            with col2:
                password = st.text_input("Пароль", type="password")
            content = generate_wifi_config(ssid, password)
        elif content_type == "vCard":
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Имя")
                phone = st.text_input("Телефон")
            with col2:
                email = st.text_input("Email")
                org = st.text_input("Организация")
            content = generate_vcard(name, phone, email, org)

        # Загрузка логотипа
        logo_file = st.file_uploader("Логотип (опционально)", type=["png", "jpg", "jpeg"])

        # Кнопка генерации
        submitted = st.form_submit_button("Сгенерировать QR-код")

    # Обработка формы
    if submitted:
        if (content_type == "WiFi" and (not ssid or not password)) or \
                (content_type == "vCard" and (not name or not phone)):
            st.error("Заполните все обязательные поля")
            return

        # Шифрование если нужно
        encryption_key = None
        if encrypt_data:
            try:
                content, encryption_key = encrypt(content, key if key else None)
                if not key:
                    save_key(encryption_key)
                    st.success("Текст зашифрован. Ключ сохранен в key.txt")
            except Exception as e:
                st.error(f"Ошибка шифрования: {str(e)}")
                return

        # Генерация QR-кода
        try:
            logo_path = None
            if logo_file:
                # Сохраняем временный файл
                logo_path = f"temp_logo.{logo_file.name.split('.')[-1]}"
                with open(logo_path, "wb") as f:
                    f.write(logo_file.getbuffer())

            qr_img = generate_qr_to_bytes(
                text=content,
                logo_path=logo_path,
                color=color,
                bg_color=bg_color,
                size=size,
                border=border,
                style=style_map[style],
                gradient=gradient,
                pattern=pattern_map[pattern],
                corner_style=corner_style_map[corner_style],
                dot_style=dot_style_map[dot_style]
            )

            # Удаляем временный файл логотипа если был
            if logo_file and os.path.exists(logo_path):
                os.remove(logo_path)

            # Отображение результата
            st.image(qr_img, caption="Ваш QR-код", use_column_width=True)

            # Ссылка для скачивания
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qr_{timestamp}.png"
            st.markdown(get_image_download_link(qr_img, filename), unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Ошибка генерации QR-кода: {str(e)}")


if __name__ == "__main__":
    main()