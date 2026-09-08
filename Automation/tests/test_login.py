import pytest
from Automation.pages.login_page import LoginPage
from Automation.pages.dashboard_page import DashboardPage
from Automation.utils.test_data import TestData
from Automation.utils.logger import get_logger

logger = get_logger("TestLogin")

class TestLogin:
    """Test suite covering all login functionality scenarios."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Precondition: Navigate to the OrangeHRM login page before each test."""
        self.driver = driver
        self.driver.get(TestData.BASE_URL)
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        logger.info(f"Navigated to: {TestData.BASE_URL}")

    def test_valid_login(self):
        """TC_LOGIN_001: Verify login with valid credentials redirects to Dashboard."""
        logger.info("Executing test_valid_login...")
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        
        # Verify dashboard loaded
        assert self.dashboard_page.is_dashboard_displayed(), (
            "Dashboard should be displayed after valid login"
        )
        assert self.dashboard_page.get_header_title() == TestData.DASHBOARD_HEADER_TEXT, (
            f"Expected header '{TestData.DASHBOARD_HEADER_TEXT}', got '{self.dashboard_page.get_header_title()}'"
        )

    def test_invalid_username(self):
        """TC_LOGIN_002: Verify login with invalid username displays error alert."""
        logger.info("Executing test_invalid_username...")
        self.login_page.login(TestData.INVALID_USERNAME, TestData.VALID_PASSWORD)
        
        error_msg = self.login_page.get_error_message()
        assert error_msg == TestData.ALERT_INVALID_CREDENTIALS, (
            f"Expected '{TestData.ALERT_INVALID_CREDENTIALS}', got '{error_msg}'"
        )
        assert self.login_page.is_login_page_displayed(), "User should remain on login page"

    def test_invalid_password(self):
        """TC_LOGIN_003: Verify login with invalid password displays error alert."""
        logger.info("Executing test_invalid_password...")
        self.login_page.login(TestData.VALID_USERNAME, TestData.INVALID_PASSWORD)
        
        error_msg = self.login_page.get_error_message()
        assert error_msg == TestData.ALERT_INVALID_CREDENTIALS, (
            f"Expected '{TestData.ALERT_INVALID_CREDENTIALS}', got '{error_msg}'"
        )
        assert self.login_page.is_login_page_displayed(), "User should remain on login page"

    def test_empty_username(self):
        """TC_LOGIN_005: Verify validation when username is omitted."""
        logger.info("Executing test_empty_username...")
        self.login_page.enter_password(TestData.VALID_PASSWORD)
        self.login_page.click_login()
        
        err = self.login_page.get_username_error()
        assert err == TestData.VALIDATION_REQUIRED, (
            f"Expected username validation '{TestData.VALIDATION_REQUIRED}', got '{err}'"
        )

    def test_empty_password(self):
        """TC_LOGIN_006: Verify validation when password is omitted."""
        logger.info("Executing test_empty_password...")
        self.login_page.enter_username(TestData.VALID_USERNAME)
        self.login_page.click_login()
        
        err = self.login_page.get_password_error()
        assert err == TestData.VALIDATION_REQUIRED, (
            f"Expected password validation '{TestData.VALIDATION_REQUIRED}', got '{err}'"
        )

    def test_both_fields_empty(self):
        """TC_LOGIN_007: Verify validation when both credentials fields are empty."""
        logger.info("Executing test_both_fields_empty...")
        self.login_page.click_login()
        
        validation_msgs = self.login_page.get_all_validation_messages()
        assert len(validation_msgs) == 2, f"Expected 2 validation messages, got {len(validation_msgs)}"
        for msg in validation_msgs:
            assert msg == TestData.VALIDATION_REQUIRED, (
                f"Expected validation '{TestData.VALIDATION_REQUIRED}', got '{msg}'"
            )
