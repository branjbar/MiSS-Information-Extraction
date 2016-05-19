from datetime import datetime
import import_db


def extract_references(word_list, word_list_labeled, unique_id):
    """ (list) --> (list)
        analyses the ordered list of words and returns the references

    """
    refs_list = []
    reference = ''
    # need_last_name_flag = False
    for index, word in enumerate(word_list):
        if (reference and word_list_labeled[index] in [1, 2]
            or not reference and word_list_labeled[index] in [1]):  # if reference is empty we should start with a name
            reference += word + ' '
        else:
            reference = reference.strip().decode("ISO-8859-1").encode('utf8', 'ignore')
            ref_len = len(reference.split(' '))

            # make sure more than one name is extracted:

            if ref_len == 1:  # a single name
                if reference in import_db.list_of_first_names:
                    refs_list.append({"given_name": reference, "prefix": "",
                                      "family_name": "",
                                      "position_in_processed_test": index - ref_len
                                      })
                else:
                    if len(reference) > 1:
                        with open('warning_log.csv', 'a') as f:
                            f.write("WARNING;" + str(unique_id) + ';' +
                                    str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +
                                    ';' + reference + ";;; Invalid Given Name  \n")

            else:
                # let's assume the last word is family name, before that the words with small letter are preffix 
                # and the rest are give names.

                ref = split_full_name(reference)

                VALID_EXTRACTION = True

                # if the first name doesn't exist in database
                if ref[0].split() and not ref[0].split()[0] in import_db.list_of_first_names:
                    # store the error in a log file
                    with open('warning_log.csv', 'a') as f:
                        f.write("WARNING;" + str(unique_id) + ';' +
                                str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +
                                ';' + '; '.join(ref) + "; Given name is invalid \n")

                        # mean names are unforgivable
                if ref[0].split() and ref[0].split()[0] in import_db.list_of_starting_words:
                    # store the error in a log file
                    with open('error_log.csv', 'a') as f:
                        f.write("ERROR;" + str(unique_id) + ';' +
                                str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +
                                ';' + '; '.join(ref) + "; A Mean Name is found \n")

                        # this reference is not valid any more and can't be stored
                    VALID_EXTRACTION = False

                # the give name should not include any word which starts with small letter
                if ref[0].split() and not all([w[0].isupper() for w in ref[0].split()]):
                    # store the error in a log file
                    with open('error_log.csv', 'a') as f:
                        f.write("ERROR;" + str(unique_id) + ';' +
                                str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +
                                ';' + '; '.join(ref) + "; Problems with Given Name \n")

                        # this reference is not valid any more and can't be stored
                    VALID_EXTRACTION = False

                # all prefix words should start with small letter, otherwise something is going wrong!
                if ref[1].split() and not all([w[0].islower() for w in ref[1].split()]):
                    # store the error in a log file
                    with open('error_log.csv', 'a') as f:
                        f.write("ERROR;" + str(unique_id) + ';' +
                                str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +
                                ';' + '; '.join(ref) + "; Problems with Prefix \n")

                        # thir reference is not valid any more and can't be stored
                    VALID_EXTRACTION = False

                if VALID_EXTRACTION:
                    refs_list.append({"given_name": ref[0], "prefix": ref[1],
                                      "family_name": ref[2],
                                      "position_in_processed_test": index - ref_len
                                      })
            reference = ''

    return refs_list


def split_full_name(full_name):
    """
    uses a simple hueristic to split a full name into given name, prefix, family name
    
    
    please note that except from 0.17% of family names, for the rest each family name is a single word!  
    :param full_name:
    :return:
    """

    # the last word is assigned to family name
    family_name = full_name.split()[-1]

    # we start form the end and figure out what is prefix, what is first name
    prefix_start = -1
    flag = False
    for iter, word in enumerate(reversed(full_name.split()[:-1])):
        if not flag and not word[0].isupper():
            flag = True

        if flag and word[0].isupper():
            prefix_start = len(full_name.split()) - iter - 1
            break

    given_name = ' '.join(full_name.split()[:prefix_start])
    prefix = ' '.join(full_name.split()[prefix_start:-1])
    return [given_name.strip(), prefix.strip(), family_name.strip()]
