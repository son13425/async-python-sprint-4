import string
from random import choices

from core.config import CUSTOM_ID_LEN


def get_unique_short_id():
    """Генерация уникальной короткой ссылки"""
    short_id = ''.join(
        choices(string.ascii_letters + string.digits, k=CUSTOM_ID_LEN)
    )
    return short_id
