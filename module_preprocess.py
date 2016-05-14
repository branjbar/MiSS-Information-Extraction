import re  # use regex to split words on capital letters

PUNCTUATION_LIST = [',', ';', '.', ':', '[', ']', '(', ')', '"', "'", '-']


def pre_processing(raw_text):
    """
        preprocesses the text (mostly for notarial acts).
        E.g., adds space before and after punctuations
         replaces multiple spaces by single ones.
         detects the names connected to previous word
         also removing the starting digits
    """

    # remove the starting and ending spaces.
    text = raw_text.strip()

    # add space before and after punctuations
    for c in PUNCTUATION_LIST:
        text = text.replace(c, ' ' + c + ' ')
    text = text.replace('  ', ' ')

    # splitting the connected words by error using the upper case in between, e.g., "(=Beatrix)" or "PeterAdriaenGerits"
    # if I get some small letter or digit which continues with capital letter and agian small letters, add space.
    text = re.sub(r"(([a-z]|\d)([A-Z][a-z]))", r"\2 \3", text)

    # a symbol connected to some letters will be removed.
    text = re.sub(r"(([-!$%^&*()_+|~={}\[\]:<>?,.\/])(\w+))", r"\3", text)

    # words starting with digits and continuing with words will be seperated
    text = re.sub(r"((\d)([a-z|A-Z]+))", r"\2 \3", text)

    # to deal with "J . M . R. Gogel" and turn it to "J. M. R. Gogel"
    text = re.sub(r" ([A-Za-z]) \. ", r" \1. ", text)
    text = re.sub(r" ([A-Za-z]) \. ", r" \1. ", text)
    text = re.sub(r" ([A-Za-z]) \. ", r" \1. ", text)

    # add dot to the end of sentence
    if text.split()[-1] != '.':
        text += ' .'

    text = text.replace(' Van ', ' van ')
    text = text.replace(' Vanden ', ' vanden ')
    text = text.replace(' Vander ', ' vander ')
    text = text.replace(' Vande ', ' vande ')

    return text
