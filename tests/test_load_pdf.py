import pytest
from data_operations import load_pdf
import time


def test_load_pdf_to_text():
    fpath = "/home/thusitha/work/bigdata/annual_reports/docs/LOLC.N0000/Annual_Report_2018-2019.pdf"
    tic = time.perf_counter()
    pages = load_pdf.load_pdf_to_text(fpath)
    toc = time.perf_counter()
    print(f"parsed the pdf in {toc - tic:0.4f} seconds")
    assert pages is not None


def test_load_metadata():
    file_meta = load_pdf.load_pdf_metadata()
    assert len(file_meta) > 0


def test_create_doc():
    file_meta = load_pdf.load_pdf_metadata()
    file1 = file_meta[1]
    load_pdf.create_and_upload_document(file1)
