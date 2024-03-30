import re
from bad_words_job import get_bad_words_from_txt_file


# keyword optimization with using "bad words" from the text file
def keywords_optimization(string, path_to_bad_words_file='/Users/evgeniy/Documents/keywords/bad_words.txt'):
    words_to_remove = get_bad_words_from_txt_file(path_to_bad_words_file)

    # remove bad words
    no_bad_words = re.sub(words_to_remove, "", string).strip()

    # remove doubles
    cleaned_string = re.sub(r'\b(\w+)\b(?=.*\b\1\b)', r'', no_bad_words)

    # Remove all punctuation except commas
    cleaned_string = re.sub(r'(?<!\w)[^\w\s,-]|[^\w\s,-](?!\w)', '', cleaned_string)

    # Extract words and separate with commas
    words = re.findall(r'\b[\w-]+\b', cleaned_string)
    result = ', '.join(words)

    # set limit of keywords
    while len(result) > 500:
        del words[-1]
        result = ', '.join(words)

    return result


if __name__ == '__main__':
    print(keywords_optimization('комбинат, агропромышленный, холдинг, 222, холдинг !! ;'))
