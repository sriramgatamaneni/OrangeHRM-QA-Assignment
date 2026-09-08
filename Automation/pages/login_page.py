from typing import List
from selenium.webdriver.common.by import By
from Automation.pages.base_page import BasePage

class LoginPage(BasePage):
    """Page Object for OrangeHRM Login Page."""
    
    # Locators
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_ALERT_TEXT = (By.CSS_SELECTOR, ".oxd-alert-content-text")
    USERNAME_REQUIRED_MSG = (By.XPATH, "//input[@name='username']/ancestor::div[contains(@class,'oxd-input-group')]//span[contains(@class,'oxd-input-group__message')]")
    PASSWORD_REQUIRED_MSG = (By.XPATH, "//input[@name='password']/ancestor::div[contains(@class,'oxd-input-group')]//span[contains(@class,'oxd-input-group__message')]")
    ALL_VALIDATION_MSGS = (By.CSS_SELECTOR, ".oxd-input-group__message")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, ".orangehrm-login-forgot-header")
    LOGIN_CONTAINER = (By.CSS_SELECTOR, ".orangehrm-login-layout")

    def enter_username(self, username: str):
        """Enters text into the username input field."""
        self.logger.info(f"Entering username: {username}")
        self.send_keys(self.USERNAME_INPUT, username)

    def enter_password(self, password: str):
        """Enters text into the password input field."""
        self.logger.info("Entering password: [PROTECTED]")
        self.send_keys(self.PASSWORD_INPUT, password)

    def click_login(self):
        """Clicks the Login submission button."""
        self.logger.info("Clicking Login button")
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str):
        """Convenience method to execute full login sequence."""
        if username:
            self.enter_username(username)
        if password:
            self.enter_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        """Retrieves text from the invalid credentials alert banner."""
        return self.get_text(self.ERROR_ALERT_TEXT)

    def get_username_error(self) -> str:
        """Retrieves inline validation error text for username field."""
        return self.get_text(self.USERNAME_REQUIRED_MSG)

    def get_password_error(self) -> str:
        """Retrieves inline validation error text for password field."""
        return self.get_text(self.PASSWORD_REQUIRED_MSG)

    def get_all_validation_messages(self) -> List[str]:
        """Retrieves text of all visible inline field validation messages."""
        elements = self.find_elements(self.ALL_VALIDATION_MSGS)
        return [el.text.strip() for el in elements if el.text.strip()]

    def is_login_page_displayed(self) -> bool:
        """Checks if login form and inputs are visible."""
        return self.is_displayed(self.LOGIN_CONTAINER) and self.is_displayed(self.LOGIN_BUTTON) and self.is_displayed(self.USERNAME_INPUT)

    def click_forgot_password(self):
        """Clicks the 'Forgot your password?' link."""
        self.click(self.FORGOT_PASSWORD_LINK)
