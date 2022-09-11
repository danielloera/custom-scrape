import os
from collections import defaultdict
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3.exceptions import MaxRetryError
from selenium_stealth import stealth
import time

screenshots_directory_name = 'screenshots'


class SeleniumScraper:

  def __init__(self, headless, js_enabled, timeout_secs, page_wait_secs):
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
    self.page_wait_secs = page_wait_secs
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
    url_to_scrape_data_map = defaultdict(lambda: [])
    print(f'Scraping {scrape_config.name}')
    for url_index, url in enumerate(scrape_config.urls):
      print(f'\nLoading url {url_index + 1}: {url}')
      try:
        self.driver.get(url)
        time.sleep(self.page_wait_secs)
      except MaxRetryError as e:
        print(f'Unable to reach: {url}\n', e)
        continue
      print(f'Waiting for {scrape_config.wait_for_class} to appear...')
      wait_for_class = scrape_config.wait_for_class
      if wait_for_class is None:
        scrape_config.item_class
      try:
        WebDriverWait(self.driver, self.timeout_secs).until(
            lambda driver: self.driver.execute_script(
                'return document.readyState') == 'complete')
        WebDriverWait(self.driver, self.timeout_secs).until(
            EC.presence_of_element_located((
                By.CLASS_NAME, scrape_config.wait_for_class)))
      except TimeoutException:
        print('Timed out.')
        continue
      items = self.driver.find_elements(By.CLASS_NAME,
                                        scrape_config.item_class)
      for item_index, item in enumerate(items):
        print('FOUND:', item.text, '\n\n')
        screenshot_name = (f'{screenshots_directory_name}/'
                           f'{scrape_config.name}_'
                           f'{url_index}_{item_index}.png')
        first_href = self.get_first_href(item)
        url_to_scrape_data_map[url].append(
            ScrapeData(screenshot_name, first_href))
        item.screenshot(screenshot_name)
        self.saved_screenshots.append(screenshot_name)
    return ScrapeResult(scrape_config.name, url_to_scrape_data_map)

  def get_first_href(self, element):
    a_tag = element.find_element(By.TAG_NAME, 'a')
    if a_tag != None:
      return a_tag.get_attribute('href')

  def cleanup(self):
    for screenshot in self.saved_screenshots:
      os.remove(screenshot)
    self.driver.quit()


class ScrapeResult:

  def __init__(self, name, url_to_scrape_data_map):
    self.name = name
    self.url_to_scrape_data_map = url_to_scrape_data_map


class ScrapeData:

  def __init__(self, screenshot, href):
    self.screenshot = screenshot
    self.href = href
