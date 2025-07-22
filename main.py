"""Bookmark Checker Script"""

import csv
import logging
import os
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

# Path to bookmarks file - look in script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
BOOKMARKS_FILE = os.path.join(script_dir, 'Bookmarks.html')

# Check if bookmarks file exists
if not os.path.exists(BOOKMARKS_FILE):
    print(f"Error: Bookmarks.html not found in {script_dir}")
    print("Please place your Bookmarks.html file in the same directory "
          "as this script.")
    exit(1)

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
    link_status = 'Dead'
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        if response.history:
            link_status = 'Redirected'
        elif response.status_code in (401, 403):
            link_status = 'Login Required'
        elif (response.status_code == 404 or
              'page not found' in response.text.lower()):
            link_status = 'Dead'
        else:
            link_status = 'Alive'
    except SSLError as ssl_error:
        link_status = 'SSL Error'
        logging.error("SSL error on %s: %s", url, ssl_error)
    except (requests.exceptions.RequestException,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError) as exc:
        logging.error("Error checking %s: %s", url, exc)
    results.append([name, url, link_status])
    logging.info("Checked: %s (%s) - %s", name, url, link_status)

# Write CSV
csv_filename = 'bookmark_check_results.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Bookmark Name', 'URL', 'Status'])
    writer.writerows(results)

logging.info("Bookmark check completed")
print("Done. Results saved to bookmark_check_results.csv and log to "
      "bookmark_check.log.")
