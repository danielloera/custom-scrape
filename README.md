# custom-scrape
Custom web scraper for screenshotting item listings using a json config.

## Usage
By default running:

```sh
python custom_scrape.python
```
will scrape the sites defined in `scrape_configs.json` and save the found items in the `screenshots` folder.

`scrape_configs.json` must contain a list of objects in the following format:
```json
[
    {
        "name": "Amiami Figure Preorders",
        "urls": ["something.com", "other.com"],
        "item_class": "item",
        "wait_for_class": "item-list"
    }
]
```
`name`: Name of the site(s) you are scraping.
This is just to label them in the final output, can be anything.

`urls`: List is urls to scrape.

`item_class`: CSS class you want to scrape and screenshot on the page.

##### Optional
`wait_for_class`: Needed only if you want to wait on a specific CSS class before scraping. This defaults to `item_class`.

## Arguments

The name of the discord text channel to send results to. Requires the `DISCORD_TOKEN` environment variable to be set.
```sh
--discord_notification_channel general
``` 

Change the config file to use (default is `scrape_configs.json`):
```sh
--config_file "some_other_file.text"
```
Show the web browser while it is scraping (i.e. make it non-headless):
```sh
--no_headless
```
Disable javascript:
```sh
--js_disabled
```
Adjust how long the scraper waits items to appear (default is 30):
```sh
--timeout_secs 15
```
Adjust how long the scraper before searching each page (default is 3):
```sh
--page_wait_secs 10
```