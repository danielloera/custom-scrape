from src.scrape import SeleniumScraper
from src.website_scrape_config import WebsiteScrapeConfig

configs = WebsiteScrapeConfig.listFromFile('scrape_configs.json')
scraper = SeleniumScraper(headless=True, js_enabled=True)
for config in configs:
    url_to_screenshots_map = scraper.scrape_and_screenshot_urls(config)
