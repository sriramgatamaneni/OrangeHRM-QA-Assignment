import time
from typing import List, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException
)
from Automation.utils.logger import get_logger

class BasePage:
    """Base Page Object providing core explicit wait and interaction methods."""
    
    def __init__(self, driver: WebDriver, timeout: int = 15):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.logger = get_logger(self.__class__.__name__)
        
    def find_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            return wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            self.logger.error(f"Element not visible with locator: {locator}")
            raise

    def find_present_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            return wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            self.logger.error(f"Element not present with locator: {locator}")
            raise

    def find_elements(self, locator: Tuple[str, str], timeout: int = None) -> List[WebElement]:
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            wait.until(EC.presence_of_element_located(locator))
            return self.driver.find_elements(*locator)
        except TimeoutException:
            return []

    def click(self, locator: Tuple[str, str], timeout: int = None):
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            elem = wait.until(EC.element_to_be_clickable(locator))
            elem.click()
            self.logger.debug(f"Clicked element: {locator}")
        except ElementClickInterceptedException:
            self.logger.warning(f"Click intercepted for {locator}. Waiting for form loader overlay to disappear...")
            self.wait_for_invisibility((By.CSS_SELECTOR, ".oxd-form-loader"), timeout=10)
            elem = wait.until(EC.element_to_be_clickable(locator))
            try:
                elem.click()
                self.logger.debug(f"Clicked element on retry: {locator}")
            except ElementClickInterceptedException:
                self.logger.warning(f"Click still intercepted for {locator}. Executing JavaScript click.")
                self.driver.execute_script("arguments[0].click();", elem)
        except TimeoutException:
            self.logger.error(f"Element not clickable with locator: {locator}")
            raise

    def send_keys(self, locator: Tuple[str, str], text: str, clear_first: bool = True, timeout: int = None):
        elem = self.find_element(locator, timeout)
        if clear_first:
            from selenium.webdriver.common.keys import Keys
            # In modern frameworks, clearing using Ctrl+A + Backspace ensures event triggers in Vue/React
            elem.send_keys(Keys.CONTROL + "a")
            elem.send_keys(Keys.BACKSPACE)
        elem.send_keys(text)
        self.logger.debug(f"Entered text into {locator}")

    def get_text(self, locator: Tuple[str, str], timeout: int = None) -> str:
        elem = self.find_element(locator, timeout)
        return elem.text.strip()

    def is_displayed(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException):
            return False

    def wait_for_url_contains(self, partial_url: str, timeout: int = None) -> bool:
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            return wait.until(EC.url_contains(partial_url))
        except TimeoutException:
            self.logger.error(f"URL did not contain '{partial_url}'. Current URL: {self.driver.current_url}")
            return False

    def hover_and_click(self, locator: Tuple[str, str], timeout: int = None):
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        elem = wait.until(EC.presence_of_element_located(locator))
        self.scroll_to_element(elem)
        actions = ActionChains(self.driver)
        actions.move_to_element(elem).pause(0.3).click().perform()
        self.logger.debug(f"Hovered and clicked element: {locator}")

    def scroll_to_element(self, element: WebElement):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)

    def wait_for_invisibility(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            return wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            return False
