import spacy
import re

#test
from spacy.matcher import Matcher

class EntProcessor:

    def process_names_from_string(self, string):
        #nlp = spacy.load("en_core_web_lg")
        nlp = spacy.load("G:\\portfolio\\projects\\scraper\\models\\woman_first_names_and_surnames_ner_model_2")

        #lowerString = string.lower()

        #test
        string = string.replace("-", "").replace("|", "")
        string = re.sub('[^a-zA-Z0-9\n\.]', ' ', string)

        doc = nlp(string)

        print("S T R I N G G G G :    ", string)


        #properNouns = " ".join([(token.text) for token in doc if token.pos_ == "PROPN"])
        #pnDoc = nlp(properNouns)

        # for token in pnDoc:
        #     print("POS: \n", token.text, "   ", token.pos_)
        # for ent in pnDoc.ents:
        #     print("LABELS: \n", ent.text, "    ", ent.label_)

        # persons = [ent.text for ent in pnDoc.ents if ent.label_ == "PERSON"]
        # orgs = [ent.text for ent in pnDoc.ents if ent.label_ == "ORG"]
        persons = [ent.text for ent in doc.ents if ent.label_ == "NAME_SURNAME"]
        names = [ent.text for ent in doc.ents if ent.label_ == "NAME"]
        #orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        
        if '-' in persons: 
            persons.remove('-')
        if '-' in names: 
            names.remove('-')            
        # if '-' in orgs: 
        #     orgs.remove('-')

        #test
        # pattern = [{"ENT_TYPE": "PERSON"}, {"ENT_TYPE": "PERSON"}] #good, if it's separated by comma it won't match
        # matcher = Matcher(nlp.vocab)
        # matcher.add("first-last-names", [pattern])
        # matches = matcher(doc)
        # for match_id, start, end in matches:
        #     #string_id = nlp.vocab.strings[match_id]  # Get string representation
        #     span = doc[start:end]  # The matched span
        #     print("*************************** \n first and last name: ", span.text)



        print("tokens:   ", [token for token in doc])
        #print("PN tokens:   ", [token for token in pnDoc])
        print("persons:   ", persons)#, "   orgs:    ", orgs)

        if len(persons): return persons[0] 
        #elif len(orgs): return orgs[0]
        elif len(names): return names[0]
        else: return ""
        

    def process_names_from_lists(self, hrefs):
        #get rid of separator chars and replace with spaces firts
        allLinks = ""#.join(hrefs)#[link for link in hrefs]
        for link in hrefs:
            #for marker in ["-", "/", "\\", ".", ]:
            extracted_old = re.sub('[^a-zA-Z0-9\n\.]', ' ', link)

            #new don't know how to remove '-' with regex
            extracted = extracted_old.replace("-", " ")

            allLinks += extracted
        result = ""
        if len(allLinks):
            result = self.process_names_from_string(allLinks)

        return result


