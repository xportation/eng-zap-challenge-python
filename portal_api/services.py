from portal_api import models


class BaseRestrictions:
    @staticmethod
    def is_around_zap_location(location):
        min_lon = -46.693419
        min_lat = -23.568704
        max_lon = -46.641146
        max_lat = -23.546686
        return min_lat < location.lat < max_lat and min_lon < location.lon < max_lon

    def check_rental_restricted(self, item):
        return False

    def check_sale_restricted(self, item):
        return False

    def is_restricted(self, item):
        if not item.address.geolocation.location.is_valid():
            return True
        return self.check_sale_restricted(item) or self.check_rental_restricted(item)


class ZapRestrictions(BaseRestrictions):
    min_rental_price = 3500
    min_usable_areas_price = 3500
    min_sale_price = 600000

    def check_rental_restricted(self, item):
        if item.pricing_info.business_type == models.BusinessType.rental:
            return int(item.pricing_info.price) < self.min_rental_price
        return False

    def check_sale_restricted(self, item):
        if item.pricing_info.business_type == models.BusinessType.sale:
            if item.usable_areas <= 0:
                return True

            sale_price = self.min_sale_price
            if self.is_around_zap_location(item.address.geolocation.location):
                sale_price = self.min_sale_price * 0.9

            usable_areas_price = int(item.pricing_info.price) / item.usable_areas
            return int(item.pricing_info.price) < sale_price or usable_areas_price <= self.min_usable_areas_price
        return False


class VivaRealRestrictions(BaseRestrictions):
    max_rental_price = 4000
    max_sale_price = 700000

    def check_rental_restricted(self, item):
        if item.pricing_info.business_type == models.BusinessType.rental:
            if not item.pricing_info.get_monthly_condo_fee():
                return True

            condo_fee_percentage = 0.3
            if self.is_around_zap_location(item.address.geolocation.location):
                condo_fee_percentage = 0.45

            max_monthly_condo_fee = int(item.pricing_info.price) * condo_fee_percentage
            monthly_condo_fee_exceeded = item.pricing_info.get_monthly_condo_fee() >= max_monthly_condo_fee
            return int(item.pricing_info.price) > self.max_rental_price or monthly_condo_fee_exceeded
        return False

    def check_sale_restricted(self, item):
        if item.pricing_info.business_type == models.BusinessType.sale:
            return int(item.pricing_info.price) > self.max_sale_price
        return False


class Portal:
    def __init__(self, storage, restrictions):
        self.storage = storage
        self.restrictions = restrictions

    def load_filters(self, filters):
        items = self.storage.load_filters(filters)
        return self.remove_restricted_items(items)

    def remove_restricted_items(self, items):
        return [item for item in items if not self.restrictions.is_restricted(item)]
