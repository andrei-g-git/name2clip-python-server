# from urllib import response
# from fastapi import FastAPI, HTTPException
# from starlette.responses import Response
# app = FastAPI()

# @app.get('/abc')
# async def doAbc() -> response:
#     return "hayyyaaa"





# def do_GET(self):
#     self.send_response(200)
#     self.send_header('Access-Control-Allow-Origin', '*')           
#     self.end_headers()





# from http.server import *
  
# class GFG(BaseHTTPRequestHandler):
    
#     def do_GET(self):
        
#         self.send_response(200)
          
#         self.send_header('content-type', 'text/html')
#         self.send_header('Access-Control-Allow-Origin', '*')    
#         self.end_headers()
        

# port = HTTPServer(('', 5555), GFG)
  
# port.serve_forever()    




from http.server import HTTPServer, BaseHTTPRequestHandler

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



    def do_POST(self):
        self.send_response(200)  
        self.path = "/def"
        self.send_header('Access-Control-Allow-Origin', '*')  
        self.send_header("Content-type", "text/plain")

        contentLength = int(self.headers.get("Content-length"))
        body = self.rfile.read(contentLength) #hope it's a string...

        self.end_headers()

        print("data is: ", body.decode('utf-8')) 
        response = "the request you just made is:   " +  body.decode('utf-8')
        self.wfile.write(bytes(response, "utf-8"))


server = HTTPServer((HOST, PORT), TestServer)
print("server running at ", HOST, " ", PORT)
server.serve_forever()
server.server_close()
print("server stopped...")