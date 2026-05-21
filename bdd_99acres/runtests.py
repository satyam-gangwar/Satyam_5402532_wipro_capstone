import os
import shutil
from datetime import datetime

from utils.logger import LogGen


logger = LogGen.loggen()

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

logger.info("========================================")
logger.info(
    f"99ACRES BDD AUTOMATION EXECUTION STARTED: {timestamp}"
)

# ========================================
# DELETE OLD ALLURE RESULTS
# ========================================

if os.path.exists("reports/allure-results"):

    logger.info(
        "Deleting old allure-results folder"
    )

    shutil.rmtree(
        "reports/allure-results"
    )

# ========================================
# DELETE OLD ALLURE REPORT
# ========================================

if os.path.exists("reports/allure-report"):

    logger.info(
        "Deleting old allure-report folder"
    )

    shutil.rmtree(
        "reports/allure-report"
    )

# ========================================
# START BEHAVE EXECUTION
# ========================================

logger.info(
    "Starting Behave test execution for 99acres"
)

behave_status = os.system(
    "behave"
)

logger.info(
    f"Behave execution completed "
    f"with status code: {behave_status}"
)

# ========================================
# GENERATE ALLURE REPORT
# ========================================

logger.info(
    "Generating Allure HTML report"
)

allure_generate_status = os.system(
    "allure generate reports/allure-results "
    "-o reports/allure-report --clean"
)

logger.info(
    f"Allure report generated "
    f"with status code: {allure_generate_status}"
)

# ========================================
# EXECUTION COMPLETED
# ========================================

logger.info(
    "99ACRES BDD AUTOMATION EXECUTION COMPLETED"
)

logger.info("========================================")