from http.server import HTTPServer, BaseHTTPRequestHandler
from api_handlers import ApiHandler as API
from nlp_processor import EntProcessor 

class ScrapingServer(BaseHTTPRequestHandler):
    def do_POST(self):
        print("received post request")
        self.handle_post_headers("/scraper")

        api = API()

        body = api.load_request_body(self)

        # src = ""
        # if "src" in body:
        src = body["src"]
            
        url = body["url"]
        print("==============================")
        headers = {'User-Agent': 'Mozilla/5.0'}
        soup = self.init_soup(api, url, headers)

        #test
        # f = open("F:\\zz delete\\demofile2.txt", "w", encoding="utf-8")
        # txt = '"""' + soup.prettify() + '"""'
        # f.write(txt)
        # f.close()

        #print("SOUPP ################################ \n", soup.prettify(), "\n ############################################")

        context, parent, grandparent = api.get_element_hierarchy_from_src(src, soup)
        alt = api.get_alt_from_media(context)

        hrefs = []

        if parent != None or grandparent != None:
            hrefs = api.get_context_links(parent)
            if not len(hrefs):
                hrefs = api.get_context_links(grandparent)

        print("ACTUAL HREFS ------: ", hrefs)

        title = soup.find("title").text            

        #get the text from the surroundings too

        result = self.pick_best_name_candidate(
            EntProcessor(),
            title,
            src,
            url,
            alt,
            hrefs,
            soup.text
        )
        print("RRRRRRRESULT!!!!!!     ", result)

        #########
        if len(result):
            self.wfile.write(bytes(result, encoding="utf-8"))
        else: 
            self.wfile.write(bytes("image", encoding="utf-8"))



    def pick_best_name_candidate(self, entProcessor, title, src, url, alt, hrefs, innerHtml):
        proc = entProcessor

        result = ""
        result = proc.process_names_from_string(title)
        print("11111")
        if not len(result):
            result = proc.process_names_from_string(alt)
            print("22222")
            if not len(result):
                links = hrefs.copy()
                links.insert(0, src)
                links.append(url)
                print("result HREF:   ", links, "FROMMMMMMMM:   ", hrefs)
                result = proc.process_names_from_lists(links)
                # if not len(result):
                #     result = proc.process_names_from_string(innerHtml)
                #     print("44444")   
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
        server = HTTPServer((HOST, PORT), ScrapingServer) #so this passes it's class before it can full initialize? ...
        print("server running at ", HOST, " ", PORT)
        server.serve_forever()
        server.server_close()
        print("server stopped...")
        
        return "Server running at ", HOST, "  on port ", PORT        