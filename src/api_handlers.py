import requests
import json
from bs4 import BeautifulSoup
import re

class ApiHandler:

    def load_request_body(self, server):
        length = int(server.headers.get("Content-length"))
        body = json.loads(
            server.rfile
                .read(length)
                .decode("utf-8")
        )

        print("src:   ", body["src"])
        return body

    def init_soup(self, url, headers):
        res = requests.get(url, headers=headers)
        print("LINKS #####  " ,res.links)
        content = res.text #res.content
        soup = BeautifulSoup(content, "html.parser")
        return soup

    def find_element_from_src(self, src, soup): 
        relativeSrc = src.split("/")[-1]
        regex = "%s$"%relativeSrc
        print("REGEX:    ", regex)
        matchingElements = soup.find_all(attrs={"src": re.compile(r'%s'%regex)})
        contextElement = None
        if len(matchingElements):
            contextElement = matchingElements[0]
        print("MATCHING ELEMENTS:    ", matchingElements)
        return contextElement

    def get_element_hierarchy_from_src(self, src, soup):
        context = self.find_element_from_src(src, soup)
        print("CONTEXT:", context  )
        parent, grandparent = None, None
        if context != None:
            parent = context.parent
            grandparent = parent.parent

        print("PARENT:   ", parent)
        print("GRAND PARENT:   ", grandparent)
        return context, parent, grandparent

    def get_alt_from_media(self, element):
        alt = ""
        if element != None:
            if element.get("alt"):
                alt = element.get("alt")
        return alt                

    def get_context_links(self, element):
        anchors = element.find_all("a")
        print("ANCHORS: ", anchors)
        for a in anchors:
            print("LINK TEXT >>>>>>>> : ", a.text)
        hrefs = [a.get("href") for a in anchors]
        print("HREFS =====: ",hrefs)
        return hrefs

