from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import json
from bs4 import BeautifulSoup
import html
import re
import spacy

class ScrapingServer(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.path = "/scraper"
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(bytes("main server app reporting in...", encoding="utf-8"))

    @staticmethod
    def init_server(HOST, PORT):
        server = HTTPServer((HOST, PORT), ScrapingServer) #so this passes it's class before it can full initialize? ...
        print("server running at ", HOST, " ", PORT)
        server.serve_forever()
        server.server_close()
        print("server stopped...")
        
        return "Server running at ", HOST, "  on port ", PORT        