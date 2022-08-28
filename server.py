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



#test --works
# req = requests.get("https://bustybloom.com")
# print(req)
# print(req.content)


server = HTTPServer((HOST, PORT), TestServer)
print("server running at ", HOST, " ", PORT)
server.serve_forever()
server.server_close()
print("server stopped...")