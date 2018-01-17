# pydecomp.py -- dekompresuje pliki tekstowe metodą słownikową
# wersja 1.3

import sys
from num62lib import num62_to_num


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
            dst_file_name = src_file_name[:-9] + '.d.txt'
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
    spec_char_after_index = False
    inside_index = False
    new_line = True
    line_beginning = False

    while True:
        if spec_char_after_index:
            char = spec_char
        else:
            char = input_file.read(1)

        word_outside = True
        second_spec_char = False
        spec_char_after_index = False

        if not spec_word_inside:
            one_word = char

        if spec_word_inside:
            if char == spec_char:
                if not inside_index:
                    one_word = char
                    spec_word_inside = False
                    second_spec_char = True
                else:
                    spec_char_after_index = True
                    char = ''
            if char.isalnum():
                index += char
                word_outside = False
                inside_index = True
            else:
                inside_index = False

        if spec_word_inside and word_outside:
            word_found = decrypt_list[num62_to_num(index)]
            if line_beginning:
                one_word = word_found + char
                line_beginning = False
            else:
                one_word = ' ' + word_found + char
            spec_word_inside = False
            index = ''

        if char == spec_char and not spec_word_inside and not second_spec_char:
            spec_word_inside = True
            if new_line:
                line_beginning = True

        if not spec_word_inside:
            output_file.write(one_word)
            one_word = ''

        if char == '\n' or char == spec_char:
            new_line = True
        else:
            new_line = False

        if not char and not spec_char_after_index:
            break


if __name__ == '__main__':
    main()
