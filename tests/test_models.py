from portal_api import models


def test_location_is_valid():
    location = models.Location(lat=1.221, lon=22.1234)
    assert location.is_valid()

    valid_locations = [(-1.221, -22.1234), (0.000001, 0.000001), (0.000001, -0.0000001)]
    for lat, lon in valid_locations:
        location.lat = lat
        location.lon = lon
        assert location.is_valid()


def test_location_is_invalid():
    location = models.Location(lat=0, lon=0)
    assert not location.is_valid()

    invalid_locations = [(0, 0.00000001), (0, -0.00000009), (0.00000009, -0.00000009)]
    for lat, lon in invalid_locations:
        location.lat = lat
        location.lon = lon
        assert not location.is_valid()


def test_non_numeric_monthly_condo_fee_must_return_zero():
    pricing = models.PricingInfo(price='1000', monthly_condo_fee='ABC')
    assert not pricing.get_monthly_condo_fee()


def test_get_monthly_condo_fee_must():
    pricing = models.PricingInfo(price='1000', monthly_condo_fee='22')
    assert pricing.get_monthly_condo_fee() == 22
