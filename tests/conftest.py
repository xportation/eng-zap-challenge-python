import json
import os
from unittest import mock

import pytest

from portal_api import services, storages, models


@pytest.fixture
def storage():
    data_filename = os.path.join(os.path.dirname(__file__), 'assets/sample_data.json')
    with open(data_filename) as f:
        data = list(json.load(f))
        items = []
        for item in data:
            items.append(models.Property(**item))
        data_loader = mock.MagicMock()
        data_loader.all.return_value = items
        return storages.MemoryStorage(data_loader)


@pytest.fixture
def base_restrictions():
    return services.BaseRestrictions()


@pytest.fixture
def zap_restrictions():
    return services.ZapRestrictions()


@pytest.fixture
def viva_real_restrictions():
    return services.VivaRealRestrictions()


@pytest.fixture
def sale_property():
    data = {
        'usableAreas': 70,
        'listingType': 'USED',
        'createdAt': '2017-04-22T18:39:31.138Z',
        'listingStatus': 'ACTIVE',
        'id': '7baf2775d4a2',
        'parkingSpaces': 1,
        'updatedAt': '2017-04-22T18:39:31.138Z',
        'owner': False,
        'images': [
          'https://resizedimgs.vivareal.com/crop/400x300/vr.images.sp/f908948bf1d9e53d36c4734d296feb99.jpg'
        ],
        'address': {
          'city': '',
          'neighborhood': '',
          'geoLocation': {
            'precision': 'RANGE_INTERPOLATED',
            'location': {
              'lon': -46.692307,
              'lat': -23.605332
            }
          }
        },
        'bathrooms': 1,
        'bedrooms': 2,
        'pricingInfos': {
          'yearlyIptu': '60',
          'price': '276000',
          'businessType': 'SALE',
          'monthlyCondoFee': '814'
        }
    }
    return models.Property(**data)


@pytest.fixture
def rental_property(sale_property):
    rental_property = sale_property.copy(deep=True)
    rental_property.pricing_info.business_type = models.BusinessType.rental
    rental_property.pricing_info.period = 'MONTHLY'
    rental_property.pricing_info.price = '2200'
    rental_property.pricing_info.rental_total_price = '3300'
    rental_property.pricing_info.monthly_condo_fee = '1100'
    rental_property.bedrooms = 4
    rental_property.bathrooms = 2
    return rental_property


@pytest.fixture
def zap_portal(storage, zap_restrictions):
    return services.Portal(storage, zap_restrictions)


@pytest.fixture
def viva_real_portal(storage, viva_real_restrictions):
    return services.Portal(storage, viva_real_restrictions)
