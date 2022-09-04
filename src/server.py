from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import json
from bs4 import BeautifulSoup
import html
import re
import spacy
from api_handlers import ApiHandler as API
from nlp_processor import EntProcessor 

class ScrapingServer(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.path = "/scraper"
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-type", "application/json")
        self.end_headers()

        api = API()

        body = api.load_request_body(self)

        src = body["src"]
        url = body["url"]
        print("==============================")
        print("URL ->>> ", url)

        soup = api.init_soup(url)  

        for data in soup(['style', 'script']):
            # Remove tags
            data.decompose()

        #print(soup.prettify())  #<------------

        parent, grandparent = api.get_element_hierarchy_from_src(src, soup)

        hrefs = api.get_context_links(parent)
        if not len(hrefs):
            hrefs = api.get_context_links(grandparent)

        title = soup.find("title").text            


        proc = EntProcessor()
        result = self.pick_best_name_candidate(
            proc,
            title,
            src,
            hrefs,
            "awfaewfwaefawefe"
        )

        print("RRRRRRRESULT!!!!!!     ", result)

        self.wfile.write(bytes(body["src"], encoding="utf-8"))

    def pick_best_name_candidate(self, entProcessor, title, src, hrefs, innerHtml):
        proc = entProcessor

        result = []

        persons, orgs = proc.process_names_from_string(title)
        if len(persons):
            result = persons
        elif len(orgs):
            result = orgs
        else:
            persons, orgs = proc.process_names_from_string(src)
            if len(persons):
                result = persons
            elif len(orgs):
                result = orgs
            else:
                persons, orgs = proc.process_names_from_lists(hrefs)
                if len(persons):
                    result = persons
                elif len(orgs):
                    result = orgs
                else:
                    persons, orgs = proc.process_names_from_string(innerHtml)
                    if len(persons):
                        result = persons
                    elif len(orgs):
                        result = orgs     

        return result




    @staticmethod
    def init_server(HOST, PORT):
        server = HTTPServer((HOST, PORT), ScrapingServer) #so this passes it's class before it can full initialize? ...
        print("server running at ", HOST, " ", PORT)
        server.serve_forever()
        server.server_close()
        print("server stopped...")
        
        return "Server running at ", HOST, "  on port ", PORT        