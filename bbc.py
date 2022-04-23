from bs4 import BeautifulSoup
import requests
import re
import time

from crawl import crawl_sub_categories, get_headlines


class BBC:
    def __init__(self):
        self.base_url = "https://www.bbc.com/"
        self.home_html = requests.get(self.base_url)
        self.soup = BeautifulSoup(
            self.home_html.text, 'html.parser'
        )
        self.adjacencyList = dict()

    def make_graph(self):
        """
        Crawls_categories from bbc.com
        """
        categories = self.soup.find_all(
            "a", href=re.compile(r"bbc\.com")
        )[2:7]
        self.adjacencyList[self.base_url] = list()
        # finds all anker tags with bbc.com in href
        end_nodes = dict()
        for category in categories:
            category_link = category["href"]
            category_text = category.span.text.lower()
            subcategories = crawl_sub_categories(
                category_link, category_text
            )
            self.adjacencyList[category_link] = subcategories
            self.adjacencyList[self.base_url].append(
                category_link
            )
            for _ in subcategories:
                end_nodes[_] = []
            time.sleep(0.5)
        self.adjacencyList.update(end_nodes)

    def bfs(self):
        visited = dict()
        for key in self.adjacencyList.keys():
            visited[key] = False
        return_map = dict()
        queue = [self.base_url]
        visited[self.base_url] = True
        while queue:
            link = queue.pop(0)
            if len(self.adjacencyList[link]) < 1:
                """Check if the link is the end node. i.e subcategory"""
                headlines = get_headlines(link)
                if headlines:
                    return_map[link] = headlines

            for child in self.adjacencyList.get(link):
                if not visited[child]:
                    queue.append(child)
                    visited[child] = True
        return return_map
