"""Bookmark Checker Script"""

import csv
import logging
import requests
from requests.exceptions import SSLError
from bs4 import BeautifulSoup
from tqdm import tqdm

# Setup logging
logging.basicConfig(
    filename='bookmark_check.log',
    level=logging.INFO,
    format='%(asctime)s %(message)s'
)
logging.info("Starting bookmark check")

# Path to bookmarks file
BOOKMARKS_FILE = input("Enter path to Bookmarks.html: ").strip()

# Parse HTML bookmarks file
with open(BOOKMARKS_FILE, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

links = [
    {'name': a_tag.text.strip(), 'url': a_tag['href'].strip()}
    for a_tag in soup.find_all('a')
]

# Check links
results = []
for link in tqdm(links, desc='Checking bookmarks', ncols=100):
    name = link['name']
    url = link['url']
    status = 'Dead'
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        if response.history:
            status = 'Redirected'
        elif response.status_code in (401, 403):
            status = 'Login Required'
        elif response.status_code == 404 or 'page not found' in response.text.lower():
            status = 'Dead'
        else:
            status = 'Alive'
    except SSLError as ssl_error:
        status = 'SSL Error'
        logging.error("SSL error on %s: %s", url, ssl_error)
    except Exception as exc:
        logging.error("Error checking %s: %s", url, exc)
    results.append([name, url, status])
    logging.info("Checked: %s (%s) - %s", name, url, status)

# Write CSV
with open('bookmark_check_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Bookmark Name', 'URL', 'Status'])
    writer.writerows(results)

logging.info("Bookmark check completed")
print("Done. Results saved to bookmark_check_results.csv and log to bookmark_check.log.")