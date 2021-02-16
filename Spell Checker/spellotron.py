"""
File: spellotron.py
Language: Python3
Author: Dhruv Rajpurohit
Description: The code is uses to correct words in a text file.
"""
from sys import argv

KEY_ADJACENCY_FILE = "keyboard_letters.txt"
LEGAL_WORD_FILE = "american_english.txt"
ALPHABET = "ABCDEDFGHIJKLMNOPQRSTUVXYZabcdefghijklmnopqrstuvwxyz"
PUNCTUATION = ".![]{}(),;\'\"/\\"
USAGE = "Usage: python3.7 spellotron.py words/lines [filename]"


def k_dict():
    """
    creates a dictionary of letters in keyboard
    :return: dictionary
    """
    letter_dict = {}
    file = open(KEY_ADJACENCY_FILE)
    for line in file:
        line = line.strip()
        letters = line.split(" ")
        letter_dict[letters[0]] = letters[1:len(letters)]
    return letter_dict


def sorted_line(line):
    """
    The function sorts the line
    :param line: line to be sorted
    :return: sorted line
    """
    chars = [c for c in line]
    chars.sort()
    return "".join(chars)


def anagram():
    """
    The function adds words from the file to a list.
    The function also sorts the words in alphabetical order same as a dictionary.
    :return: the sorted dictionary
    """
    english_dict = {}
    open_file = open(LEGAL_WORD_FILE)
    for line in open_file.readlines():
        line = line.strip()
        key = sorted_line(line)
        if key in english_dict:
            v = english_dict.get(key) + "," + line
            english_dict[key] = v
        else:
            english_dict[key] = line
    return english_dict


THESAURUS = anagram()


def quick_look(word):
    """
    The function is used to look up the word in the dictionary
    param word: word being searched
    """
    s_word = "".join(sorted_line(word))
    if s_word in THESAURUS.keys():
        possibility = THESAURUS[s_word]
        return word in possibility
    return False


def sp_words(text):
    """
    a loist of possibilities of the adjacent keys
    param text: the text file being processed through the code
    """
    words = []
    build_up = ""
    while True:
        for char_idx in range(len(text)):
            if text[char_idx] not in ALPHABET or char_idx == len(text) - 1:
                if build_up != "":
                    if char_idx == len(text) - 1:
                        build_up += text[len(text) - 1]
                    words.append(build_up)
                build_up = ""
            else:
                build_up += text[char_idx]
        return words


def replace_letter(word, index, letter):
    """
    The code replaces the right letter with the wrong one
    :param word: The word in which changes are to be made
    :param index: The index at which the letter will be replaced
    :param letter: The letter will be replaced
    :return: The word with the replaced letter
    """
    wd = word[0:index]
    index = word[index+1:len(word)]
    return wd + letter + index


def letter_replacement(word):
    """
    the code helps to find the word by replacing the letters
    :param word: The word in which changes were to made
    :return: The changed word
    """
    qwerty = k_dict()
    possibility = []
    while True:
        for i in range(len(word)):
            adjacent_keys = qwerty[word[i]]
            for adj_key in adjacent_keys:
                new_word = replace_letter(word, i, adj_key)
                if quick_look(new_word):
                    possibility.append(new_word)
                    break
        if not possibility:
            return None
        else:
            return possibility[0]


def letter_insertion(word, idx, letter):
    """
    Inserts a letter
    :param word: the word in which the letter is to be added
    :param idx: The index at which the letter is inserted
    :param letter: The letter whihc has been inserted
    :return: The changed word
    """
    wd = word[0:idx]
    index = word[idx:len(word)]
    return wd + letter + index


def insert_letter(word):
    """
    To find the word after inserting letters
    :param word: The word to be changed
    :return: The changes made
    """
    possibilities = []
    while True:
        for idx in range(len(word)):
            for letter in ALPHABET:
                new_word = letter_insertion(word, idx, letter)
                if quick_look(new_word):
                    possibilities.append(new_word)
                    break
        if not possibilities:
            return None
        else:
            return possibilities[0]


