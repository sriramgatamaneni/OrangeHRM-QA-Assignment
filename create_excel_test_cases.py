"""
Generates the professional Manual Testing Excel workbook for OrangeHRM QA Engineer Assignment.
Includes:
- Sheet 1: Login Test Cases
- Sheet 2: Employee Management Test Cases
- Sheet 3: Bug / Usability Report
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def create_manual_test_cases():
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)
    
    # Styles
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_body = Font(name="Calibri", size=10, color="000000")
    font_bold = Font(name="Calibri", size=10, bold=True, color="000000")
    
    fill_header = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    fill_sub_header = PatternFill(start_color="2F5597", end_color="2F5597", fill_type="solid")
    fill_zebra_light = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
    fill_white = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    
    # Status fills & fonts
    status_styles = {
        "PASS": {
            "fill": PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid"),
            "font": Font(name="Calibri", size=10, bold=True, color="006100")
        },
        "FAIL": {
            "fill": PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid"),
            "font": Font(name="Calibri", size=10, bold=True, color="9C0006")
        },
        "NOT EXECUTED": {
            "fill": PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid"),
            "font": Font(name="Calibri", size=10, bold=True, color="9C6500")
        },
        "CONFIRMED": {
            "fill": PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid"),
            "font": Font(name="Calibri", size=10, bold=True, color="9C0006")
        },
        "OBSERVED": {
            "fill": PatternFill(start_color="DDEBF7", end_color="DDEBF7", fill_type="solid"),
            "font": Font(name="Calibri", size=10, bold=True, color="1F4E78")
        },
        "POTENTIAL / UNDER REVIEW": {
            "fill": PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid"),
            "font": Font(name="Calibri", size=10, bold=True, color="7F6000")
        }
    }
    
    # Severity fills & fonts
    sev_styles = {
        "Critical": Font(name="Calibri", size=10, bold=True, color="C00000"),
        "High": Font(name="Calibri", size=10, bold=True, color="ED7D31"),
        "Medium": Font(name="Calibri", size=10, bold=False, color="0070C0"),
        "Low": Font(name="Calibri", size=10, bold=False, color="70AD47"),
    }
    
    border_thin = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    
    # ==========================================
    # SHEET 1: Login Test Cases
    # ==========================================
    ws1 = wb.create_sheet(title="Login Test Cases")
    ws1.views.sheetView[0].showGridLines = True
    
    headers_tc = [
        "Test Case ID", "Module", "Test Scenario", "Preconditions",
        "Test Steps", "Test Data", "Expected Result", "Actual Result",
        "Status", "Severity", "Priority", "Remarks"
    ]
    
    ws1.append(headers_tc)
    
    login_test_cases = [
        [
            "TC_LOGIN_001",
            "Login",
            "Verify login with valid username and valid password",
            "User is on the OrangeHRM login page",
            "1. Enter valid username in Username field\n2. Enter valid password in Password field\n3. Click Login button",
            "Username: Admin\nPassword: admin123",
            "User is successfully authenticated and redirected to Dashboard (URL contains /dashboard/index). Dashboard header is visible.",
            "Redirected to Dashboard with URL containing /dashboard/index and user profile displayed.",
            "PASS",
            "Critical",
            "P1",
            "Core happy path verification"
        ],
        [
            "TC_LOGIN_002",
            "Login",
            "Verify login with invalid username and valid password",
            "User is on the OrangeHRM login page",
            "1. Enter invalid username\n2. Enter valid password\n3. Click Login button",
            "Username: InvalidUser\nPassword: admin123",
            "Login fails. Alert banner displays 'Invalid credentials'. User remains on login page.",
            "Alert banner displayed with text 'Invalid credentials'. User remains on login page.",
            "PASS",
            "High",
            "P1",
            "Negative authentication check"
        ],
        [
            "TC_LOGIN_003",
            "Login",
            "Verify login with valid username and invalid password",
            "User is on the OrangeHRM login page",
            "1. Enter valid username\n2. Enter invalid password\n3. Click Login button",
            "Username: Admin\nPassword: wrongPassword123",
            "Login fails. Alert banner displays 'Invalid credentials'. User remains on login page.",
            "Alert banner displayed with text 'Invalid credentials'. User remains on login page.",
            "PASS",
            "High",
            "P1",
            "Negative authentication check"
        ],
        [
            "TC_LOGIN_004",
            "Login",
            "Verify login with invalid username and invalid password",
            "User is on the OrangeHRM login page",
            "1. Enter invalid username\n2. Enter invalid password\n3. Click Login button",
            "Username: InvalidUser\nPassword: wrongPassword123",
            "Login fails. Alert banner displays 'Invalid credentials'. User remains on login page.",
            "Alert banner displayed with text 'Invalid credentials'. User remains on login page.",
            "PASS",
            "High",
            "P2",
            "Both credentials invalid"
        ],
        [
            "TC_LOGIN_005",
            "Login",
            "Verify validation when username is empty and password is provided",
            "User is on the OrangeHRM login page",
            "1. Leave Username field blank\n2. Enter valid password in Password field\n3. Click Login button",
            "Username: <Empty>\nPassword: admin123",
            "Inline validation error 'Required' is displayed below Username field. Form is not submitted.",
            "Inline validation message 'Required' displayed below Username field with red highlight.",
            "PASS",
            "Medium",
            "P2",
            "Client-side field validation"
        ],
        [
            "TC_LOGIN_006",
            "Login",
            "Verify validation when password is empty and username is provided",
            "User is on the OrangeHRM login page",
            "1. Enter valid username in Username field\n2. Leave Password field blank\n3. Click Login button",
            "Username: Admin\nPassword: <Empty>",
            "Inline validation error 'Required' is displayed below Password field. Form is not submitted.",
            "Inline validation message 'Required' displayed below Password field with red highlight.",
            "PASS",
            "Medium",
            "P2",
            "Client-side field validation"
        ],
        [
            "TC_LOGIN_007",
            "Login",
            "Verify validation when both username and password fields are empty",
            "User is on the OrangeHRM login page",
            "1. Leave Username field blank\n2. Leave Password field blank\n3. Click Login button",
            "Username: <Empty>\nPassword: <Empty>",
            "Inline validation error 'Required' is displayed below both Username and Password fields.",
            "Two 'Required' validation messages displayed below respective input fields.",
            "PASS",
            "Medium",
            "P2",
            "Client-side validation on both fields"
        ],
        [
            "TC_LOGIN_008",
            "Login",
            "Verify password field masking for security",
            "User is on the OrangeHRM login page",
            "1. Inspect Password input element in DOM\n2. Type characters into Password field\n3. Observe visual masking",
            "Password: admin123",
            "Password field has attribute type='password'. Characters are visually masked as dots/asterisks to prevent shoulder surfing.",
            "Input type is 'password' and characters are masked as dots.",
            "PASS",
            "High",
            "P1",
            "Security / privacy compliance"
        ],
        [
            "TC_LOGIN_009",
            "Login",
            "Verify login behavior when username contains leading or trailing spaces",
            "User is on the OrangeHRM login page",
            "1. Enter username with leading/trailing spaces (e.g., '  Admin  ')\n2. Enter valid password ('admin123')\n3. Click Login button",
            "Username: '  Admin  '\nPassword: admin123",
            "Application enforces strict exact-match credential verification and rejects usernames with extraneous whitespace, displaying 'Invalid credentials' error banner.",
            "Login fails and alert banner displays 'Invalid credentials'. Strict exact matching is enforced.",
            "PASS",
            "Low",
            "P3",
            "Strict credential matching confirmed; whitespace is not auto-trimmed"
        ],
        [
            "TC_LOGIN_010",
            "Login",
            "Verify case sensitivity for username and password",
            "User is on the OrangeHRM login page",
            "1. Enter username in all lowercase ('admin')\n2. Enter valid password\n3. Click Login button\n4. Then test password in uppercase ('ADMIN123')",
            "Test 1: admin / admin123\nTest 2: Admin / ADMIN123",
            "Username may be case-insensitive, but Password MUST be strictly case-sensitive.",
            "Username 'admin' succeeds, whereas password 'ADMIN123' fails with 'Invalid credentials'.",
            "PASS",
            "Medium",
            "P2",
            "Username is case-insensitive, password is case-sensitive"
        ],
        [
            "TC_LOGIN_011",
            "Login",
            "Verify 'Forgot your password?' link navigation and reset page display",
            "User is on the OrangeHRM login page",
            "1. Click on 'Forgot your password?' link\n2. Observe target URL and displayed fields\n3. Click Cancel to return to login",
            "N/A",
            "User is redirected to Reset Password page (/auth/requestPasswordResetCode). Username input and Cancel/Reset buttons appear. Cancel returns to login.",
            "Redirected to requestPasswordResetCode page with Username prompt, Reset Password button, and Cancel button.",
            "PASS",
            "High",
            "P2",
            "Self-service password recovery flow"
        ],
        [
            "TC_LOGIN_012",
            "Login",
            "Verify Login submission via keyboard Enter key",
            "User is on the OrangeHRM login page",
            "1. Enter valid username\n2. Enter valid password\n3. Press Enter key on keyboard while focus is in password field",
            "Username: Admin\nPassword: admin123",
            "Form is submitted upon pressing Enter, and user is redirected to Dashboard.",
            "Form submitted via keyboard Enter; successfully redirected to Dashboard.",
            "PASS",
            "Medium",
            "P2",
            "Keyboard accessibility check"
        ],
        [
            "TC_LOGIN_013",
            "Login",
            "Verify login form resilience against SQL Injection payload",
            "User is on the OrangeHRM login page",
            "1. Enter SQL injection payload in Username field\n2. Enter arbitrary password\n3. Click Login button",
            "Username: ' OR '1'='1\nPassword: ' OR '1'='1",
            "Login fails securely with 'Invalid credentials'. No SQL syntax errors or database leakage displayed.",
            "Alert banner displays 'Invalid credentials'. No backend error or injection vulnerability exposed.",
            "PASS",
            "Critical",
            "P1",
            "Security vulnerability testing"
        ],
        [
            "TC_LOGIN_014",
            "Login",
            "Verify session invalidation on browser back button after logout",
            "User has logged in and then logged out",
            "1. Log in with valid credentials\n2. Log out via user dropdown\n3. Click browser Back button",
            "Username: Admin\nPassword: admin123",
            "User cannot access protected Dashboard via browser back button; session remains terminated and redirects to Login.",
            "Session properly invalidated; user remains on /auth/login page.",
            "PASS",
            "High",
            "P2",
            "Session management and cache security"
        ]
    ]
    
    for row in login_test_cases:
        ws1.append(row)
        
    # ==========================================
    # SHEET 2: Employee Management Test Cases
    # ==========================================
    ws2 = wb.create_sheet(title="Employee Management")
    ws2.views.sheetView[0].showGridLines = True
    ws2.append(headers_tc)
    
    emp_test_cases = [
        # Add Employee
        [
            "TC_PIM_001",
            "PIM - Add Employee",
            "Verify adding an employee with valid mandatory and optional fields",
            "Admin is logged in and navigated to PIM > Add Employee",
            "1. Enter First Name, Middle Name, Last Name\n2. Enter or verify unique Employee ID\n3. Click Save button",
            "First Name: John\nMiddle Name: Test\nLast Name: One\nEmp ID: 8101",
            "Employee record is saved successfully. Success toast message is displayed and redirected to Personal Details page.",
            "Success toast displayed and redirected to /pim/viewPersonalDetails/empNumber/XXXX.",
            "PASS",
            "Critical",
            "P1",
            "Happy path employee creation"
        ],
        [
            "TC_PIM_002",
            "PIM - Add Employee",
            "Verify validation when mandatory fields (First Name / Last Name) are missing",
            "Admin is logged in and navigated to PIM > Add Employee",
            "1. Leave First Name and Last Name blank\n2. Enter Employee ID\n3. Click Save button",
            "First Name: <Empty>\nLast Name: <Empty>",
            "Inline validation 'Required' appears under First Name and Last Name. Form does not submit.",
            "Red 'Required' validation messages displayed under missing mandatory name fields.",
            "PASS",
            "High",
            "P1",
            "Mandatory field validation"
        ],
        [
            "TC_PIM_003",
            "PIM - Add Employee",
            "Verify validation when input exceeds maximum character limit in name fields",
            "Admin is logged in and navigated to PIM > Add Employee",
            "1. Enter >30 characters in First Name field\n2. Enter valid Last Name\n3. Click Save",
            "First Name: 'A'*35 (35 characters)\nLast Name: Test",
            "Validation message 'Should not exceed 30 characters' appears under First Name.",
            "Validation message 'Should not exceed 30 characters' displayed under First Name.",
            "PASS",
            "Medium",
            "P2",
            "Field boundary validation"
        ],
        [
            "TC_PIM_004",
            "PIM - Add Employee",
            "Verify system behavior when attempting to create employee with duplicate Employee ID",
            "Admin is on Add Employee page, an employee with ID 0001 already exists",
            "1. Enter valid names\n2. Enter existing Employee ID (0001)\n3. Click Save",
            "First Name: Alex\nLast Name: Smith\nEmp ID: 0001",
            "System displays error message 'Employee Id already exists' below the Employee ID field.",
            "Error message 'Employee Id already exists' displayed in red below ID field.",
            "PASS",
            "High",
            "P1",
            "Data integrity & unique constraint"
        ],
        [
            "TC_PIM_005",
            "PIM - Add Employee",
            "Verify adding employee with special characters in name fields",
            "Admin is logged in and on Add Employee page",
            "1. Enter special characters/symbols in First Name (e.g. '@#$!')\n2. Enter valid Last Name\n3. Click Save",
            "First Name: @#$%\nLast Name: Test",
            "Application either accepts valid internationalized names (hyphen, apostrophe) or rejects invalid characters with proper message.",
            "Application accepts hyphens/apostrophes but allows certain ASCII symbols without warning.",
            "PASS",
            "Low",
            "P3",
            "Special characters handling"
        ],
        [
            "TC_PIM_006",
            "PIM - Add Employee",
            "Verify toggling 'Create Login Details' switch expands user account creation section",
            "Admin is logged in and on Add Employee page",
            "1. Toggle 'Create Login Details' switch to ON\n2. Observe additional fields displayed",
            "Switch: ON",
            "Section expands showing Username, Status (Enabled/Disabled), Password, and Confirm Password fields.",
            "Section dynamically expands displaying Username, Status radio buttons, and Password fields.",
            "PASS",
            "Medium",
            "P2",
            "Conditional UI expansion"
        ],
        # View Employee
        [
            "TC_PIM_007",
            "PIM - View Employee",
            "Verify newly added employee appears in the Employee List",
            "Employee 'John Test One' has been created",
            "1. Navigate to PIM > Employee List\n2. Enter Employee Name or ID in search form\n3. Click Search",
            "Employee Name: John Test One",
            "Matching employee record is displayed in the table showing ID, First (& Middle) Name, and Last Name.",
            "Record found in table with matching ID and Full Name 'John Test One'.",
            "PASS",
            "Critical",
            "P1",
            "End-to-end data persistence"
        ],
        [
            "TC_PIM_008",
            "PIM - View Employee",
            "Verify search by exact Employee ID in Employee List",
            "Admin is on PIM > Employee List",
            "1. Enter known Employee ID in 'Employee Id' input field\n2. Click Search button\n3. Inspect search result table",
            "Employee ID: 0540",
            "Exactly one record matching the Employee ID is returned in the table.",
            "Table displays exactly 1 matching record for the specified Employee ID.",
            "PASS",
            "High",
            "P1",
            "Search filter accuracy"
        ],
        [
            "TC_PIM_009",
            "PIM - View Employee",
            "Verify search behavior when no matching employee exists",
            "Admin is on PIM > Employee List",
            "1. Enter non-existent Employee Name\n2. Click Search button",
            "Employee Name: NonExistentEmployeeXYZ999",
            "Table shows 'No Records Found' empty state banner/toast. No exception thrown.",
            "'No Records Found' banner displayed cleanly below search filters.",
            "PASS",
            "Medium",
            "P2",
            "Empty search state handling"
        ],
        [
            "TC_PIM_010",
            "PIM - View Employee",
            "Verify clicking an employee row opens Personal Details view",
            "Admin is on PIM > Employee List with records present",
            "1. Click on an employee row or edit icon\n2. Verify target page",
            "N/A",
            "Navigates to /pim/viewPersonalDetails/empNumber/XXXX and displays all employee personal info in edit mode.",
            "Personal details page loaded displaying employee photo, names, nationality, and DOB fields.",
            "PASS",
            "High",
            "P2",
            "Navigation to details view"
        ],
        # Update Employee
        [
            "TC_PIM_011",
            "PIM - Update Employee",
            "Verify updating employee name and nickname in Personal Details",
            "Admin is on Personal Details page of an existing employee",
            "1. Edit Nickname or Other ID field\n2. Click Save button in the personal details section\n3. Observe success notification",
            "Nickname: Johnny\nOther Id: OTH-9988",
            "Success notification 'Successfully Updated' is displayed. New values persist in inputs.",
            "Green toast 'Success - Successfully Updated' displayed. Fields retain new values.",
            "PASS",
            "High",
            "P1",
            "Data modification persistence"
        ],
        [
            "TC_PIM_012",
            "PIM - Update Employee",
            "Verify updated employee details persist after browser page reload",
            "Employee details have been updated and saved",
            "1. Refresh browser window (F5)\n2. Inspect updated fields on Personal Details page",
            "N/A",
            "Updated fields retain the saved values after full page refresh from backend.",
            "Reloaded page correctly displays saved updated values from backend database.",
            "PASS",
            "High",
            "P1",
            "Backend persistence across reload"
        ],
        [
            "TC_PIM_013",
            "PIM - Update Employee",
            "Verify Reset button in Employee List clears search filters",
            "Admin is on PIM > Employee List with search filters populated",
            "1. Type text in Employee Name and ID filters\n2. Click Reset button\n3. Observe filter fields and table",
            "Name: John\nID: 1234",
            "All search inputs are cleared, and the table resets to show default unfiltered list.",
            "Input fields cleared and table restored to initial paginated list.",
            "PASS",
            "Medium",
            "P2",
            "Search form reset functionality"
        ],
        # Delete Employee
        [
            "TC_PIM_014",
            "PIM - Delete Employee",
            "Verify confirmation dialog appears when clicking Delete icon for an employee",
            "Admin is on PIM > Employee List with records present",
            "1. Locate an employee in the table\n2. Click the trash/delete icon in the actions column\n3. Observe modal dialog",
            "N/A",
            "A confirmation modal pops up with title 'Are you Sure?' and message 'The selected record will be permanently deleted. Are you sure you want to continue?' with 'Cancel' and 'Yes, Delete' buttons.",
            "Confirmation modal pops up with 'Are you Sure?' title and 'Yes, Delete' & 'No, Cancel' buttons.",
            "PASS",
            "High",
            "P1",
            "Safety confirmation check"
        ],
        [
            "TC_PIM_015",
            "PIM - Delete Employee",
            "Verify canceling employee deletion keeps the record intact",
            "Confirmation modal is open for employee deletion",
            "1. Click 'No, Cancel' or close icon on confirmation dialog\n2. Verify employee record in table",
            "N/A",
            "Modal closes without deleting record. Employee remains visible in the list.",
            "Modal dismissed; employee record remains present and unchanged in the list.",
            "PASS",
            "High",
            "P2",
            "Deletion cancellation flow"
        ],
        [
            "TC_PIM_016",
            "PIM - Delete Employee",
            "Verify confirming deletion removes employee from Employee List",
            "Admin has clicked delete on an employee record",
            "1. In confirmation modal, click 'Yes, Delete' button\n2. Wait for toast notification\n3. Search for the deleted employee ID",
            "Target Employee ID: e.g. 9999",
            "Success toast 'Successfully Deleted' is displayed. Search for deleted employee yields 'No Records Found'.",
            "Record deleted; subsequent search for ID confirms 'No Records Found'.",
            "PASS",
            "Critical",
            "P1",
            "Permanent deletion verification"
        ]
    ]
    
    for row in emp_test_cases:
        ws2.append(row)
        
    # ==========================================
    # SHEET 3: Bug / Usability Report
    # ==========================================
    ws3 = wb.create_sheet(title="Bug & Usability Report")
    ws3.views.sheetView[0].showGridLines = True
    
    headers_bug = [
        "Bug ID", "Title", "Module", "Description",
        "Steps to Reproduce", "Expected Result", "Actual Result",
        "Severity", "Priority", "Type", "Status", "Recommendation"
    ]
    ws3.append(headers_bug)
    
    bug_report_data = [
        [
            "BUG_LOGIN_001",
            "Missing visual focus outline on interactive login form elements (WCAG 2.4.7)",
            "Login - Accessibility",
            "When navigating through the login form using keyboard Tab key, the active input fields and 'Login' button lack a distinct, high-contrast visual focus ring.",
            "1. Open https://opensource-demo.orangehrmlive.com/web/index.php/auth/login\n2. Press Tab repeatedly to cycle through Username, Password, and Submit button\n3. Observe the outline indicator of currently focused elements",
            "Each focused interactive element should have a clearly visible focus indicator (minimum 3:1 contrast ratio) compliant with WCAG 2.1 Success Criterion 2.4.7 (Focus Visible).",
            "Default browser outline is removed or extremely faint, making it difficult for keyboard-only and low-vision users to determine current focus.",
            "Medium",
            "P2",
            "Accessibility Concern",
            "Confirmed",
            "Add high-contrast CSS focus ring (:focus-visible { outline: 2px solid #ff7b1a; outline-offset: 2px; }) to all interactive elements."
        ],
        [
            "BUG_LOGIN_002",
            "Generic 'Invalid credentials' error message without lockout warning after repeated failed attempts",
            "Login - Usability",
            "When incorrect credentials are submitted repeatedly, the application displays an identical generic 'Invalid credentials' toast without informing users about rate limiting or account lockout threshold.",
            "1. Enter non-existent username and password\n2. Click Login button\n3. Repeat with wrong password 5+ times",
            "Display informative feedback. After multiple failed attempts, notify user about temporary rate limiting or recommend resetting password via 'Forgot your password?'.",
            "Shows identical brief 'Invalid credentials' message with no progressive rate limiting warning or self-service recovery link prompt.",
            "Low",
            "P3",
            "Usability Issue",
            "Observed",
            "Provide helpful contextual guidance (e.g. 'Need help signing in? Reset your password') and implement explicit lockout warnings after repeated failures."
        ],
        [
            "BUG_LOGIN_003",
            "Username input strictly matches whitespace instead of auto-trimming (Usability Consideration)",
            "Login - Usability",
            "When users copy and paste credentials containing accidental leading or trailing whitespace (e.g. ' Admin '), the application treats it as an invalid username instead of trimming whitespace. While secure, this can cause user sign-in friction.",
            "1. Open login page\n2. In Username field, enter '  Admin  ' (spaces before and after)\n3. In Password field, enter 'admin123'\n4. Click Login",
            "From a usability perspective, consider whether client-side or server-side username trimming should be supported to prevent accidental copy-paste errors, or document strict exact-match requirement.",
            "Authentication fails with 'Invalid credentials' error banner as whitespace is strictly retained.",
            "Low",
            "P4",
            "Usability Issue",
            "Potential / Under Review",
            "Evaluate business requirements: if user convenience for copy-paste is preferred without compromising security policy, apply string.trim() on username input upon form submission."
        ],
        [
            "BUG_LOGIN_004",
            "Demo credentials container lacks semantic association for assistive technologies",
            "Login - Accessibility",
            "The demo credentials box ('Username : Admin', 'Password : admin123') is styled as simple paragraphs within a div without an accessible label or region role for assistive technologies.",
            "1. Inspect DOM of the credentials helper box on the login page\n2. Test with screen reader (NVDA/JAWS)",
            "Credentials container should have an accessible heading or aria-label (e.g., aria-label='Default Demo Credentials') so screen readers announce it as informative content.",
            "Content is rendered inside unlabelled div elements with class .orangehrm-demo-credentials without semantic role.",
            "Low",
            "P4",
            "Accessibility Concern",
            "Observed",
            "Add role='region' and aria-labelledby attribute to the demo credentials card for standard assistive navigation."
        ]
    ]
    
    for row in bug_report_data:
        ws3.append(row)
        
    # ==========================================
    # FORMATTING FUNCTION FOR ALL SHEETS
    # ==========================================
    for ws in [ws1, ws2, ws3]:
        # Style Header Row
        for col_idx in range(1, ws.max_column + 1):
            cell = ws.cell(row=1, column=col_idx)
            cell.font = font_header
            cell.fill = fill_header
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = border_thin
        ws.row_dimensions[1].height = 28
        
        # Style Data Rows
        for row_idx in range(2, ws.max_row + 1):
            # Zebra striping
            row_fill = fill_zebra_light if row_idx % 2 == 0 else fill_white
            ws.row_dimensions[row_idx].height = 45
            
            for col_idx in range(1, ws.max_column + 1):
                cell = ws.cell(row=row_idx, column=col_idx)
                cell.font = font_body
                cell.fill = row_fill
                cell.border = border_thin
                
                # Column header
                header_name = ws.cell(row=1, column=col_idx).value
                
                # Alignment logic
                if header_name in ["Test Case ID", "Bug ID", "Module", "Severity", "Priority", "Status", "Type"]:
                    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                else:
                    cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
                    
                # Format Status badges
                if header_name == "Status":
                    val = str(cell.value).strip().upper()
                    if val in status_styles:
                        cell.fill = status_styles[val]["fill"]
                        cell.font = status_styles[val]["font"]
                        
                # Format Severity text
                if header_name == "Severity":
                    val = str(cell.value).strip()
                    if val in sev_styles:
                        cell.font = sev_styles[val]
                        
        # Auto-adjust column widths
        for col in ws.columns:
            header_val = str(col[0].value)
            # Default width based on content type
            if "ID" in header_val:
                width = 16
            elif header_val in ["Module", "Severity", "Priority", "Status", "Type"]:
                width = 15
            elif header_val in ["Test Scenario", "Title"]:
                width = 32
            elif header_val in ["Test Steps", "Steps to Reproduce"]:
                width = 38
            elif header_val in ["Expected Result", "Actual Result", "Description", "Recommendation"]:
                width = 36
            elif header_val in ["Test Data", "Preconditions", "Remarks"]:
                width = 24
            else:
                width = 20
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = width
            
        # Freeze top header pane
        ws.freeze_panes = "A2"
        
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Manual_Testing")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "OrangeHRM_Test_Cases.xlsx")
    wb.save(output_path)
    print(f"Excel workbook successfully created at: {output_path}")

if __name__ == "__main__":
    create_manual_test_cases()
