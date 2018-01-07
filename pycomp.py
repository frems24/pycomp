# pycomp.py -- kompresuje pliki tekstowe metodą słownikową
# wersja 1.2

import os
import sys
from operator import itemgetter


def main():
    """ Główna funkcja programu. """

    # Przygotowanie informacji o statystyce słów w pliku
    src_file_name = sys.argv[1]
    words_dict = {}             # słownik {wyraz: [ilość wystąpień, długość]}
    spec_char = '@'

    with open(src_file_name, 'r') as input_file:
        for line in input_file:
            update_words_dict(line.rstrip(), words_dict, spec_char)

    min_repetitions = 2
    for word in words_dict.copy():
        if words_dict[word][0] < min_repetitions:
            words_dict.pop(word)

    # Przygotowanie listy słów do nagłówka oraz słownika z pozycjami tych słów na liście
    header_list = create_header(words_dict)
    header_dict = {}
    for index, word in enumerate(header_list):
        header_dict[word] = index

    # Przygotowanie nagłówka w docelowym pliku
    header_str = ''
    for word in header_list:
        word_sep = word + ' '
        header_str += word_sep
    header = spec_char + header_str + spec_char

    # Kompresja pliku
    dst_file_name = src_file_name + '.dcmp'
    with open(dst_file_name, 'w') as output_file:
        output_file.write(header)
        with open(src_file_name, 'r') as input_file:
            for input_line in input_file:
                output_line = create_output_line(input_line, header_dict, spec_char)
                output_file.write(output_line)

    # Wyświetlenie statystyk kompresji
    src_file_size = os.stat(src_file_name).st_size
    dst_file_size = os.stat(dst_file_name).st_size
    comp_ratio = (src_file_size - dst_file_size) / src_file_size
    print(f'{src_file_name:15} compression ratio: {comp_ratio:>5.1%}')


def update_words_dict(line, words_dict, spec_char):
    """
    Uaktualnie słownik 'words': jeśli nie ma w nim słowa to dopisuje, jeśli jest to zwiększa liczbę wystąpień.
    :param line: line: wiersz z pliku ze słowami
    :param words_dict: words_dict: słownik do uaktualnienia
    :param spec_char: przyjęty znak specjalny
    :return: uaktualniony słownik 'words' (w miejscu)
    """
    min_length = 2

    for word in line.split():
        if word in words_dict:
            words_dict[word][0] += 1
        else:
            if len(word) >= min_length and spec_char not in word:
                words_dict[word] = [1, len(word)]


def create_header(words_dict):
    """
    Utworzenie odpowiednio ułożonej listy z wyrazami do nagłówka.
    :param words_dict: słownik z wyrazami zebranymi z pliku źródłowego {wyraz: [ilość wystąpień, długość]}
    :return: lista przeznaczona do nagłówka pliku
    """
    # Utworzenie posortowanej listy słów
    words_sorted_list = sorted(words_dict.items(), key=itemgetter(1), reverse=True)
    words_total = len(words_sorted_list)

    # Utworzenie listy słów dla nagłówka
    dst_word_index = 0
    src_word_index = 0

    words_list = []
    while src_word_index < words_total:
        word_length = words_sorted_list[src_word_index][1][1]
        dst_word_indicator_length = len(str(dst_word_index))
        word_saved_space = word_length - dst_word_indicator_length
        word_dict_space = word_length + 1
        word_repeat = words_sorted_list[src_word_index][1][0]
        if word_saved_space * word_repeat > word_dict_space:
            words_list.append(words_sorted_list[src_word_index][0])
            dst_word_index += 1
        src_word_index += 1

    return words_list


def create_output_line(input_line, header_dict, spec_char):
    """
    Funkcja przetwarzająca linię tekstu odczytanego z pliku wejściowego
    na linię tekstu do zapisu w pliku skompresowanym.
    :param input_line: (str) linia odczytana z pliku wejściowego
    :param header_dict: słownik opisujący nagłówek pliku wyjściowego
    :param spec_char: znak specjalny poprzedzający numer pozycji w nagłówku
    :return: (str) linia przeznaczona do zapisu w pliku wyjściowym
    """
    output_line = ''
    one_word = ''
    for char in input_line:
        word_outside = True
        if char.isprintable() and not char.isspace():
            one_word += char
            if char == spec_char:
                one_word += spec_char
            word_outside = False

        if word_outside:
            if one_word in header_dict:
                one_word = spec_char + str(header_dict[one_word])
                output_line = output_line[:-1]
            output_line += one_word
            output_line += char
            one_word = ''

    return output_line


if __name__ == '__main__':
    main()
