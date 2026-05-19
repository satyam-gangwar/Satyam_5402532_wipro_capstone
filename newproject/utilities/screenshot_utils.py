from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

import allure
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import settings


def _safe_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", value).strip("_")


def capture_screenshot(driver: WebDriver, test_name: str) -> Path:
    settings.screenshot_dir.mkdir(parents=True, exist_ok=True)
    file_path = settings.screenshot_dir / f"{_safe_name(test_name)}_{datetime.now():%Y%m%d_%H%M%S}.png"
    driver.save_screenshot(str(file_path))
    with open(file_path, "rb") as image_file:
        allure.attach(
            image_file.read(),
            name=file_path.name,
            attachment_type=allure.attachment_type.PNG,
        )
    return file_path
