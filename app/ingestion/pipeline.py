from load_urls import load_urls
from scraper import scrape_url
from chunking import chunk_text
from embeddings import store_chunks
from markdown_store import save_markdown

def run_pipeline():
    urls = load_urls()

    for url in urls:
        print(f"\nProcessing: {url}")

        text = scrape_url(url)
        if not text:
            continue

        save_markdown(url, text)
        chunks = chunk_text(text)
        store_chunks(url, chunks)

if __name__ == "__main__":
    run_pipeline()