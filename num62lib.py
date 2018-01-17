# num62lib.py -- biblioteka funkcji do obsługi liczb w systemie o podstawie 62
# wersja 1.0


def num62_to_num(number_str):
    """
    Zamienia liczbę w systemie o podstawie 62 na liczbę dziesiętną.
    :param number_str: (str) liczba w systemie o podstawie 62
    :return: (int) liczba dziesiętna
    """
    src_base = 62
    num_len_exp = len(number_str) - 1
    num_base_10 = 0
    for pos, digit_sign in enumerate(number_str):
        exp = num_len_exp - pos
        num_base_10 += (src_base ** exp) * character_to_num(digit_sign)

    return num_base_10


def num_to_num62(num):
    """
    Zamienia liczbę dziesiętną na liczbę w systemie o podstawie 62.
    :param num: (int) liczba dziesiętna
    :return: (str) liczba w systemie o podstawie 62
    """
    if num == 0:
        return '0'

    dst_base = 62
    num62 = ''
    while num > 0:
        rest = num % dst_base
        num62 = num_to_character(rest) + num62
        num //= dst_base

    return num62


def character_to_num(character):
    """
    Funkcja przekształca znak w systemie o podstawie 62 na kolejną liczbę według wzoru:
    0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
    :param character: znak do przekształcenia
    :return: liczba
    """
    if character.isdigit():
        num = int(character)
    elif character.isupper():
        num = ord(character) - 55
    elif character.islower():
        num = ord(character) - 61
    else:
        num = None

    return num


def num_to_character(num):
    """
    Funkcja przekształca liczbę na znak w systemie o podstawie 62 według wzoru:
    0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
    :param num: liczba (0 - 61) do przekształcenia
    :return: znak
    """
    if num >= 0:
        if num <= 9:
            character = chr(num + 48)
        elif num <= 35:
            character = chr(num + 55)
        elif num <= 61:
            character = chr(num + 61)
        else:
            character = None
    else:
        character = None

    return character
