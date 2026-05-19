import pytest
import allure

from pages.home_page import HomePage


@allure.feature("Commercial Module")
class TestCommercial:

    @pytest.mark.commercial
    def test_commercial_flow(self, base_url, test_data):

        location = test_data["property_search"]["commercial_location"]

        home = HomePage(self.driver)

        # OPEN SITE
        home.open(base_url)
        home.wait_for_page_load()

        # OPEN COMMERCIAL TAB
        commercial = home.open_commercial_tab()

        # SEARCH
        commercial.search_commercial_property(location)

        # FILTER
        commercial.apply_basic_filters()

        # VALIDATE
        assert commercial.is_results_loaded()
        assert commercial.results_contain_location(location)