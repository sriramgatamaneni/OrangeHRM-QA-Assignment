import time
from selenium.webdriver.common.by import By
from Automation.pages.base_page import BasePage

class EmployeePage(BasePage):
    """Page Object for OrangeHRM Add Employee and Personal Details Page."""
    
    # Locators
    FIRST_NAME_INPUT = (By.NAME, "firstName")
    MIDDLE_NAME_INPUT = (By.NAME, "middleName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    EMPLOYEE_ID_INPUT = (By.XPATH, "//label[text()='Employee Id']/parent::div/following-sibling::div/input")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    SUCCESS_TOAST = (By.CSS_SELECTOR, ".oxd-toast-content")
    PERSONAL_DETAILS_HEADER = (By.XPATH, "//h6[contains(text(), 'Personal Details')]")
    ADD_EMPLOYEE_HEADING = (By.XPATH, "//h6[contains(text(), 'Add Employee')]")
    FORM_LOADER = (By.CSS_SELECTOR, ".oxd-form-loader")

    def wait_for_form_loader_to_disappear(self, timeout: int = 10) -> bool:
        """Explicitly waits for the OrangeHRM form loader overlay to disappear."""
        return self.wait_for_invisibility(self.FORM_LOADER, timeout=timeout)

    def enter_first_name(self, first_name: str):
        """Enters the employee's first name."""
        self.send_keys(self.FIRST_NAME_INPUT, first_name)

    def enter_middle_name(self, middle_name: str):
        """Enters the employee's middle name."""
        if middle_name:
            self.send_keys(self.MIDDLE_NAME_INPUT, middle_name)

    def enter_last_name(self, last_name: str):
        """Enters the employee's last name."""
        self.send_keys(self.LAST_NAME_INPUT, last_name)

    def enter_employee_id(self, emp_id: str):
        """Enters a unique employee ID."""
        self.send_keys(self.EMPLOYEE_ID_INPUT, emp_id)

    def get_employee_id(self) -> str:
        """Retrieves the auto-populated or entered employee ID."""
        elem = self.find_element(self.EMPLOYEE_ID_INPUT)
        return elem.get_attribute("value")

    def click_save(self):
        """Clicks the Save button on the Add Employee form after ensuring loader is gone."""
        self.logger.info("Waiting for form loader overlay to clear before clicking Save")
        self.wait_for_form_loader_to_disappear()
        self.logger.info("Clicking Save button")
        self.click(self.SAVE_BUTTON)

    def add_employee(self, first_name: str, middle_name: str, last_name: str, emp_id: str = None) -> str:
        """
        Fills the Add Employee form, enters unique ID (or uses auto-generated),
        saves the record, and waits for successful persistence.
        Returns the saved Employee ID.
        """
        self.wait_for_form_loader_to_disappear()
        self.find_element(self.FIRST_NAME_INPUT)
        self.enter_first_name(first_name)
        if middle_name:
            self.enter_middle_name(middle_name)
        self.enter_last_name(last_name)
        
        self.wait_for_form_loader_to_disappear()
        assigned_id = emp_id or self.get_employee_id()
        if emp_id:
            self.enter_employee_id(emp_id)
            
        self.logger.info(f"Submitting employee: {first_name} {middle_name} {last_name} (ID: {assigned_id})")
        self.click_save()
        
        # Wait for success toast or redirection to Personal Details
        self.wait_for_save_success()
        return assigned_id

    def wait_for_save_success(self) -> bool:
        """Waits for save confirmation toast or redirect to Personal Details."""
        toast_present = self.is_displayed(self.SUCCESS_TOAST, timeout=8)
        redirected = self.wait_for_url_contains("/pim/viewPersonalDetails", timeout=10)
        return toast_present or redirected
