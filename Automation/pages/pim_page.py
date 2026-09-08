from selenium.webdriver.common.by import By
from Automation.pages.base_page import BasePage

class PIMPage(BasePage):
    """Page Object for OrangeHRM PIM Navigation and Module."""
    
    # Locators
    PIM_MENU_LINK = (By.XPATH, "//span[text()='PIM']/ancestor::a | //a[contains(@href, 'viewPimModule')]")
    TOPBAR_NAV = (By.CSS_SELECTOR, ".oxd-topbar-body-nav")
    ADD_EMPLOYEE_TAB = (By.XPATH, "//a[contains(text(), 'Add Employee')]")
    EMPLOYEE_LIST_TAB = (By.XPATH, "//a[contains(text(), 'Employee List')]")
    PAGE_HEADER = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb-module")
    HAMBURGER_ICON = (By.CSS_SELECTOR, "i.bi-list, .oxd-topbar-header-hamburger")

    def navigate_to_pim(self):
        """
        Navigates to PIM module by moving to (hovering over) PIM side menu
        and clicking it, fulfilling assignment requirements.
        Handles both desktop and responsive/collapsed sidebar gracefully.
        """
        self.logger.info("Navigating to PIM module via ActionChains hover + click")
        
        # If sidebar is collapsed (e.g. responsive viewport), toggle hamburger menu
        if not self.is_displayed(self.PIM_MENU_LINK, timeout=3):
            if self.is_displayed(self.HAMBURGER_ICON, timeout=2):
                self.logger.info("Sidebar collapsed, clicking hamburger menu icon")
                self.click(self.HAMBURGER_ICON)
                
        pim_elem = self.find_element(self.PIM_MENU_LINK, timeout=10)
        
        # Hover over PIM menu item using ActionChains
        from selenium.webdriver.common.action_chains import ActionChains
        actions = ActionChains(self.driver)
        actions.move_to_element(pim_elem).perform()
        
        # Click the PIM menu item
        try:
            pim_elem.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", pim_elem)
            
        self.wait_for_url_contains("/pim/")
        self.find_element(self.TOPBAR_NAV)

    def is_pim_displayed(self) -> bool:
        """Verifies if PIM module is currently active and loaded."""
        url_ok = self.wait_for_url_contains("/pim/")
        topbar_ok = self.is_displayed(self.TOPBAR_NAV)
        return url_ok and topbar_ok

    def click_add_employee_tab(self):
        """Clicks the 'Add Employee' tab in the PIM topbar."""
        self.logger.info("Clicking 'Add Employee' topbar tab")
        self.click(self.ADD_EMPLOYEE_TAB)
        self.wait_for_url_contains("/pim/addEmployee")

    def click_employee_list_tab(self):
        """Clicks the 'Employee List' tab in the PIM topbar."""
        self.logger.info("Clicking 'Employee List' topbar tab")
        self.click(self.EMPLOYEE_LIST_TAB)
        self.wait_for_url_contains("/pim/viewEmployeeList")
