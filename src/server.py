from http.server import HTTPServer, BaseHTTPRequestHandler
from api_handlers import ApiHandler as API
from nlp_processor import EntProcessor 
import pickle
class ScrapingServer(BaseHTTPRequestHandler):
    def do_POST(self):
        print("received post request")
        self.handle_post_headers("/scraper")

        api = API()

        body = api.load_request_body(self)
            
        url = body["url"]

        headers = {'User-Agent': 'Mozilla/5.0'}
        soup = self.init_soup(api, url, headers)

        title = ""
        if soup.find("title") != None and len(soup.find("title")):
            title = soup.find("title").text  

        src = body["src"]
        context, parent, grandparent = api.get_element_hierarchy_from_src(src, soup)
        alt = api.get_alt_from_media(context)

        #no idea how to pass a language model changed from the tk app other than  it being saved and loaded to and from disk:
        language_model = None
        with open("C:/My_Data/language_model_tkinter.pkl", "rb") as file:
            language_model = pickle.load(file)

        result = self.pick_best_name_candidate(
            EntProcessor(),
            language_model,
            title,
            url,
            alt
        )
        print("RRRRRRRESULT!!!!!!     ", result)

        #########
        if len(result):
            self.wfile.write(bytes(result, encoding="utf-8"))
        else: 
            self.wfile.write(bytes("image", encoding="utf-8"))



    def pick_best_name_candidate(self, entProcessor, model, title, url, alt):
        proc = entProcessor

        result = ""
        result = proc.process_names_from_string(title, model)
        print("11111")
        if not len(result):
            result = proc.process_names_from_string(alt, model)
            print("22222")
            if not len(result):
                result = proc.process_names_from_string(url, model)
                print("44444")   
        return result


    def init_soup(self, api, url, headers):
        soup = api.init_soup(url, headers)
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
        server = HTTPServer((HOST, PORT), ScrapingServer) #so this passes it's class before it can fully initialize? ... 
        print("server running at ", HOST, " ", PORT)
        server.serve_forever()
        server.server_close()
        print("server stopped...")
        
        return "Server running at ", HOST, "  on port ", PORT        