import re  # use regex to split words on capital letters
from datetime import datetime

# 64% of people don't have prefix in their name!, 35% have one of the prefixes in following list, Less than 1% have other prefixes
PREFIXES = ['van', 'de', 'van der', 'van den', 'van de', 'den', 'vanden', 'vander', 'vande']

FREQ_NAMES = ['te', 'kinderen', 'dochter']

# Labels we assign to words
LABELS = {1: 'NAME    ', 2: 'PREFIX   ', 3: 'FAKE     ', 4: 'FREQUENT', -1: 'NOT_NAME', None: 'UNKNOWN', 5: 'DIGIT    '}



import import_db


def extract_names(word_list, unique_id):
    """ (list) --> (dist)
        for each word the specifications are reported:
        1 : words started with capital letter
        2 : last name prefix
        3 : First word of the whole paragraph which continues with a capital letter word
        4 : Very frequent words
        5 : Digit
        -1: has capital letter but is not a name
    """

    # get a list of words from pre-processed words.
    word_list_labeled = {}  # for word specific

    # search for names and digits
    for index, word in enumerate(word_list):
        word_list_labeled[index] = None

        # if word starts by a capital letter and has at least three letters
        if re.match('[A-Z][a-z]+', word):  # and index > 0:
            word_list_labeled[index] = 1  # i.e., Name


        # A capital letter followed by a dot
        if re.match('[A-Z]\.', word):
            word_list_labeled[index] = 1

        if re.match('\d+', word):
                word_list_labeled[index] = 5  # i.e., Digit

            # search for last name prefixes
    for index, word in enumerate(word_list):
        # one component prefixes, happen if before and after them we have names
        if word in PREFIXES \
                and word_list_labeled.get(index - 1) == 1 \
                and word_list_labeled.get(index + 1) == 1:
            word_list_labeled[index] = 2

        # two component prefixes, happen if before and after them we have names
        if index < len(word_list) - 1 \
                and word + " " + word_list[index + 1] in PREFIXES \
                and word_list_labeled.get(index - 1) == 1 \
                and word_list_labeled.get(index + 2) == 1:
            word_list_labeled[index] = 2
            word_list_labeled[index + 1] = 2

    # let's double check every word which starts a sentence
    if word_list[0] in import_db.list_of_first_names:
        word_list_labeled[0] = 1
    else:
        word_list_labeled[0] = 3
        # store the error in a log file
        with open('warning_log.csv', 'a') as f:
            f.write("WARNING;" + str(unique_id) + ';' +
                    str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +
                    ';' + word_list[0] + ";;; Invalid Given Name \n")

    for index, word in enumerate(word_list):
        if index < len(word_list) - 1:
            if word == '.':
                if word_list[index + 1] in import_db.list_of_first_names:
                    word_list_labeled[index + 1] = 1
                else:
                    word_list_labeled[index + 1] = 3
                    # store the error in a log file
                    with open('warning_log.csv', 'a') as f:
                        f.write("WARNING;" + str(unique_id) + ';' +
                                str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +
                                ';' + word_list[index + 1] + ";;; Invalid Given Name \n")

    for index, word in enumerate(word_list):
        if word in FREQ_NAMES:
            word_list_labeled[index] = 4

    # this is to get rid of "Sint Oedenrode, Sint Janssstraat, Sint Janssstraat, etc."
    for index, word in enumerate(word_list):
        if word in ['Sint', 'St']:
            word_list_labeled[index] = -1

    return word_list_labeled
