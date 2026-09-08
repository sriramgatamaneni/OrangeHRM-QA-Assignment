from selenium.webdriver.common.by import By
from Automation.pages.base_page import BasePage

class DashboardPage(BasePage):
    """Page Object for OrangeHRM Dashboard Page."""
    
    # Locators
    HEADER_TITLE = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb-module")
    USER_DROPDOWN_TAB = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")
    LOGOUT_LINK = (By.XPATH, "//a[text()='Logout'] | //a[contains(@href, '/auth/logout')]")
    SIDEBAR_MENU = (By.CSS_SELECTOR, ".oxd-sidepanel-body")

    def is_dashboard_displayed(self) -> bool:
        """Verifies if the dashboard header and side menu are visible."""
        url_ok = self.wait_for_url_contains("/dashboard/index")
        header_ok = self.is_displayed(self.HEADER_TITLE)
        return url_ok and header_ok

    def get_header_title(self) -> str:
        """Returns the module title displayed in the top bar."""
        return self.get_text(self.HEADER_TITLE)

    def open_user_dropdown(self):
        """Clicks the user profile avatar/name tab to open the dropdown menu."""
        self.logger.info("Opening user profile dropdown")
        self.click(self.USER_DROPDOWN_TAB)

    def click_logout(self):
        """Clicks the Logout item inside the open user dropdown."""
        self.logger.info("Clicking Logout link")
        self.click(self.LOGOUT_LINK)

    def logout(self):
        """Convenience method to execute complete logout sequence."""
        self.open_user_dropdown()
        self.click_logout()
        self.wait_for_url_contains("/auth/login")
