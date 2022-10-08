import spacy
import re
from pprint import pprint
#test
from spacy.matcher import Matcher

class EntProcessor:

    def process_names_from_string(self, string, language_model):

        #nlp = spacy.load("en_core_web_lg")
        nlp = language_model

        #test
        string = string.replace("-", " ").replace("|", "").replace("/", " ")
        string = re.sub('[^a-zA-Z0-9\n\.]', ' ', string)

        doc = nlp(string)

        print("S T R I N G G G G :    ", string)


        # persons = [ent.text for ent in doc.ents if ent.label_ == "NAME_SURNAME"]
        # names = [ent.text for ent in doc.ents if ent.label_ == "NAME"]

        persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        
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


        # print("persons:   ", persons)#, "   orgs:    ", orgs)

        res = ""

        # if len(spans) and len(spans[0].text) > 1: res = spans[0].text
        # elif len(persons): res = persons[0] 
        # elif len(names): res = names[0]

        if len(persons): res = persons[0] 

        return res
        

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


