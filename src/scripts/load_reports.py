from data_operations import load_pdf
from multiprocessing import Pool
from config import logger

PROCESSES = 12

if __name__ == "__main__":
    logger.info("starting loading files")
    file_meta = load_pdf.load_pdf_metadata()
    with Pool(PROCESSES) as p:
        p.map(load_pdf.create_and_upload_document, file_meta)






