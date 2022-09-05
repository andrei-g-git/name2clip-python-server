from http.server import HTTPServer, BaseHTTPRequestHandler
from api_handlers import ApiHandler as API
from nlp_processor import EntProcessor 

class ScrapingServer(BaseHTTPRequestHandler):
    def do_POST(self):

        self.handle_post_headers("/scraper")

        api = API()

        body = api.load_request_body(self)
        src = body["src"]
        url = body["url"]
        print("==============================")
        soup = self.init_soup(api, url)

        #print(soup.prettify())

        parent, grandparent = api.get_element_hierarchy_from_src(src, soup)

        hrefs = []

        if parent != None or grandparent != None:
            hrefs = api.get_context_links(parent)
            if not len(hrefs):
                hrefs = api.get_context_links(grandparent)

        title = soup.find("title").text            

        #get the text from the surroundings too

        resultList = self.pick_best_name_candidate(
            EntProcessor(),
            title,
            src,
            hrefs,
            "awfaewfwaefawefe"
        )
        print("RRRRRRRESULT!!!!!!     ", resultList[0])

        #########
        self.wfile.write(bytes(resultList[0], encoding="utf-8"))



    def pick_best_name_candidate(self, entProcessor, title, src, hrefs, innerHtml):
        proc = entProcessor

        result = []
        persons, orgs = proc.process_names_from_string(title)
        print("11111")
        if len(persons):
            result = persons
        elif len(orgs):
            result = orgs
        else:
            persons, orgs = proc.process_names_from_string(src)
            print("22222")
            if len(persons):
                result = persons
            elif len(orgs):
                result = orgs
            else:
                persons, orgs = proc.process_names_from_lists(hrefs)
                print("33333")
                if len(persons):
                    result = persons
                elif len(orgs):
                    result = orgs
                else:
                    persons, orgs = proc.process_names_from_string(innerHtml)
                    print("44444")
                    if len(persons):
                        result = persons
                    elif len(orgs):
                        result = orgs     
        return result


    def init_soup(self, api, url):
        soup = api.init_soup(url)
        for data in soup(['style', 'script']):
            data.decompose()
        return soup


    def handle_post_headers(self, path):
        self.send_response(200)
        self.path = "/scraper"
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-type", "application/json")
        self.end_headers()

    @staticmethod
    def init_server(HOST, PORT):
        server = HTTPServer((HOST, PORT), ScrapingServer) #so this passes it's class before it can full initialize? ...
        print("server running at ", HOST, " ", PORT)
        server.serve_forever()
        server.server_close()
        print("server stopped...")
        
        return "Server running at ", HOST, "  on port ", PORT        