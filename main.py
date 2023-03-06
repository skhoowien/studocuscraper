import requests
from bs4 import BeautifulSoup
import csv
import os

url = 'https://www.studocu.com/en-us/search/ithaca%20college?category=3&institutionId=398'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

links = soup.find_all('a','h3', {'class': '_23f9be87023f'})

if not os.path.exists('output.csv'):
    with open('output.csv', mode='w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Link', 'Title', 'Content'])  # Add header row if file is empty

with open('output.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    for link in links:
        href = link['href']
        title = link.find('h3', {'class': '_23ef9b87023f'}).get_text().strip()
        link_response = requests.get(href)
        link_soup = BeautifulSoup(link_response.content, 'html.parser')
        page_content = link_soup.find('div', {'class': 'page-content'})
        if page_content is not None:
            content = page_content.get_text().strip()
        else:
            content = 'N/A'
        writer.writerow([href, title, content])
        print(f"Scraped data from link {href} has been saved to output.csv")
