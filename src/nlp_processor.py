import spacy

class EntProcessor:

    def process_names_from_string(self, string):
        nlp = spacy.load("en_core_web_md")

        lowerString = string.lower()

        doc = nlp(lowerString)

        #test
        # for ent in doc.ents:
        #     print("LABELS: \n", ent.text, "    ", ent.label_)


        properNouns = "".join([(token.text + " ") for token in doc if token.pos_ == "PROPN"])
        pnDoc = nlp(properNouns)

        for token in pnDoc:
            print("POS: \n", token.text, "   ", token.pos_)

        persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"] #<--- back to doc
        orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        
        print("tokens:   ", [token for token in doc])
        print("PN tokens:   ", [token for token in pnDoc])
        print("persons:   ", persons, "   orgs:    ", orgs)
        return persons, orgs

    def process_names_from_lists(self, hrefs):
        allLinks = "".join(hrefs)#[link for link in hrefs]
        persons, orgs = [], []
        if len(allLinks):
            persons, orgs = self.process_names_from_string(allLinks)

        return persons, orgs


