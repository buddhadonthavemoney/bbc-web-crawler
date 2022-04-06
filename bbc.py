from bs4 import BeautifulSoup
import requests
import re
import time

from crawl import crawl_sub_categories, get_headlines


class BBC:
    def __init__(self):
        self.base_url = "https://www.bbc.com/"
        self.adjacencyList = dict()
        # adjacencyList is a graph represented using a list
        self.home_html = requests.get(self.base_url)
        self.soup = BeautifulSoup(
            self.home_html.text, 'html.parser'
        )

    def crawl_categories(self):
        """
        Crawls_categories from bbc.com
        """
        categories = self.soup.find_all(
            "a", href=re.compile(r"bbc\.com")
        )[2:6]
        self.adjacencyList[self.base_url] = list()
        # finds all anger tags with bbc.com in href
        end_nodes = dict()
        # enn_nodes is used to add the subcategories as a node in adacencyList
        for category in categories:
            category_link = category["href"]
            category_text = category.span.text.lower()
            subcategories = crawl_sub_categories(
                category_link, category_text
            )
            self.adjacencyList[category_link] = subcategories
            """ here the list of categories is appended to base url base url the 1st node
            and the subcategories its neigbours
            """

            self.adjacencyList[self.base_url].append(
                category_link
            )
            for _ in subcategories:
                end_nodes[_] = []
            time.sleep(0.5)
        self.adjacencyList.update(end_nodes)

    def bfs(self):
        visited = set()
        return_map = dict()
        queue = [self.base_url]
        visited.add(self.base_url)
        while queue:
            link = queue.pop(0)
            if len(self.adjacencyList[link]) < 1:
                """Check if the link is the end node. i.e subcategory"""
                headlines = get_headlines(link)
                if headlines:
                    return_map[link] = headlines

            for child in self.adjacencyList.get(link):
                queue.append(child)
                if child not in visited:
                    visited.add(child)
                    queue.append(child)
        return return_map
