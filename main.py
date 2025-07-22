
import csv
import logging
import requests
from requests.exceptions import SSLError
from bs4 import BeautifulSoup
from tqdm import tqdm

# Setup logging
logging.basicConfig(filename='bookmark_check.log', level=logging.INFO, format='%(asctime)s %(message)s')
logging.info("Starting bookmark check")

# Path to bookmarks file
bookmarks_file = input("Enter path to Bookmarks.html: ").strip()

# Parse HTML bookmarks file
with open(bookmarks_file, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

links = []
for a in soup.find_all('a'):
    links.append({'name': a.text.strip(), 'url': a['href'].strip()})

# Check links
results = []
for link in tqdm(links, desc='Checking bookmarks', ncols=100):
    name, url = link['name'], link['url']
    status = 'Dead'
    try:
        resp = requests.get(url, timeout=10, allow_redirects=True)
        if resp.history:
            status = 'Redirected'
        elif resp.status_code in (401, 403):
            status = 'Login Required'
        elif resp.status_code == 404 or 'page not found' in resp.text.lower():
            status = 'Dead'
        else:
            status = 'Alive'
    except SSLError as e:
        status = 'SSL Error'
        logging.error(f"SSL error on {url}: {e}")
    except Exception as e:
        logging.error(f"Error checking {url}: {e}")
    results.append([name, url, status])
    logging.info(f"Checked: {name} ({url}) - {status}")

# Write CSV
with open('bookmark_check_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Bookmark Name', 'URL', 'Status'])
    writer.writerows(results)

logging.info("Bookmark check completed")
print("Done. Results saved to bookmark_check_results.csv and log to bookmark_check.log.")
