# extract unused - "bad words" from the text file
from pathlib import Path


def get_bad_words_from_txt_file(path_to_txt: str) -> str:
    with open(path_to_txt, 'r') as txt_file:
        words_to_remove = "|".join([word.strip() for word in txt_file.readlines()])
    return f"r'{words_to_remove}'"


def add_bad_words_from_list(words_list, bad_word_file):
    with open(bad_word_file, 'a') as text_file:
        for word in words_list:
            if word not in get_bad_words_from_txt_file(bad_word_file):
                text_file.write(word.lower() + '\n')


bad_word_file = f'{Path.home()}/Documents/keywords/bad_words.txt'

if __name__ == '__main__':
    # print(get_bad_words_from_txt_file('/Users/evgeniy/Documents/keywords/bad_words.txt'))
    add_bad_words_from_list(['bad_words_list'])
