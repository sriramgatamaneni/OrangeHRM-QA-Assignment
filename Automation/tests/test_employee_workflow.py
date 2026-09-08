import pytest
from Automation.pages.login_page import LoginPage
from Automation.pages.dashboard_page import DashboardPage
from Automation.pages.pim_page import PIMPage
from Automation.pages.employee_page import EmployeePage
from Automation.pages.employee_list_page import EmployeeListPage
from Automation.utils.test_data import TestData
from Automation.utils.logger import get_logger

logger = get_logger("TestEmployeeWorkflow")

class TestEmployeeWorkflow:
    """
    End-to-End Automated Workflow:
    1. Login to OrangeHRM
    2. Navigate to PIM module via hover and click
    3. Add 4 unique employees
    4. Verify each employee in the Employee List (scroll, print 'Name Verified', assert)
    5. Logout and verify return to Login page
    """

    def test_complete_employee_workflow(self, driver):
        logger.info("========== Starting OrangeHRM Complete Employee Workflow ==========")
        
        # 1. Initialize Page Objects
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        pim_page = PIMPage(driver)
        employee_page = EmployeePage(driver)
        employee_list_page = EmployeeListPage(driver)

        # 2. Login Flow
        logger.info("Step 1: Navigating to Login Page and Authenticating")
        driver.get(TestData.BASE_URL)
        assert login_page.is_login_page_displayed(), "Login page should be displayed"
        login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)

        # Verify Dashboard
        logger.info("Step 2: Verifying Dashboard after login")
        assert dashboard_page.is_dashboard_displayed(), "Dashboard was not displayed after login"
        logger.info(f"Dashboard verified: {dashboard_page.get_header_title()}")

        # 3. PIM Navigation (hover and click)
        logger.info("Step 3: Navigating to PIM module via hover and click")
        pim_page.navigate_to_pim()
        assert pim_page.is_pim_displayed(), "PIM module was not displayed after navigation"

        # 4. Add 4 Unique Employees
        employees_to_add = TestData.get_employees()
        logger.info(f"Step 4: Adding {len(employees_to_add)} unique employees")
        
        created_records = []
        for emp in employees_to_add:
            logger.info(f"Adding Employee: {emp['first_name']} {emp['middle_name']} {emp['last_name']}")
            pim_page.click_add_employee_tab()
            
            saved_id = employee_page.add_employee(
                first_name=emp["first_name"],
                middle_name=emp["middle_name"],
                last_name=emp["last_name"],
                emp_id=emp["emp_id"]
            )
            
            emp["saved_id"] = saved_id
            created_records.append(emp)
            logger.info(f"Saved Employee: {emp['first_name']} {emp['last_name']} with ID: {saved_id}")

        # 5. Navigate to Employee List and Verify Each Employee
        logger.info("Step 5: Navigating to Employee List for verification")
        pim_page.click_employee_list_tab()
        
        verification_results = []
        for emp in created_records:
            full_name = f"{emp['first_name']} {emp['middle_name']} {emp['last_name']}"
            logger.info(f"Locating and verifying employee: {full_name} (ID: {emp['saved_id']})")
            
            is_found = employee_list_page.locate_and_verify_employee(
                first_name=emp["first_name"],
                middle_name=emp["middle_name"],
                last_name=emp["last_name"],
                emp_id=emp["saved_id"]
            )
            
            # Strict Assertion: The test MUST fail if employee is not found
            assert is_found, (
                f"Assertion Failed: Employee '{full_name}' with ID '{emp['saved_id']}' "
                f"was NOT found in the Employee List."
            )
            verification_results.append(full_name)

        logger.info(f"All {len(verification_results)} employees successfully verified!")

        # 6. Logout from Dashboard/Header
        logger.info("Step 6: Logging out from the application")
        dashboard_page.logout()

        # 7. Assert return to Login page
        logger.info("Step 7: Verifying return to Login page")
        assert login_page.is_login_page_displayed(), "User should be redirected to Login page after logout"
        assert driver.current_url.endswith("/auth/login") or "/auth/login" in driver.current_url, (
            f"Expected URL to contain '/auth/login', got '{driver.current_url}'"
        )
        logger.info("========== OrangeHRM Employee Workflow Completed Successfully! ==========")
