from pymystem3 import Mystem

from regex_tools import extract_words_no_digits, keywords_optimization


def lema_minus_bad_words(any_text: str):
    all_words_list = lema(any_text)
    return keywords_optimization(", ".join(all_words_list))


def lema(any_text: str) -> list:
    lemmatized_words_lst = extract_words_no_digits(Mystem().lemmatize(any_text))
    return [word for word in lemmatized_words_lst if len(word) > 2]


if __name__ == '__main__':
    print(lema(
        'XXVI Петербургский международный экономический форум (ПМЭФ) 2023 '
        'в конгрессно-выставочном центре (КВЦ) "Экспофорум". '
        'Генеральный директор компании «Метеор Лифт» (Meteor lift) Игорь Майоров.'))
