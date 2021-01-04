import re


class WebsiteScrapeConfig:

    def __init__(self, name=None, urls=None, wait_for_class=None, item_class=None):
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