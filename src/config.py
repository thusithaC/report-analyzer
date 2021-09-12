import os
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("REPORT-ANALYZER")

REPORTS_FILE_LOCATION = "/home/thusitha/work/bigdata/annual_reports/docs"

MONGODB_HOST_PORT = os.getenv("MONGODB_HOST_PORT", "localhost:27017")
MONGO_DB_NAME = os.getenv("DB_NAME", "annualReports")
CLEANED_DOCS = "cleanedReports"

