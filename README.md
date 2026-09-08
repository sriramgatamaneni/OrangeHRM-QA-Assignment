# OrangeHRM QA Automation & Manual Testing Project

An enterprise-grade, submission-ready QA testing repository for the OrangeHRM demo application, featuring a comprehensive manual testing suite and an end-to-end automated testing framework built with **Python**, **Selenium WebDriver**, and **PyTest** implementing the **Page Object Model (POM)** architecture.

---

## 🔗 Application Under Test

- **Application URL**: [https://opensource-demo.orangehrmlive.com/web/index.php/auth/login](https://opensource-demo.orangehrmlive.com/web/index.php/auth/login)
- **Application Type**: Single Page Application (SPA) built with Vue.js
- **Default Credentials**:
  - **Username**: `Admin`
  - **Password**: `admin123`

---

## 🛠️ Technologies & Tools

- **Programming Language**: Python 3.13+
- **Browser Automation**: Selenium WebDriver 4.x
- **Test Runner / Framework**: PyTest 8.x
- **Design Pattern**: Page Object Model (POM)
- **Spreadsheet Generation**: openpyxl
- **Supported Browsers**: Google Chrome (configured for Headless and Headed execution)
- **OS Platform**: Windows / Cross-Platform

---

## 📁 Project Structure

```
OrangeHRM-QA-Assignment/
│
├── Manual_Testing/
│   └── OrangeHRM_Test_Cases.xlsx         # Multi-sheet styled Excel workbook
│
├── Automation/
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── base_page.py                  # Core explicit wait & interaction wrapper
│   │   ├── login_page.py                 # Login Page Object
│   │   ├── dashboard_page.py             # Dashboard Page & Logout Object
│   │   ├── pim_page.py                   # PIM Navigation & Sub-tabs Object
│   │   ├── employee_page.py              # Add Employee & Form Submission Object
│   │   └── employee_list_page.py         # Employee List Search & Verification Object
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_login.py                 # Automated Login edge cases suite
│   │   └── test_employee_workflow.py     # End-to-End multi-employee management workflow
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── test_data.py                  # Isolated test data & unique ID generator
│   │   └── logger.py                     # Centralized console & file logger
│   │
│   ├── conftest.py                       # Chrome WebDriver fixtures & failure screenshot hook
│   ├── pytest.ini                        # PyTest configuration for Automation directory
│   └── requirements.txt                  # Python project dependencies
│
├── screenshots/                          # Automatically stores timestamped failure screenshots
├── conftest.py                           # Root proxy conftest for root execution
├── pytest.ini                            # Root proxy pytest.ini for seamless discovery
└── README.md                             # Project documentation & execution guide
```

---

## 📋 Manual Testing Suite

The manual testing artifacts are encapsulated in an enterprise-grade Excel workbook located at:
`Manual_Testing/OrangeHRM_Test_Cases.xlsx`

The workbook contains three styled sheets with fixed headers, custom column widths, word wrapping, and color-coded status badges (`PASS`, `FAIL`, `NOT EXECUTED`):

### 1. Sheet 1: Login Test Cases (14 Scenarios)
Columns: `Test Case ID`, `Module`, `Test Scenario`, `Preconditions`, `Test Steps`, `Test Data`, `Expected Result`, `Actual Result`, `Status`, `Severity`, `Priority`, `Remarks`
- **TC_LOGIN_001**: Valid username + valid password (`Admin` / `admin123`)
- **TC_LOGIN_002**: Invalid username + valid password (`InvalidUser` / `admin123`)
- **TC_LOGIN_003**: Valid username + invalid password (`Admin` / `wrongPassword123`)
- **TC_LOGIN_004**: Invalid username + invalid password
- **TC_LOGIN_005**: Username empty, password provided (validates inline `Required`)
- **TC_LOGIN_006**: Password empty, username provided (validates inline `Required`)
- **TC_LOGIN_007**: Both fields empty (validates both inline `Required` alerts)
- **TC_LOGIN_008**: Password masking (`type="password"` prevents shoulder surfing)
- **TC_LOGIN_009**: Leading & trailing spaces in username (strict credential exact-match verification)
- **TC_LOGIN_010**: Case sensitivity check (username case-insensitive, password case-sensitive)
- **TC_LOGIN_011**: Forgot Password link navigation to `/auth/requestPasswordResetCode`
- **TC_LOGIN_012**: Form submission via keyboard `Enter` key
- **TC_LOGIN_013**: SQL Injection resilience (`' OR '1'='1`)
- **TC_LOGIN_014**: Post-logout browser Back button session invalidation

### 2. Sheet 2: Employee Management (16 Scenarios)
Covers full lifecycle:
- **Add Employee**:
  - Valid mandatory + optional data submission
  - Missing mandatory fields (`First Name` / `Last Name`)
  - Boundary input length (>30 characters validation)
  - Duplicate Employee ID collision prevention
  - Special character handling in names
  - Toggle "Create Login Details" expandable section
- **View Employee**:
  - Employee presence in table
  - Exact search by unique Employee ID
  - Empty search results state handling ("No Records Found")
  - Transition to Personal Details edit view
- **Update Employee**:
  - Edit employee details (Nickname / Other ID)
  - Backend persistence verified across page refresh (F5)
  - Search filter Reset button functionality
- **Delete Employee**:
  - Confirmation modal popup ("Are you Sure?")
  - Cancellation of deletion preserves record
  - Confirmed permanent deletion removes record from list

### 3. Sheet 3: Bug & Usability Report (4 Real Issues)
Columns: `Bug ID`, `Title`, `Module`, `Description`, `Steps to Reproduce`, `Expected Result`, `Actual Result`, `Severity`, `Priority`, `Type`, `Status`, `Recommendation`
1. **BUG_LOGIN_001** *(Accessibility Concern - Medium / P2 | Status: Confirmed)*: Missing visual focus outline on interactive login form elements (WCAG 2.1 SC 2.4.7 Focus Visible).
2. **BUG_LOGIN_002** *(Usability Issue - Low / P3 | Status: Observed)*: Generic "Invalid credentials" error banner without lockout warning or guidance after repeated failed attempts.
3. **BUG_LOGIN_003** *(Usability Issue - Low / P4 | Status: Potential / Under Review)*: Username input strictly compares whitespace instead of auto-trimming, presenting an opportunity to enhance copy-paste usability.
4. **BUG_LOGIN_004** *(Accessibility Concern - Low / P4 | Status: Observed)*: Demo credentials card lacks semantic landmark attributes (`role="region"` / `aria-labelledby`) for screen reader announcement.

---

## 🤖 Automated Scenarios

The automated suite implements robust Page Object Model architecture across two primary test files:

### Suite 1: Login Automation (`Automation/tests/test_login.py`)
1. **`test_valid_login`**: Logs in with `Admin` / `admin123` and asserts Dashboard header `"Dashboard"` is displayed.
2. **`test_invalid_username`**: Asserts `"Invalid credentials"` alert and verifies user remains on login page.
3. **`test_invalid_password`**: Asserts `"Invalid credentials"` alert and verifies user remains on login page.
4. **`test_empty_username`**: Submits password only and asserts inline `"Required"` validation under username.
5. **`test_empty_password`**: Submits username only and asserts inline `"Required"` validation under password.
6. **`test_both_fields_empty`**: Submits empty form and asserts both fields display `"Required"` validations.

### Suite 2: Complete Employee Workflow (`Automation/tests/test_employee_workflow.py`)
Executes the full end-to-end lifecycle as required by the assignment specification:
1. **Login Flow**: Authenticates using valid credentials and verifies Dashboard.
2. **PIM Navigation**: Moves mouse over PIM menu using `ActionChains` hover, handles responsive hamburger collapse fallback, and clicks to navigate.
3. **Add 4 Unique Employees**:
   - Sequential creation using isolated test data from `Automation/utils/test_data.py`:
     - Employee 1: **John Test One**
     - Employee 2: **David Test Two**
     - Employee 3: **Robert Test Three**
     - Employee 4: **Michael Test Four**
   - Automatically generates unique numeric Employee IDs to prevent duplicate ID collisions on the live shared demo instance.
   - Waits for save success toast and backend persistence.
4. **Employee List Verification**:
   - Navigates to Employee List tab.
   - For each employee, searches and filters by unique ID.
   - Scrolls to the located record in the results table.
   - Asserts that the employee exists in the table.
   - Prints the required confirmation to stdout:
     ```
     John Test One - Name Verified
     David Test Two - Name Verified
     Robert Test Three - Name Verified
     Michael Test Four - Name Verified
     ```
5. **Logout Flow**:
   - Expands user profile menu in header.
   - Clicks Logout link.
   - Asserts return to Login page (`/auth/login`) with form inputs visible.

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+ (tested on Python 3.13)
- Google Chrome browser installed

### Step 1: Clone or Navigate to Project Directory
```powershell
cd C:\Users\srira\.gemini\antigravity\scratch\OrangeHRM-QA-Assignment
```

### Step 2: Create and Activate Virtual Environment
```powershell
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
venv\Scripts\Activate.ps1

# Activate on Windows (Command Prompt)
venv\Scripts\activate.bat

# Activate on macOS / Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```powershell
pip install -r Automation/requirements.txt
```

---

## 🚀 Running Tests

### 1. Run the Entire Test Suite (Default Headless Mode)
From the project root:
```powershell
pytest -v
```

### 2. Run in Visible (Headed) Browser Mode
To view browser interactions live:
```powershell
pytest -v --headed
```

### 3. Run Specific Test Suites
```powershell
# Run only Login edge cases
pytest -v Automation/tests/test_login.py

# Run only the Complete Employee Workflow
pytest -v Automation/tests/test_employee_workflow.py
```

### 4. Regenerate Manual Testing Excel Spreadsheet
```powershell
python create_excel_test_cases.py
```

---

## 📊 Actual Test Execution Results

All tests were executed against the live OrangeHRM demo instance:

```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\srira\.gemini\antigravity\scratch\OrangeHRM-QA-Assignment
configfile: pytest.ini
collected 7 items

Automation/tests/test_employee_workflow.py::TestEmployeeWorkflow::test_complete_employee_workflow PASSED
Automation/tests/test_login.py::TestLogin::test_valid_login PASSED
Automation/tests/test_login.py::TestLogin::test_invalid_username PASSED
Automation/tests/test_login.py::TestLogin::test_invalid_password PASSED
Automation/tests/test_login.py::TestLogin::test_empty_username PASSED
Automation/tests/test_login.py::TestLogin::test_empty_password PASSED
Automation/tests/test_login.py::TestLogin::test_both_fields_empty PASSED

======================== 7 passed in 126.14s (0:02:06) ========================
```

### Verified Workflow Console Output:
```text
John Test One - Name Verified
David Test Two - Name Verified
Robert Test Three - Name Verified
Michael Test Four - Name Verified
All 4 employees successfully verified!
```

---

## 🏛️ Design Pattern & Architecture

This project strictly implements the **Page Object Model (POM)**:
1. **Separation of Concerns**: Test methods only contain assertions and business flow steps. Web element locators and low-level Selenium interactions reside strictly within Page classes.
2. **Single Source of Truth**: Element locators (By.NAME, By.XPATH, By.CSS_SELECTOR) are declared once per page as class constants.
3. **Explicit Synchronization**: Eliminates brittle `time.sleep()` calls, utilizing `WebDriverWait` combined with `expected_conditions` (`visibility_of_element_located`, `element_to_be_clickable`, `invisibility_of_element_located`).
4. **Resilience & Responsive Handling**: Dynamically manages window dimensions and provides responsive drawer toggle handling if the browser enters a collapsed viewport state.
5. **Automated Defect Diagnostics**: The `pytest_runtest_makereport` hook captures timestamped screenshots under `screenshots/` automatically whenever any test step fails.

---

## 🐙 GitHub Repository

```text
GitHub Repository:
[ADD GITHUB URL HERE]
```
*(Add your remote GitHub repository URL above before final submission).*
