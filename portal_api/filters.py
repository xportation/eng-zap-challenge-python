class BusinessTypeFilter:
    def __init__(self, business_type):
        self.business_type = business_type

    def is_allowed(self, item):
        return item.pricing_info.business_type == self.business_type


class CityFilter:
    def __init__(self, city):
        self.city = city

    def is_allowed(self, item):
        return item.address.city == self.city


class MinPriceFilter:
    def __init__(self, price):
        self.price = price

    def is_allowed(self, item):
        return int(item.pricing_info.price) >= self.price


class MaxPriceFilter:
    def __init__(self, price):
        self.price = price

    def is_allowed(self, item):
        return int(item.pricing_info.price) <= self.price


class BedroomsFilter:
    def __init__(self, bedrooms):
        self.bedrooms = bedrooms

    def is_allowed(self, item):
        return item.bedrooms == self.bedrooms


class BathroomsFilter:
    def __init__(self, bathrooms):
        self.bathrooms = bathrooms

    def is_allowed(self, item):
        return item.bathrooms == self.bathrooms


def filters_factory(filter_query):
    filters_map = {
        'business_type': BusinessTypeFilter,
        'city': CityFilter,
        'min_price': MinPriceFilter,
        'max_price': MaxPriceFilter,
        'bedrooms': BedroomsFilter,
        'bathrooms': BathroomsFilter,

    }
    filters = []
    for key, value in filter_query.__dict__.items():
        if value is not None:
            filter_class = filters_map.get(key)
            if filter_class:
                filters.append(filter_class(value))
    return filters
