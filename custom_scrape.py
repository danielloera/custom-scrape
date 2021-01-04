import argparse
from src.scrape import SeleniumScraper
from src.website_scrape_config import WebsiteScrapeConfig

# Program arguments
parser = argparse.ArgumentParser()
parser.add_argument('--config_file', default='scrape_configs.json',
                    help='file to load scrape configs from.')
parser.add_argument('--no_headless', dest='headless', action='store_false',
                    help='enable browser head.')
parser.set_defaults(headless=True)
parser.add_argument('--js_disabled', dest='js_enabled', action='store_false',
                    help='Disable javascript.')
parser.set_defaults(js_enabled=True)
parser.add_argument('--timeout_secs', type=int, default=30,
                    help='Seconds to wait while waiting for pages to load.')

if __name__ == '__main__':
    args = parser.parse_args()
    configs = WebsiteScrapeConfig.listFromFile(args.config_file)
    scraper = SeleniumScraper(
        headless=args.headless, js_enabled=args.js_enabled, timeout_secs=args.timeout_secs)
    for config in configs:
        url_to_screenshots_map = scraper.scrape_and_screenshot_urls(config)
