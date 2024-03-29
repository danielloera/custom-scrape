import argparse
import src.discord_notifier as discord_notifier
from src.scraper import SeleniumScraper
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
                    help='Seconds to wait elements to appear.')
parser.add_argument('--page_wait_secs', type=int, default=3,
                    help='''Seconds to wait before searching the page.
                    This is useful if want to wait for images to load.''')
parser.add_argument('--discord_notification_channel', default=None,
                    help='''The discord text channel name to send results to.
                    Requires the DISCORD_TOKEN environment variable to be set.
                    ''')
parser.add_argument('--notify_on_changes', action='store_true',
                    help='''Only notifies on changes to items.
                    Will store a file locally to keep track.''')
parser.set_defaults(notify_on_changes=False)

if __name__ == '__main__':
  args = parser.parse_args()
  configs = WebsiteScrapeConfig.listFromFile(args.config_file)
  try:
    with SeleniumScraper(headless=args.headless,
                         js_enabled=args.js_enabled,
                         timeout_secs=args.timeout_secs,
                         page_wait_secs=args.page_wait_secs) as scraper:
      results = [scraper.scrape_and_screenshot_urls(config)
                 for config in configs]
      if args.discord_notification_channel is not None:
        discord_notifier.send_scrape_result_messages(
            results, args.discord_notification_channel, args.notify_on_changes)
  except Exception as err:
    print(f'Error oh noes!:\n{err}')
    discord_notifier.send_message(f'Scrape failed:\n{err}', args.discord_notification_channel)
