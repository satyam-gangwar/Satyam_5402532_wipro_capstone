from __future__ import annotations

import allure
import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage, LoginSessionExpiredError
from tests.base_test import BaseTest
from utilities.logger import get_logger
from utilities.screenshot_utils import capture_screenshot


logger = get_logger("e2e")


@allure.epic("99acres")
@allure.feature("Login Flow")
@pytest.mark.e2e
class Test99AcresE2E(BaseTest):

    @pytest.mark.parametrize(
        "login_key",
        [
            "login"
        ]
    )
    @allure.title("Login with OTP")
    def test_login_flow(
        self,
        base_url: str,
        test_data: dict,
        login_key: str
    ) -> None:

        login_data = test_data[login_key]

        mobile_number = (
            login_data.get("mobile_number")
            or login_data.get("username")
        )

        otp_pause_seconds = int(
            login_data.get("otp_pause_seconds", 60)
        )

        before_mobile_entry_pause_seconds = int(
            login_data.get(
                "before_mobile_entry_pause_seconds",
                0
            )
        )

        after_mobile_entry_pause_seconds = int(
            login_data.get(
                "after_mobile_entry_pause_seconds",
                0
            )
        )

        if not mobile_number:
            pytest.skip("Login credentials missing")

        home_page = HomePage(self.driver)
        login_page = LoginPage(self.driver)

        with allure.step("Open home page"):
            home_page.open(base_url)
            home_page.wait_for_page_load()

            self._capture_step("01_home")

            logger.info("Homepage opened successfully")

        with allure.step("Login with OTP"):
            home_page.open_login()

            self._capture_step("02_login_popup")

            assert login_page.is_login_dialog_displayed(), (
                "Login dialog not visible"
            )

            logger.info("Login popup opened successfully")

            self._start_login_with_session_retry(
                home_page,
                login_page,
                base_url,
                mobile_number,
                otp_pause_seconds,
                before_mobile_entry_pause_seconds,
                after_mobile_entry_pause_seconds,
            )

            self._capture_step("03_login_done")

            logger.info("Login process completed")

        with allure.step("Validate login"):
            assert "99acres" in self.driver.title.lower(), (
                "99acres title not found after login"
            )

            self._capture_step("04_login_success")

            logger.info("Login validation completed successfully")

    def _capture_step(self, step_name: str) -> None:

        path = capture_screenshot(
            self.driver,
            f"e2e_{step_name}"
        )

        allure.attach.file(
            path,
            name=step_name,
            attachment_type=allure.attachment_type.PNG
        )

        logger.info(
            "Screenshot captured: %s",
            path
        )

    def _start_login_with_session_retry(
        self,
        home_page,
        login_page,
        base_url: str,
        mobile_number: str,
        otp_pause_seconds: int,
        before_mobile_entry_pause_seconds: int,
        after_mobile_entry_pause_seconds: int,
    ) -> None:

        try:
            login_page.start_mobile_login_and_pause_for_otp(
                mobile_number,
                otp_pause_seconds,
                before_mobile_entry_pause_seconds,
                after_mobile_entry_pause_seconds,
            )

            logger.info("Login process started successfully")

            return

        except LoginSessionExpiredError:
            logger.info("Session expired, retrying login")

        home_page.open(base_url)

        self._capture_step("05_homepage_reopened")

        home_page.open_login()

        self._capture_step("06_login_popup_reopened")

        assert login_page.is_login_dialog_displayed(), (
            "Login dialog not visible after retry"
        )

        login_page.start_mobile_login_and_pause_for_otp(
            mobile_number,
            otp_pause_seconds,
            before_mobile_entry_pause_seconds,
            after_mobile_entry_pause_seconds,
        )

        self._capture_step("07_retry_login_done")

        logger.info("Login retry completed successfully")