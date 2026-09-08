import os
import time
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Automation.utils.logger import get_logger

logger = get_logger("Conftest")

def pytest_addoption(parser):
    """Adds CLI options for Pytest execution if not already added."""
    try:
        parser.addoption(
            "--headed",
            action="store_true",
            default=False,
            help="Run browser in visible (headed) mode instead of headless."
        )
    except ValueError:
        pass

@pytest.fixture(scope="function")
def driver(request):
    """
    Initializes and yields a Chrome WebDriver instance configured with
    optimal options. Captures screenshot on failure and cleanly quits on teardown.
    """
    is_headed = request.config.getoption("--headed")
    
    options = Options()
    if not is_headed:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    
    logger.info(f"Launching Chrome (Headed: {is_headed})...")
    driver_instance = webdriver.Chrome(options=options)
    driver_instance.set_window_size(1920, 1080)
    
    # Attach driver to request node for screenshot hook
    request.node.driver = driver_instance
    
    yield driver_instance
    
    logger.info("Tearing down Chrome WebDriver session...")
    try:
        driver_instance.quit()
    except Exception as e:
        logger.warning(f"Error during driver quit: {e}")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to capture a full-page screenshot upon test failure.
    Screenshots are saved in the project screenshots/ directory.
    """
    outcome = yield
    report = outcome.get_result()
    
    # Only capture during execution phase
    if report.when == "call" and report.failed:
        driver_instance = getattr(item, "driver", None)
        if driver_instance:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name.replace("/", "_").replace("::", "_")
            
            # Determine screenshots directory relative to project root
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            screenshots_dir = os.path.join(base_dir, "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            
            screenshot_file = os.path.join(screenshots_dir, f"FAIL_{test_name}_{timestamp}.png")
            try:
                driver_instance.save_screenshot(screenshot_file)
                logger.error(f"TEST FAILED: [{item.name}]. Screenshot saved to: {screenshot_file}")
            except Exception as ex:
                logger.error(f"Failed to capture screenshot for [{item.name}]: {ex}")
