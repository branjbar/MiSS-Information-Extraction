"""
a class to extract names.

"""
import module_names, module_refs, module_rels, module_preprocess
import re  # use regex to split words on capital letters

import import_db

import_db.init()


# TODO: other patterns for relationship: kinderen van [blah] en [blue]
# TODO: other patterns for relationship: zoon van [blah] en [blue]
# TODO: other patterns for relationship: dochter van [blah] en [blue]


class Nerd():
    """
    a full class for named entity recognition
    """

    def __init__(self, text, unique_id=None):
        """
        receives a raw text and applied preprocessing and then extracts important features
        such as relationships and references.
        
        :param text: the raw text
        :param unique_id: the unique id that allows us to keep track of errors and make future improvements
        :return: so many things.
        """
        self.text = text  # the raw text
        self.unique_id = unique_id  # the unique id we use for logging
        self.pp_text = ''  # pre-processed text
        self.word_list = []  # list of words which appear in the text
        self.word_list_labeled = {}  # list of words with labels
        self.references = []  # list of references
        self.relations = []  # list of relationships

        self.pp_text = module_preprocess.pre_processing(self.text)

        if len(self.text) > 3:
            self.word_list = self.pp_text.split()
            self.word_list_labeled = module_names.extract_names(self.word_list, self.unique_id)

    def get_references(self):
        """
            extracts the references and returns them
        """
        if not self.references:
            self.references = module_refs.extract_references(self.word_list, self.word_list_labeled, self.unique_id)
        return self.references

    def get_relations(self):
        """
            extracts the relationships and returns them
        """

        # first, make sure you have the references extracted
        if not self.references:
            self.references = module_refs.extract_references(self.word_list, self.word_list_labeled)

        # second, make sure you have the relations extracted
        if not self.relations:
            self.relations = module_rels.extract_relations(self.references, word_list)
        return self.relations


    def get_highlighted_text(self):
        """
        this highlights the extracted references
        """
        # first, make sure you have the references extracted
        if not self.references:
            self.references = module_refs.extract_references(self.word_list, self.word_list_labeled, self.unique_id)

        self.hl_text = ' ' + self.pp_text  # the space in the begining is to let the single names be chosen from the begining

        # first highlight the full names
        for ref in self.references:
            ref_name_with_dash = ref['given_name'] + ' - ' + ref['prefix'] + ' - ' + ref['family_name']
            ref_name_with_dash = ref_name_with_dash.replace('-  -', '--')
            ref_name = ref['given_name'] + ' ' + ref['prefix'] + ' ' + ref['family_name']
            ref_name = ref_name.replace('  ', ' ').strip()  # in case an extra space is added

            if ref['family_name']:
                self.hl_text = self.hl_text.replace(ref_name, """<span style="background-color: #FFFF00">%s</span>"""
                                                    % ref_name_with_dash)

        # Now, highlight the single names
        for ref in self.references:
            ref_name = ref['given_name'] + ' ' + ref['prefix'] + '' + ref['family_name']
            ref_name = ref_name.replace('  ', ' ').strip()  # in case an extra space is added

            if not ref['family_name']:
                self.hl_text = self.hl_text.replace(' ' + ref_name + ' ',
                                                    """ <span style="background-color: #8CBF26">%s</span> """
                                                    % (ref_name))

        self.hl_text = self.hl_text.replace('*', ' ')

        return self.hl_text


if __name__ == "__main__":
    text1 = """
            Testament van Huwelijkse voorwaardes tussen ijsken dochter PeterAdriaenGerits van de Loo inwoner St. Michielsgestel met Lijsken 
            dochter Dirck Janssen van den Oetelaer, eerder weduwe van Joffrouw =Jan Wouter Goijaerts en daarvoor weduwe van 
            Willem Gerits, inwoonster Den Bosch. 1ABC 11.
            """

    nerd = Nerd(text1)

    print "\nTEXT\n", nerd.pp_text

    print "\nEXTRACTIONS"

    for ref in nerd.get_references():
        print ref['given_name'], '|', ref['prefix'], '|', ref['family_name']

    print "\nHTML OUTPUT"
    print nerd.get_highlighted_text()
