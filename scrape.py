from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from website_scrape_config import WebsiteScrapeConfig

amiami_config = WebsiteScrapeConfig(
    name="Hatsune Miku Bishoujo Preorders",
    url='https://www.amiami.com/eng/search/list/?s_keywords=Hatsune%20Miku&' +
    's_st_list_preorder_available=1&s_cate_tag=14',
    wait_for_class='new-items',
    item_class='newly-added-items__item'
)
firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = True
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference("javascript.enabled", True)
driver = webdriver.Firefox(options=firefox_options,
                           firefox_profile=firefox_profile)

def scrape(scrape_config):
    print(f'Scraping {scrape_config.name}')
    driver.get(scrape_config.url)
    print(f'Waiting for {scrape_config.wait_for_class} to appear...')
    WebDriverWait(driver, 30).until(EC.presence_of_element_located(
        (By.CLASS_NAME, scrape_config.wait_for_class)))
    items = driver.find_elements_by_class_name(scrape_config.item_class)
    for item in items:
        print('FOUND:', item.text, '\n\n')
        item.screenshot(f'screenshots/{item.text}.png')
    print('done.')
    driver.quit()

scrape(amiami_config)
