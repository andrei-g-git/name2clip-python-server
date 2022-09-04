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

    def init_soup(self, url):
        res = requests.get(url)
        print("LINKS #####  " ,res.links)
        content = res.text #res.content
        soup = BeautifulSoup(content, "html.parser")
        return soup

    def find_element_from_src(self, src, soup): #not sure why I pass 'self' here but apparently I have to
        relativeSrc = src.split("/")[-1]
        regex = "%s$"%relativeSrc#[-15:] #if the string is too long it's possible there might be errors (i don't know if there might be errors)     ':' denotes a range I think
        print("REGEX:    ", regex)
        matchingElements = soup.find_all(attrs={"src": re.compile(r'%s'%regex)})
        contextElement = matchingElements[0]

        #print(contextElement)
        return contextElement

    def get_element_hierarchy_from_src(self, src, soup):
        context = self.find_element_from_src(src, soup)

        parent = context.parent
        grandparent = parent.parent

        #print("parent  :", parent, " \n grandparent:  ", grandparent)
        return parent, grandparent

    def get_context_links(self, element):
        anchors = element.find_all("a")
        hrefs = [a.get("href") for a in anchors]
        print("HREFS =====: ",hrefs)
        return hrefs

