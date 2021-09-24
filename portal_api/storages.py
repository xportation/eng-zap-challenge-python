from typing import List

import requests
from pydantic import ValidationError

from portal_api import models


class DataLoaderWeb:
    def __init__(self, logger, data_url):
        self.logger = logger
        self.data_url = data_url
        self.items = []
        self.reload()

    def all(self) -> List[models.Property]:
        return self.items

    def reload(self):
        self.logger.debug('Reloading items')
        self.items = []
        resp = requests.get(self.data_url)
        if resp.ok:
            for item in resp.json():
                self.load_item(item)
        self.logger.debug('Reload done')

    def load_item(self, item):
        try:
            self.items.append(models.Property(**item))
        except ValidationError as e:
            self.logger.exception(e.json())


class MemoryStorage:
    def __init__(self, data_loader):
        self.items = data_loader.all()

    def load_filters(self, filters):
        items_filtered = []
        for item in self.items:
            if self.is_allowed(item, filters):
                items_filtered.append(item)
        return items_filtered

    @staticmethod
    def is_allowed(item, filters):
        if not len(filters):
            return True

        for f in filters:
            if not f.is_allowed(item):
                return False
        return True
