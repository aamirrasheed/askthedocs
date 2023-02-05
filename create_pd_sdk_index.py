from gpt_index import GPTSimpleVectorIndex, TrafilaturaWebReader
import os
from bs4 import BeautifulSoup
import requests

# use beautiful soup to scrape all of the links from the parallel domain website

def get_links_from_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('a')
    links = [link.get('href') for link in links]

    # add base url to relative links
    for link in links:
      if not link.startswith('http'):
        links[links.index(link)] = url + link
    
    # remove anchors from links
    for link in links:
      if '#' in link:
        links[links.index(link)] = link.split('#')[0]
    
    # remove duplicate links
    links = list(dict.fromkeys(links))

    # remove links to other websites
    links = [link for link in links if url in link]
      
    return links

# then use trafilatura to scrape the text from each link
# then use gpt_index to create an index of the scraped text
links = get_links_from_url("https://parallel-domain.github.io/pd-sdk/")

documents = TrafilaturaWebReader().load_data(links)

index = GPTSimpleVectorIndex(documents)

index.save_to_disk('pd-sdk-index.json')