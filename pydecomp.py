# pydecomp.py -- dekompresuje pliki tekstowe metodą słownikową
# wersja 1.0

import sys


def main():
    """ Główna funkcja programu. """

    src_file_name = sys.argv[1]

    # Wczytanie nagłówka pliku
    with open(src_file_name, 'r') as input_file:
        # Wczytanie znaku specjalnego
        spec_char = input_file.read(1)
        if spec_char.isprintable() and not spec_char.isspace() and len(spec_char) > 0:
            char = ''
            header_str = ''
            # Wczytanie listy słów z nagłówka pliku
            while char != spec_char:
                char = input_file.read(1)
                header_str += char

            decrypt_list = header_str.split()
        else:
            decrypt_list = ''

        if decrypt_list:
            dst_file_name = src_file_name.rstrip('.txt.dcmp') + '_decomp.txt'
            # Dekompresja pliku
            with open(dst_file_name, 'w') as output_file:
                decompress(input_file, output_file, decrypt_list, spec_char)


def decompress(input_file, output_file, decrypt_list, spec_char):
    """
    Funkcja przetwarzająca znaki w pliku.
    :param input_file: plik skompresowany
    :param output_file: plik wynikowy
    :param decrypt_list: lista wyrazów służących do dekompresji
    :param spec_char: prefix pozycji wyrazu na liście
    :return: None
    """
    one_word = ''
    index = ''
    spec_word_inside = False
    while True:
        char = input_file.read(1)
        word_outside = True
        second_spec_char = False

        if not spec_word_inside:
            one_word = char

        if spec_word_inside:
            if char.isdigit():
                index += char
                word_outside = False
            if char == spec_char:
                one_word = char
                spec_word_inside = False
                second_spec_char = True

        if spec_word_inside and word_outside:
            one_word = decrypt_list[int(index)]
            one_word += char
            spec_word_inside = False
            index = ''

        if char == spec_char and not spec_word_inside and not second_spec_char:
            spec_word_inside = True

        if not spec_word_inside:
            output_file.write(one_word)
            one_word = ''

        if not char:
            break


if __name__ == '__main__':
    main()
