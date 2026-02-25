# ingestion/ingest.py
#Establishes URL where document lives, and destination. Opens and writes.

import os
import requests
from config import PDF_URL, PDF_PATH

PDF_URL = PDF_URL
RAW_DATA_PATH = PDF_PATH


def fetch_pdf():
    os.makedirs("data/raw", exist_ok=True)

    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/pdf",
        "Referer": "https://www.omnipod.com/"
    }

    response = session.get(PDF_URL, headers=headers)

    print("Status:", response.status_code)

    if response.status_code != 200:
        raise Exception(f"Failed to download PDF (status {response.status_code})")

    with open(RAW_DATA_PATH, "wb") as f:
        f.write(response.content)

    print("PDF downloaded successfully.")


if __name__ == "__main__":
    fetch_pdf()