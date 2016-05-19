RELATION_INDICATORS_BEFORE_MIDDLE = [["kinderen van", "en"], ["zoon van", "en"], ["dochter van", "en"]]

RELATION_INDICATORS_MIDDLE = {"gehuwd met": "married with",
                              "weduwe van": "widow of",
                              "weduwe": "widow of",
                              "en zijn vrouw": "husband of",
                              ", weduwe van": "widow of",
                              "weduwnaar van": "widower of",
                              "vrouw van": "wife of",
                              ", gehuwd met": "married with",
                              "man van": "husband of",
                              "weduwe wijlen": "widow of",
                              ", weduwnaar van": ", wedower of",
                              ", de weduwe van": "widow of",
                              "getrouwt met": "married with",
                              "huijsvrouw van": "wife of",
                              "weduwnaar": "widower of",
                              "weduwe van wijlen": "widow of",
                              ", de weduwe": "widow of",
                              ", weduwe": "widow of",
                              ", vrouw van": "wife of",
                              ", huisvrouw van": "wife of",
                              "en haar man": "wife of",
                              "huisvrouw van": "wife of",
                              "en zijn huisvrouw": "husband of",
                              "getrouwd met": "married with",
                              "echtgenote van": "married with",
                              }
#                               "zoon van": "son of",
#                               ", dochter van": "daughter of",
#                               ", zoon van": "son of",
#                               "dochter van": "daughter of",
#                               "dochter": "daughter of"
# }

def extract_relations(references, word_list):
    """
        uses the pre-defined patterns to find relations between individuals
    """
    relations = []
    for index1, ref1 in enumerate(references):
        for index2, ref2 in enumerate(references):

            start_of_ref1 = ref1['position_in_processed_test']
            end_of_ref1 = ref1['position_in_processed_test'] + \
                          len(ref1['given_name'].split())+ \
                          len(ref1['prefix'].split()) + \
                          len(ref1['family_name'].split())
            start_of_ref2 = ref2['position_in_processed_test']
            end_of_ref2 = ref2['position_in_processed_test'] + \
                          len(ref2['given_name'].split())+ \
                          len(ref2['prefix'].split()) + \
                          len(ref2['family_name'].split())

            if index2 == index1 + 1:
                term = ' '.join(word_list[end_of_ref1: start_of_ref2])
                if term in RELATION_INDICATORS_MIDDLE.keys():
                    relations.append(
                        {"ref1": ref1, "ref2": ref2, "relation": RELATION_INDICATORS_MIDDLE[term]})




                # to detect relations in patterns like "Gerrit Hendrix en Hendersken Thijssen echtelieden"
                try:
                    term1 = ' '.join(word_list[end_of_ref1: start_of_ref2])
                    term2 = word_list[end_of_ref1]
                    if term1 == "en" and (term2 == "echtelieden" or term2 == "e"):
                        relations.append({"ref1": ref1, "ref2": ref2, "relation": "husband of"})
                except:
                    pass

                # detect relations in patterns like "Jorden Thomassen en Catharina Hendriks zijn vrouw"
                try:
                    term1 = ' '.join(word_list[end_of_ref1: start_of_ref2])
                    term2 = ' '.join(word_list[end_of_ref2: end_of_ref2 + 2])
                    if term1 == "en" and term2 == "zijn vrouw":
                        relations.append({"ref1": ref1, "ref2": ref2, "relation": "husband of"})
                except:
                    pass

                # detect relations in like "kinderen van Johannes Janse Smits en Antonetta Jan Roeloff Donckers"
                try:
                    term1 = ' '.join(word_list[start_of_ref1 - 2:start_of_ref1])
                    term2 = ' '.join(word_list[end_of_ref1:start_of_ref2])
                    if [term1, term2] in RELATION_INDICATORS_BEFORE_MIDDLE:
                        relations.append({"ref1": ref1, "ref2": ref2, "relation": "married with"})
                except:
                    pass

                    # TODO: use "te" to extract locations. Or use the Lexicon of location names for this!

    return relations
