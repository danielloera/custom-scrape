from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from website_scrape_config import WebsiteScrapeConfig

amiami_config = WebsiteScrapeConfig(
    name="Amiami Hatsune Miku Figure Preorders",
    urls=[
    # Bishoujo
    'https://www.amiami.com/eng/search/list/?s_keywords=Hatsune%20Miku&s_st_list_preorder_available=1&s_cate_tag=14',
    # Plastic models
    'https://www.amiami.com/eng/search/list/?s_keywords=Hatsune%20Miku&s_st_list_preorder_available=1&s_cate_tag=36'],
    wait_for_class='new-items',
    item_class='newly-added-items__item'
)
firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = True
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference("javascript.enabled", True)
driver = webdriver.Firefox(options=firefox_options,
                           firefox_profile=firefox_profile)


def scrape_and_screenshot_urls(scrape_config):
    url_to_screenshots_map = defaultdict(lambda: [])
    print(f'Scraping {scrape_config.name}')
    for i, url in enumerate(scrape_config.urls):
        print(f'Loading url {i + 1}: {url}')
        driver.get(url)
        print(f'Waiting for {scrape_config.wait_for_class} to appear...')
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.CLASS_NAME, scrape_config.wait_for_class)))
        items = driver.find_elements_by_class_name(scrape_config.item_class)
        for item in items:
            print('FOUND:', item.text, '\n\n')
            screenshot_name = f'screenshots/{item.text}.png'
            url_to_screenshots_map[url].append(screenshot_name)
            item.screenshot(screenshot_name)
        print('done.')
    driver.quit()
    return url_to_screenshots_map


scrape_and_screenshot_urls(amiami_config)
