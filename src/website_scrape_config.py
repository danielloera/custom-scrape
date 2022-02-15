import json


class WebsiteScrapeConfig:

    def __init__(self, name, urls, wait_for_class, item_class):
        self.name = name
        self.urls = urls
        self.wait_for_class = wait_for_class
        self.item_class = item_class

    def __key(self):
        return(self.name, self.urls, self.wait_for_class, self.item_class)

    def __eq__(self, other):
        return isinstance(other, WebsiteScrapeConfig) and self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())

    @staticmethod
    def listFromFile(config_file_name):
        with open(config_file_name) as f:
            json_configs = json.load(f)
            configs = []
            for json_config in json_configs:
                name = json_config.get("name", None)
                urls = json_config.get("urls", None)
                wait_for_class = json_config.get("wait_for_class", None)
                item_class = json_config.get("item_class", None)
                if name is None:
                    raise ValueError('Each scrape config needs a name.')
                if urls is None or not urls:
                    raise ValueError(
                        'Each scrape config needs at least 1 url.')
                if item_class is None:
                    raise ValueError('Each scrape config needs an item_class.')
                configs.append(WebsiteScrapeConfig(
                    name=name, urls=urls,
                    wait_for_class=wait_for_class, item_class=item_class))
        return configs
