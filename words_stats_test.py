# words_stats_test.py -- pokazuje zawartość nagłówka do programu pycomp.py
# wersja 1.3

import sys
from operator import itemgetter
from num62lib import num_to_num62


def main():
    """ Główna funkcja programu. """

    # Przygotowanie informacji o statystyce słów w pliku
    file_name = sys.argv[1]
    words_dict = {}  # słownik {wyraz: [ilość wystąpień, długość]}
    spec_char = '@'

    with open(file_name, 'r') as input_file:
        for line in input_file:
            update_words_dict(line.rstrip(), words_dict, spec_char)

    min_repetitions = 2
    for word in words_dict.copy():
        if words_dict[word][0] < min_repetitions:
            words_dict.pop(word)

    # Utworzenie posortowanej listy słów
    words_sorted_list = sorted(words_dict.items(), key=itemgetter(1), reverse=True)
    words_total = len(words_sorted_list)

    # Utworzenie listy słów dla nagłówka
    dst_word_index = 0
    src_word_index = 0

    words_list = []
    while src_word_index < words_total:
        word_length = words_sorted_list[src_word_index][1][1]
        dst_word_indicator_length_62 = len(num_to_num62(dst_word_index))
        word_saved_space = word_length - dst_word_indicator_length_62
        word_dict_space = word_length + 1
        word_repeat = words_sorted_list[src_word_index][1][0]
        if word_saved_space * word_repeat > word_dict_space:
            words_list.append(words_sorted_list[src_word_index])
            dst_word_index += 1
        src_word_index += 1

    num_of_spec = 0
    print("idx        słowo      il. wyst  długość")
    for n, (word, stats) in enumerate(words_list):
        n_62 = num_to_num62(n)
        print("%3s%18s\t%d\t%d" % (n_62, word, stats[0], stats[1]))
        num_of_spec += stats[0]

    print(f"\nIlość wystąpień '@' w pliku: {num_of_spec}")
    print("Całkowita ilość słów: %d" % words_total)
    print("dst: %d" % dst_word_index)
    print("src: %d" % src_word_index)

    print("Gotowe.")


def update_words_dict(line, words_dict, spec_char):
    """
    Uaktualnie słownik 'words': jeśli nie ma w nim słowa to dopisuje, jeśli jest to zwiększa liczbę wystąpień.
    :param line: line: wiersz z pliku ze słowami
    :param words_dict: words_dict: słownik do uaktualnienia
    :param spec_char: przyjęty znak specjalny
    :return: uaktualniony słownik 'words' (w miejscu)
    """
    min_length = 2

    line = line.replace(spec_char, ' ')
    for word in line.split():
        if word in words_dict:
            words_dict[word][0] += 1
        else:
            if len(word) >= min_length:
                words_dict[word] = [1, len(word)]


if __name__ == '__main__':
    main()
