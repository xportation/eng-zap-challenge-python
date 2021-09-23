from unittest import mock

from portal_api import storages, models


def build_storage(sale_property, rental_property):
    data_loader = mock.MagicMock()
    data_loader.all.return_value = [sale_property, rental_property]
    return storages.MemoryStorage(data_loader)


def build_business_type_filter(business_type):
    business_filter = mock.MagicMock()
    business_filter.is_allowed.side_effect = lambda i: i.pricing_info.business_type == business_type
    return business_filter


def build_bedrooms_filter(bedrooms):
    business_filter = mock.MagicMock()
    business_filter.is_allowed.side_effect = lambda i: i.bedrooms == bedrooms
    return business_filter


def test_load_using_filters(sale_property, rental_property):
    storage = build_storage(sale_property, rental_property)
    rental_only = storage.load_filters([build_business_type_filter(models.BusinessType.rental)])
    assert len(rental_only) == 1
    assert rental_only[0].pricing_info.business_type == models.BusinessType.rental


def test_load_using_two_filters(sale_property, rental_property):
    storage = build_storage(sale_property, rental_property)
    all_properties = storage.load_filters([
        build_business_type_filter(models.BusinessType.rental),
        build_bedrooms_filter(2)
    ])
    assert len(all_properties) == 2
    assert all_properties[0].pricing_info.business_type == models.BusinessType.sale
    assert all_properties[1].pricing_info.business_type == models.BusinessType.rental
