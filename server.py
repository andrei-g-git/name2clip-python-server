# from urllib import response
# from fastapi import FastAPI, HTTPException
# from starlette.responses import Response
# app = FastAPI()

# @app.get('/abc')
# async def doAbc() -> response:
#     return "hayyyaaa"




from functools import reduce
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import json
from bs4 import BeautifulSoup
import html
import re

PORT = 9999
HOST = "localhost"

class TestServer(BaseHTTPRequestHandler):

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

        print("src attribute:  ", body["src"])

        res = requests.get(body["url"])
        content = res.content
        soup = BeautifulSoup(content, "html.parser")

        src = body["src"]

        relativeSrc = src.split("/")[-1]

        print("RELATIVE SRC: ", relativeSrc)

        regex = "%s$"%relativeSrc
        matchingElements = soup.find_all(attrs={"src": re.compile(r'%s'%regex)})

        contextElement = matchingElements[0]

        grandparent = contextElement.parent.parent

        anchors = grandparent.find_all("a")

        hrefs = []
        for a in anchors:
            hrefs.append(a.get("href"))

        title = soup.find("title").text

        print("\n\n text:   ", grandparent.text)
        print("src:  ", src)
        print("hrefs: ", hrefs)
        print("TITLE:  ", title)

        #print("\n\n ^^^^^^^^^^^^^^^^^^^^^^ \n all inner text:   ", soup.text)



server = HTTPServer((HOST, PORT), TestServer)
print("server running at ", HOST, " ", PORT)
server.serve_forever()
server.server_close()
print("server stopped...")