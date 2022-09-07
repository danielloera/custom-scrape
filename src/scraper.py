import os
from collections import defaultdict
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3.exceptions import MaxRetryError
from selenium_stealth import stealth

screenshots_directory_name = 'screenshots'


class SeleniumScraper:

    def __init__(self, headless, js_enabled, timeout_secs):
        firefox_options = webdriver.ChromeOptions()
        firefox_options.headless = headless
        if js_enabled:
            firefox_options.add_argument("--enable_javascript")
        self.driver = webdriver.Chrome(chrome_options=firefox_options)
        self.driver.maximize_window()
        stealth(self.driver,
                languages=["en_US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        self.timeout_secs = timeout_secs
        if not os.path.isdir(screenshots_directory_name):
            os.mkdir(screenshots_directory_name)
        self.saved_screenshots = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            return False
        self.cleanup()
        return True

    def scrape_and_screenshot_urls(self, scrape_config):
        url_to_screenshots_map = defaultdict(lambda: [])
        print(f'Scraping {scrape_config.name}')
        for url_index, url in enumerate(scrape_config.urls):
            print(f'\nLoading url {url_index + 1}: {url}')
            try:
                self.driver.get(url)
            except MaxRetryError as e:
                print(f'Unable to reach: {url}\n', e)
                continue
            print(f'Waiting for {scrape_config.wait_for_class} to appear...')
            wait_for_class = scrape_config.wait_for_class
            if wait_for_class is None:
                scrape_config.item_class
            try:
                WebDriverWait(self.driver, self.timeout_secs).until(
                    EC.presence_of_element_located((
                        By.CLASS_NAME, scrape_config.wait_for_class)))
            except TimeoutException:
                print('Timed out.')
                continue
            items = self.driver.find_elements_by_class_name(
                scrape_config.item_class)
            for item_index, item in enumerate(items):
                print('FOUND:', item.text, '\n\n')
                screenshot_name = (f'{screenshots_directory_name}/'
                                   f'{scrape_config.name}_'
                                   f'{url_index}_{item_index}.png')
                url_to_screenshots_map[url].append(screenshot_name)
                item.screenshot(screenshot_name)
                self.saved_screenshots.append(screenshot_name)
        return ScrapeResult(scrape_config.name, url_to_screenshots_map)

    def cleanup(self):
        for screenshot in self.saved_screenshots:
            os.remove(screenshot)
        self.driver.quit()


class ScrapeResult:

    def __init__(self, name, url_to_screenshots_map):
        self.name = name
        self.url_to_screenshots_map = url_to_screenshots_map
