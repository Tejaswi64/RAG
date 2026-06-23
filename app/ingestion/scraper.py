import requests
from bs4 import BeautifulSoup
import urllib3

# Disable SSL warnings for corporate proxy
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_url(url):
    try:
        response = requests.get(url, timeout=10, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")

        # remove scripts/styles
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator=" ")
        clean_text = " ".join(text.split())

        return clean_text

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""