def remove_letter(word, idx):
    """
    Removes a letter
    :param word: The word to be changed
    :param idx: The index at which the letter is removed
    :return: The new word
    """
    wd = word[0:idx]
    index = word[idx+1:len(word)]
    return wd + index


def letter_removal(word):
    """
    Searches for the letter by removing a certain letter
    :param word: The word where the changes are made
    :return: The possibilities of the words
    """
    possibilities = []
    while True:
        for idx in range(len(word)):
            new_word = remove_letter(word, idx)
            if quick_look(new_word):
                possibilities.append(new_word)
                break
        if not possibilities:
            return None
        else:
            return possibilities[0]


def strategies(word):
    """
    the code uses the strategies to find the appropriate word
    :param word: The word on which all the strategies are performed on
    :return: The changes made to word
    """
    """
    Applies all of the defined strategies (Replacement, Removal, Insertion) on the word to find english matches
    param word: The word that will be modified
    """
    replaced = letter_replacement(word)
    removed = letter_removal(word)
    inserted = insert_letter(word)
    while True:
        if replaced is not None:
            return replaced
        if removed is not None:
            return removed
        if inserted is not None:
            return inserted
        return None


def is_capital(word):
    """
    To see if the word is capitalized or not
    :param word: The word which is checked
    :return: if the the word is capitalized or not
    """
    wd = word[0]
    upper_case = wd.isupper()
    return upper_case


def capitalize(word):
    """
    Turn the word to a capital one
    :param word: The word on which the changes are made
    :return: The upper case word
    """
    wd = word[0]
    wd_1 = word[1:]
    upper_case = wd.upper
    cap_word = upper_case + wd_1
    return cap_word


def auto_correct(errors, mode):
    """
    Perform all the cases to correct the word and prints the results
    :param errors: The misspelled words
    :param mode: The string which will be used to identify the data
    """
    oxford = {}
    words = sp_words(errors)
    mistakes = []
    corrected_words = []
    unknown = []
    correction = ""

    for word in words:
        word = word.strip()
        word_is_cap = is_capital(word)
        word = word.lower()
        if not quick_look(word):
            mistakes.append(word)
            corrected_word = strategies(word)
            if corrected_word is None:
                unknown.append(word)
            else:
                if not word_is_cap:
                    corrected_words.append(corrected_word)
                    oxford[word] = corrected_word
        else:
            correction = errors
    for misspelled in oxford:
        correction = correction.replace(misspelled, oxford[misspelled])
        correction = correction.replace("\n ", "\n")
    if mode == "lines":
        print(correction)
    elif mode == "words":
        while True:
            for misspelled in oxford:
                print(misspelled, "->", oxford[misspelled])
            print()
    print(len(words), "words read from file")
    print()
    print(len(corrected_words), "Corrected Words")
    print(list(oxford.keys()))
    print()
    print(len(unknown), "unknown words")
    print(unknown)


def read_text(filename):
    """
    Reads the text file
    param filename: file that is being read
    """
    file = open(filename)
    lines = file.readlines()
    len_line = len(lines)
    text = ""
    while True:
        for line_idx in range(len(lines)):
            text += lines[line_idx]
            if line_idx < (len_line - 1):
                text += " "
        return text


def check_usage_error(args):
    """
    Checks the command to start the programs is right
    :param args:list of arguments
    :return: True or False according to conditions set
    """
    valid = True
    valid_arg = True
    not_valid = False
    if len(args) < 2:
        print(USAGE)
        return False, False
    if args[1] not in ["words", "lines"]:
        print(USAGE)
        return False, False
    if valid and valid_arg:
        if len(args) < 3:
            print("reading from stdin")
        return True, not_valid
    else:
        print(USAGE)
        return False, False


def main():
    valid_args, reading = check_usage_error(argv)
    mode = argv[1]
    if not reading:
        filename = argv[2]
        text_data = read_text(filename)
    else:
        text_data = input("")
    auto_correct(text_data, mode)


if __name__ == "__main__":
    main()
