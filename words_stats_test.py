# words_stats_test.py -- pokazuje zawartość nagłówka do programu pycomp.py
# wersja 1.1

import sys
from operator import itemgetter


def main():
    """ Główna funkcja programu. """

    # Przygotowanie informacji o statystyce słów w pliku
    file_name = sys.argv[1]
    words_dict = {}  # słownik {wyraz: [ilość wystąpień, długość]}

    with open(file_name, 'r') as input_file:
        for line in input_file:
            update_words_dict(line.rstrip(), words_dict, 3)

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
        dst_word_indicator_length = len(str(dst_word_index)) + 1
        word_saved_space = word_length - dst_word_indicator_length
        word_dict_space = word_length + 1
        word_repeat = words_sorted_list[src_word_index][1][0]
        if word_saved_space * word_repeat > word_dict_space:
            words_list.append(words_sorted_list[src_word_index])
            dst_word_index += 1
        src_word_index += 1

    print("idx       słowo      il. wyst  długość")
    for n, (word, stats) in enumerate(words_list):
        print("%4d%13s\t%d\t%d" % (n, word, stats[0], stats[1]))

    print("\nCałkowita ilość słów: %d" % words_total)
    print("dst: %d" % dst_word_index)
    print("src: %d" % src_word_index)

    print("Gotowe.")


def update_words_dict(line, words_dict, min_length):
    """
    Uaktualnie słownik 'words': jeśli nie ma w nim słowa to dopisuje, jeśli jest to zwiększa liczbę wystąpień.
    :param line: line: wiersz z pliku ze słowami
    :param words_dict: words_dict: słownik do uaktualnienia
    :param min_length: minimalna wymagana długość wyrazu
    :return: uaktualniony słownik 'words' (w miejscu)
    """
    delimiters = ". , ; : ? $ @ ^ < > # % ` ! * - = ( ) [ ] { } / \" '".split()

    for sign in delimiters:
        line = line.replace(sign, " ")

    for word in line.split():
        if word in words_dict:
            words_dict[word][0] += 1
        else:
            if len(word) >= min_length:
                words_dict[word] = [1, len(word)]


if __name__ == '__main__':
    main()
