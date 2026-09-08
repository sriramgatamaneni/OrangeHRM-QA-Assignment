import time
from typing import Optional, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from Automation.pages.base_page import BasePage

class EmployeeListPage(BasePage):
    """Page Object for OrangeHRM Employee List and Search Functionality."""
    
    # Locators
    EMPLOYEE_LIST_TAB = (By.XPATH, "//a[contains(text(), 'Employee List')]")
    EMPLOYEE_NAME_INPUT = (By.XPATH, "//label[text()='Employee Name']/parent::div/following-sibling::div//input")
    EMPLOYEE_ID_INPUT = (By.XPATH, "//label[text()='Employee Id']/parent::div/following-sibling::div//input")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    RESET_BUTTON = (By.CSS_SELECTOR, "button[type='reset']")
    TABLE_CARDS = (By.CSS_SELECTOR, ".oxd-table-card")
    LOADING_SPINNER = (By.CSS_SELECTOR, ".oxd-loading-spinner")
    FORM_LOADER = (By.CSS_SELECTOR, ".oxd-form-loader")
    NO_RECORDS_BANNER = (By.XPATH, "//*[contains(text(), 'No Records Found')]")
    AUTOCOMPLETE_OPTION = (By.CSS_SELECTOR, ".oxd-autocomplete-option")

    def navigate_to_employee_list(self):
        """Navigates to the Employee List tab and waits for search container to load."""
        self.logger.info("Navigating to Employee List tab")
        self.click(self.EMPLOYEE_LIST_TAB)
        self.wait_for_url_contains("/pim/viewEmployeeList")
        self.find_element(self.SEARCH_BUTTON)
        self.wait_for_table_loaded()

    def wait_for_table_loaded(self):
        """Waits for loading spinner and form loader overlay to disappear."""
        self.wait_for_invisibility(self.LOADING_SPINNER, timeout=10)
        self.wait_for_invisibility(self.FORM_LOADER, timeout=10)

    def reset_search_filters(self):
        """Clicks the Reset button to clear all search fields."""
        self.logger.info("Resetting search filters")
        self.click(self.RESET_BUTTON)
        self.wait_for_table_loaded()

    def search_by_employee_id(self, emp_id: str):
        """Enters an employee ID in search filters and clicks Search."""
        self.logger.info(f"Filtering Employee List by Employee ID: {emp_id}")
        self.reset_search_filters()
        self.send_keys(self.EMPLOYEE_ID_INPUT, emp_id)
        self.click(self.SEARCH_BUTTON)
        self.wait_for_table_loaded()

    def search_by_employee_name(self, name: str):
        """Enters employee name into the search field and submits search."""
        self.logger.info(f"Filtering Employee List by Employee Name: {name}")
        self.reset_search_filters()
        self.send_keys(self.EMPLOYEE_NAME_INPUT, name)
        # In case autocomplete dropdown appears, give it a moment
        time.sleep(0.5)
        self.click(self.SEARCH_BUTTON)
        self.wait_for_table_loaded()

    def locate_and_verify_employee(self, first_name: str, middle_name: str, last_name: str, emp_id: str = None) -> bool:
        """
        Locates the employee in the Employee List table, scrolls to the row,
        verifies the full name, prints '<Full Name> - Name Verified', and returns verification status.
        """
        full_name = f"{first_name} {middle_name} {last_name}".strip()
        expected_first_middle = f"{first_name} {middle_name}".strip()
        
        # Prefer exact search by unique employee ID if provided, otherwise search by name
        if emp_id:
            self.search_by_employee_id(emp_id)
        else:
            self.search_by_employee_name(first_name)
            
        rows = self.find_elements(self.TABLE_CARDS, timeout=8)
        
        for row in rows:
            row_text = row.text
            # OrangeHRM displays First (& Middle) in one column, and Last Name in the next column
            if (expected_first_middle in row_text or first_name in row_text) and last_name in row_text:
                self.scroll_to_element(row)
                output_message = f"{full_name} - Name Verified"
                print(output_message)
                self.logger.info(f"VERIFIED: {output_message}")
                return True
                
        self.logger.warning(f"Employee '{full_name}' (ID: {emp_id}) was NOT found in the table.")
        return False
