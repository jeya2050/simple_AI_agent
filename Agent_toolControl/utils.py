from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup


def search_duckduckgo(query, max_results=5):
    ddgs = DDGS()
    results = ddgs.text(query, max_results=max_results)
    return [urls['href'] for urls in results]


def scrab_Data(urls):
    data=[]
    for url in urls:
        headers = {'User-Agent': 'Mozilla/5.0'}  # Helps prevent blocking by some servers
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()
            text = ' '.join(text.split()) 
            data.append({f'site:{url},extract_data:{text}'})
            # print(data)

        else:
            pass
            print(f"Failed to retrieve {url}")
    return data




if __name__=="__main__":
    query="age of python?"
    urls=search_duckduckgo(query, max_results=5)
    print(urls)


    scrab_Data=scrab_Data(urls)


