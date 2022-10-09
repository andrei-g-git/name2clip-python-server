import spacy
import re
from pprint import pprint
from spacy.matcher import Matcher

class EntProcessor:

    def process_names_from_string(self, string, language_model):

        nlp = language_model

        #test
        string = string.replace("-", " ").replace("|", "").replace("/", " ")
        string = re.sub('[^a-zA-Z0-9\n\.]', ' ', string)

        doc = nlp(string)

        print("S T R I N G G G G :    ", string)

        ner_label = "PERSON"
        label_dict = nlp.pipe_labels
        all_ner_labels = label_dict["ner"]
        if "NAME_SURNAME" in all_ner_labels:
            ner_label = "NAME_SURNAME"

        # persons = [ent.text for ent in doc.ents if ent.label_ == "NAME_SURNAME"]
        # names = [ent.text for ent in doc.ents if ent.label_ == "NAME"]

        persons = [ent.text for ent in doc.ents if ent.label_ == ner_label]
        
        if '-' in persons: 
            persons.remove('-')

        #test --- vocab is too small for this (10k tokens is small)
        # pattern = [{"ENT_TYPE": "NAME"}, {"ENT_TYPE": "SURNAME"}] #good, if it's separated by comma it won't match
        # matcher = Matcher(nlp.vocab)
        # matcher.add("first-last", [pattern])
        # matches = matcher(doc)
        # span = ""
        # count = 0
        # spans = []
        # pprint("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n MATCHES:  " + str(matches))
        # for match_id, start, end in matches:
        #     span = doc[start:end]  # The matched span
        #     count += 1
        #     print("% \n % \n " + str(count) + "% \n % \n ")
        #     print("################# start" + str(start) + "     end: " + str(end))
        #     print("*************************** \n first and last name: ", span.text)   
        #     spans.append(span)


        res = ""

        if len(persons): res = persons[0] 

        return res
        


