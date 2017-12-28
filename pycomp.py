# pycomp.py -- kompresuje pliki tekstowe metodą słownikową
# wersja 0.1
# tylko ASCII ?

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

    # words_list = list(words_dict.items())
    # words_len_3 = sorted([wl3 for wl3 in words_list if wl3[1][0] == 3], key=itemgetter(1), reverse=True)
    # words_len_4 = sorted([wl4 for wl4 in words_list if wl4[1][0] == 4], key=itemgetter(1), reverse=True)
    # words_len_more_4 = sorted([wlm4 for wlm4 in words_list if wlm4[1][0] > 4], key=itemgetter(1))

    # Utworzenie posortowanej tablicy słów dla nagłówka
    words_sorted_list = sorted(words_dict.items(), key=itemgetter(1), reverse=True)
    for n, (word, stats) in enumerate(words_sorted_list):
        print("%3d%13s\t%d\t%d" % (n, word, stats[0], stats[1]))

    # for n, (word, stats) in enumerate(words_len_3):
    #     print("%d%13s\t%d\t%d" % (n, word, stats[0], stats[1]))
    # print()
    # for n, (word, stats) in enumerate(words_len_4):
    #     print("%d%13s\t%d\t%d" % (n, word, stats[0], stats[1]))
    # print()
    # for n, (word, stats) in enumerate(words_len_more_4):
    #     print("%d%13s\t%d\t%d" % (n, word, stats[0], stats[1]))

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
