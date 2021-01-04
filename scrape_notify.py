from src.scrape import SeleniumScraper
from src.website_scrape_config import WebsiteScrapeConfig

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

scraper = SeleniumScraper()
scraper.scrape_and_screenshot_urls(amiami_config)