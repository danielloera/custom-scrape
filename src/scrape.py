from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumScraper:

    def __init__(self, headless, js_enabled):
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.headless = headless
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("javascript.enabled", js_enabled)
        self.driver = webdriver.Firefox(options=firefox_options,
                                        firefox_profile=firefox_profile)

    def scrape_and_screenshot_urls(self, scrape_config):
        url_to_screenshots_map = defaultdict(lambda: [])
        print(f'Scraping {scrape_config.name}')
        for url_index, url in enumerate(scrape_config.urls):
            print(f'\nLoading url {url_index + 1}: {url}')
            self.driver.get(url)
            print(f'Waiting for {scrape_config.wait_for_class} to appear...')
            wait_for_class = scrape_config.wait_for_class
            if wait_for_class is None:
                scrape_config.item_class
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(
                (By.CLASS_NAME, scrape_config.wait_for_class)))
            items = self.driver.find_elements_by_class_name(
                scrape_config.item_class)
            for item_index, item in enumerate(items):
                print('FOUND:', item.text, '\n\n')
                screenshot_name = f'screenshots/{scrape_config.name}_{url_index}_{item_index}.png'
                url_to_screenshots_map[url].append(screenshot_name)
                item.screenshot(screenshot_name)
        self.driver.quit()
        return url_to_screenshots_map
