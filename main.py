import json
from bbc import BBC

if __name__ == "__main__":
    bbc = BBC()
    bbc.crawl_categories()
    # print(json.dumps(bbc.adjacencyList, indent=2))
    headlines = bbc.bfs()
    print(json.dumps(headlines, indent=2))
