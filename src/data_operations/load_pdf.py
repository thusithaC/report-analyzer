from config import logger, REPORTS_FILE_LOCATION, MONGO_DB_NAME, MONGODB_HOST_PORT, CLEANED_DOCS
from utils.mongo_helper import MongoHelper
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import re
import os
from typing import List, Dict

def clean_text(text: str):
    text = re.sub(r'[^\w\s]|\n', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.lower().strip()


def load_pdf_to_text(file_loc: str, clean: bool=True):
    pages = {}
    for i, page_layout in enumerate(extract_pages(file_loc)):
        text_elements = []
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                text = element.get_text()
                if clean:
                    text = clean_text(text)
                text_elements.append(text)
        pages[str(i)] = text_elements
    return pages


def upload_doc(doc: dict):
    db = MongoHelper(host=MONGODB_HOST_PORT, db_name=MONGO_DB_NAME)
    ret = db.insert(CLEANED_DOCS, doc)
    logger.info(f"inserted document {ret}")
    db.close()


def create_and_upload_document(meta_data: dict):
    file_loc = meta_data.get("full_path")
    logger.info(f"Loading file {file_loc}")
    try:
        text_data = load_pdf_to_text(file_loc)
        doc = {"text": text_data}
        doc.update(meta_data)
        logger.info(f"uploading file data")
        upload_doc(doc)
    except Exception as e:
        logger.error(f"Error occurred processing document {file_loc}. Document will be ignored")


def load_pdf_metadata() -> List[Dict]:
    all_dirs = os.listdir(REPORTS_FILE_LOCATION)
    all_files = []

    for loc in all_dirs:
        files = [x for x in os.listdir(os.path.join(REPORTS_FILE_LOCATION, loc)) if str(x).endswith(".pdf")]
        for file in files:

            full_path = os.path.join(REPORTS_FILE_LOCATION, loc, file)
            res = re.search(r'.*(20\d\d).?(20\d\d).*|.*(20\d\d).?(\d\d).*|.*(20\d\d).*', file)
            year_pattens = [x for x in res.groups() if x is not None]
            year_pattens = sorted(map(lambda x: int(f"20{x}") if len(x) == 2 else int(x), year_pattens))
            file_meta = {
                "full_path":  full_path,
                "company": loc,
                "years": year_pattens
            }
            all_files.append(file_meta)

    return all_files



