# ingestion/pdf_parser.py
#Reads the file with a PDF reader, structures text pairing page number and content

from pypdf import PdfReader


def parse_pdf(file_path):
    reader = PdfReader(file_path)

    documents = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()

        if text:
            documents.append({
                "text": text,
                "page": i + 1
            })

    return documents