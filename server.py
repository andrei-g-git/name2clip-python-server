# from urllib import response
# from fastapi import FastAPI, HTTPException
# from starlette.responses import Response
# app = FastAPI()

# @app.get('/abc')
# async def doAbc() -> response:
#     return "hayyyaaa"




from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import json
from bs4 import BeautifulSoup

PORT = 9999
HOST = "localhost"

class TestServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        self.path = "/abc"

        self.send_header('Access-Control-Allow-Origin', '*')        
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        self.wfile.write(bytes("just some generic response", "utf-8")) 



    # def do_POST(self):

    #     print("blaaaaaaaaaaah")

    #     self.send_response(200)  
    #     self.path = "/def"
    #     self.send_header('Access-Control-Allow-Origin', '*')  
    #     self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    #     self.send_header('Access-Control-Allow-Methods', 'POST')
    #     self.send_header("Content-type", "text/plain")

    #     contentLength = int(self.headers.get("Content-length"))
    #     body = self.rfile.read(contentLength) #hope it's a string...

    #     self.end_headers()

    #     print("data is: ", body.decode('utf-8')) 
    #     response = "the request you just made is:   " +  body.decode('utf-8')
    #     self.wfile.write(bytes(response, "utf-8"))


    def do_POST(self): 

        self.send_response(200)
        self.path = "/scraper"
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-type", "application/json")
        self.end_headers()

        length = int(self.headers.get("Content-length"))
        body = json.loads(
            self.rfile
                .read(length)
                .decode("utf-8")
        )

        print("raw body:  ", body["src"])

        res = requests.get(body["url"])
        content = res.content
        html = BeautifulSoup(content, "html.parser")

        src = body["src"]
        #string = json.dumps(src)
        # attrDict = {"src": ""}
        # attrDict["src"] = src
        # selector = "[src=%s]"%src
        #mediaTagThing = html.select("img[src='%s']"%src)
        #mediaTagThing = html.find_all(attrs={"src": "%s"%src})

        srcWithoutProtocol = src.replace("https:", "")
        mediaTagThing = html.find_all(attrs={
            "src": src,
            "src": srcWithoutProtocol
        })


        print("src:   ", body["src"])
        #print(string)
        print(mediaTagThing)
        #print(type(src), "   ", type(string))
        #print('img[src="%s"]'%src)
        print("is string? :", isinstance(src, str))

        #find_context_element_from_all("src", src, html)

def find_context_element_from_all(attributeType, attributeValue, soup):
    tagsWithSrc = soup.select("[src]")
    #contextElements = filter(lambda elem: (elem["src"] == attributeValue), tagsWithSrc)

    srcWithoutProtocol = attributeValue.replace("https:", "")


    contextElements = []
    for tag in tagsWithSrc:
        print(">>>>>>>>>>>>>    ", tag["src"])
        if tag["src"] == attributeValue or tag["src"] == srcWithoutProtocol:
            contextElements.append(tag)


    #length = sum(1 for item in contextElements)
    length = len(contextElements)
    if length > 0: 
        #print(next(contextElements))
        print(contextElements[0])
    else: 
        print("contextElements is empty")
    print(attributeValue)
    #print(tagsWithSrc)


def findContextElement(src):
    abc = src
    #nothing works
    #getting the element like this doesn't work 

    #  element = html.find_all(attrs={"src": "%s"%src})

    #feeding a dictionary doesn't work
    #    attrDict = {"src": ""}
    #    attrDict["src"] = src
    #     element = html.find_all(attrs=attrDict)


    #or using a selector ... no go
    #      element = html.select('img[src="%s"]'%src)

    #I don't goddamn know, python sucks





#test --works
# req = requests.get("https://bustybloom.com")
# print(req)
# print(req.content)


server = HTTPServer((HOST, PORT), TestServer)
print("server running at ", HOST, " ", PORT)
server.serve_forever()
server.server_close()
print("server stopped...")