import spacy

class EntProcessor:

    def process_names_from_string(self, string):
        nlp = spacy.load("en_core_web_md")
        doc = nlp(string)

        persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"] # or ent.label_ == "ORG"]      # list comprehension
        orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        
        print("tokens:   ", [token for token in doc])
        print("persons:   ", persons, "   orgs:    ", orgs)
        return persons, orgs

    def process_names_from_lists(self, hrefs):
        persons = []
        orgs = []
        nlp = spacy.load("en_core_web_md")
        if len(hrefs):
            for link in hrefs:
                doc = nlp(link)
                persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"] 
                orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        return persons, orgs

