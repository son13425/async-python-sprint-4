import string
from random import choices

from core.config import CUSTOM_ID_LEN


def create_unique_short_link():
    """Генерация уникальной короткой ссылки"""
    short_link = ''.join(
        choices(string.ascii_letters + string.digits, k=CUSTOM_ID_LEN)
    )
    return short_link
