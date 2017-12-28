# pycomp.py -- kompresuje pliki tekstowe metodą słownikową
# wersja 0.1

import sys
from operator import itemgetter


def main():
    """ Główna funkcja programu. """

    # Przygotowanie informacji o statystyce słów w pliku
    file_name = sys.argv[1]
    words_dict = {}  # słownik {wyraz: [ilość wystąpień, długość]}

    with open(file_name, 'r') as input_file:
        for line in input_file:
            update_words_dict(line.rstrip(), words_dict, 2, 3)

    # Utworzenie posortowanej listy słów
    words_sorted_list = sorted(words_dict.items(), key=itemgetter(1), reverse=True)
    words_total = len(words_sorted_list)

    # Utworzenie listy słów dla nagłówka
    dst_words_index = 0
    src_words_index = 0

    words_0_to_9 = []
    while dst_words_index < 10 and src_words_index < words_total:
        if words_sorted_list[src_words_index][1][1] > 2:
            words_0_to_9.append(words_sorted_list[src_words_index])
            dst_words_index += 1
        src_words_index += 1

    for n, (word, stats) in enumerate(words_0_to_9):
        print("%3d%13s\t%d\t%d" % (n, word, stats[0], stats[1]))

    words_10_to_99 = []
    while dst_words_index < 100 and src_words_index < words_total:
        if words_sorted_list[src_words_index][1][1] > 3:
            words_10_to_99.append(words_sorted_list[src_words_index])
            dst_words_index += 1
        src_words_index += 1

    print("\n%d\n" % len(words_10_to_99))
    for n, (word, stats) in enumerate(words_10_to_99):
        print("%3d%13s\t%d\t%d" % (n + 10, word, stats[0], stats[1]))

    words_100_to_999 = []
    while dst_words_index < 1000 and src_words_index < words_total:
        if words_sorted_list[src_words_index][1][1] > 4:
            words_100_to_999.append(words_sorted_list[src_words_index])
            dst_words_index += 1
        src_words_index += 1

    print("\n%d\n" % len(words_100_to_999))
    for n, (word, stats) in enumerate(words_100_to_999):
        print("%3d%13s\t%d\t%d" % (n + 100, word, stats[0], stats[1]))

    print("\ntotal: %d" % words_total)
    print("dst: %d" % dst_words_index)
    print("src: %d" % src_words_index)

    # Zapisanie nagłówka w docelowym pliku
    # Kompresja pliku
    print("Gotowe.")


def update_words_dict(line, words_dict, min_repetitions, min_length):
    """
    Uaktualnie słownik 'words': jeśli nie ma w nim słowa to dopisuje, jeśli jest to zwiększa liczbę wystąpień.
    :param line: line: wiersz z pliku ze słowami
    :param words_dict: words_dict: słownik do uaktualnienia
    :param min_repetitions: minimalna wymagana ilość powtórzeń wyrazu
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

    for word in words_dict.copy():
        if words_dict[word][0] < min_repetitions:
            words_dict.pop(word)


if __name__ == '__main__':
    main()
