import random
import time
from typing import List, Dict

class TestData:
    """Central repository for test data and environment configurations."""
    
    BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    
    # Valid Credentials
    VALID_USERNAME = "Admin"
    VALID_PASSWORD = "admin123"
    
    # Invalid Test Data
    INVALID_USERNAME = "InvalidUser"
    INVALID_PASSWORD = "wrongPassword123"
    
    # Expected Messages
    ALERT_INVALID_CREDENTIALS = "Invalid credentials"
    VALIDATION_REQUIRED = "Required"
    DASHBOARD_HEADER_TEXT = "Dashboard"
    
    @staticmethod
    def generate_employee_id() -> str:
        """Generates a unique 6-digit employee ID to prevent duplicate ID collisions."""
        return str(random.randint(100000, 999999))
    
    @classmethod
    def get_employees(cls) -> List[Dict[str, str]]:
        """
        Returns the list of 4 unique employees requested in the assignment.
        Each employee has a unique Employee ID to guarantee successful saving.
        """
        base_employees = [
            {
                "first_name": "John",
                "middle_name": "Test",
                "last_name": "One",
                "emp_id": cls.generate_employee_id()
            },
            {
                "first_name": "David",
                "middle_name": "Test",
                "last_name": "Two",
                "emp_id": cls.generate_employee_id()
            },
            {
                "first_name": "Robert",
                "middle_name": "Test",
                "last_name": "Three",
                "emp_id": cls.generate_employee_id()
            },
            {
                "first_name": "Michael",
                "middle_name": "Test",
                "last_name": "Four",
                "emp_id": cls.generate_employee_id()
            }
        ]
        return base_employees
