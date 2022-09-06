import spacy
import re
class EntProcessor:

    def process_names_from_string(self, string):
        nlp = spacy.load("en_core_web_md")

        lowerString = string.lower()

        doc = nlp(lowerString)

        #test
        # for ent in doc.ents:
        #     print("LABELS: \n", ent.text, "    ", ent.label_)


        properNouns = " ".join([(token.text) for token in doc if token.pos_ == "PROPN"])
        pnDoc = nlp(properNouns)

        for token in pnDoc:
            print("POS: \n", token.text, "   ", token.pos_)

        persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"] #<--- back to doc
        orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        
        print("tokens:   ", [token for token in doc])
        print("PN tokens:   ", [token for token in pnDoc])
        print("persons:   ", persons, "   orgs:    ", orgs)

        if len(persons): return persons[0] 
        elif len(orgs): return orgs[0]
        else: return ""
        

    def process_names_from_lists(self, hrefs):
        #get rid of separator chars and replace with spaces firts
        allLinks = ""#.join(hrefs)#[link for link in hrefs]
        for link in hrefs:
            #for marker in ["-", "/", "\\", ".", ]:
            extracted = re.sub('[^a-zA-Z0-9\n\.]', ' ', link)
            allLinks += extracted
        result = ""
        if len(allLinks):
            result = self.process_names_from_string(allLinks)

        return result


