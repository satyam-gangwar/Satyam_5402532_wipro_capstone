import os
import shutil
from datetime import datetime

from utils.logger import LogGen
logger = LogGen.loggen()


timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)
logger.info("========================================")
logger.info("99Acres AUTOMATION EXECUTION STARTED")

# Clean Old Allure Results
if os.path.exists("reports/allure-results"):
    logger.info(
        "Deleting old allure-results folder"
    )
    shutil.rmtree("reports/allure-results")


# Clean Old Allure Report
if os.path.exists("reports/allure-report"):
    logger.info(
        "Deleting old allure-report folder"
    )
    shutil.rmtree("reports/allure-report")


# Execute Behave Tests
logger.info("Starting Behave Test Execution")
behave_status = os.system("behave")
logger.info(
    f"Behave Execution Completed "
    f"with status code : {behave_status}"
)


# Generate Allure HTML Report
logger.info("Generating Allure HTML Report")
allure_generate_status = os.system(
    "allure generate reports/allure-results "
    "-o reports/allure-report --clean"
)
logger.info(
    f"Allure Report Generated "
    f"with status code : "
    f"{allure_generate_status}"
)
logger.info("99Acres AUTOMATION EXECUTION COMPLETED")
logger.info("========================================")