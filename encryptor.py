from cryptography.fernet import Fernet
import base64
import os


def generate_key() -> str:
    """Генерирует ключ шифрования"""
    return Fernet.generate_key().decode()


def encrypt(text: str, key: str = None) -> tuple:
    """
    Шифрует текст

    :param text: Текст для шифрования
    :param key: Ключ шифрования (если None - генерируется новый)
    :return: Кортеж (зашифрованный текст, ключ)
    """
    if key is None:
        key = generate_key()
    else:
        # Проверяем, что ключ валидный
        try:
            Fernet(key.encode())
        except:
            raise ValueError("Invalid key")

    f = Fernet(key.encode())
    encrypted = f.encrypt(text.encode())
    return encrypted.decode(), key


def decrypt(encrypted_text: str, key: str) -> str:
    """
    Дешифрует текст

    :param encrypted_text: Зашифрованный текст
    :param key: Ключ шифрования
    :return: Расшифрованный текст
    """
    f = Fernet(key.encode())
    try:
        decrypted = f.decrypt(encrypted_text.encode())
    except:
        raise ValueError("Decryption failed. Invalid key or token.")
    return decrypted.decode()


def save_key(key: str, filename: str = "key.txt") -> None:
    """Сохраняет ключ в файл"""
    with open(filename, 'w') as f:
        f.write(key)


def load_key(filename: str = "key.txt") -> str:
    """Загружает ключ из файла"""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Key file {filename} not found")
    with open(filename, 'r') as f:
        return f.read()