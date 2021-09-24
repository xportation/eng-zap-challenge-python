
def test_must_ignore_any_property_without_geolocation(zap_restrictions, viva_real_restrictions,
                                                      sale_property, rental_property):
    sale_property.address.geolocation.location.lat = 0
    sale_property.address.geolocation.location.lon = 0
    rental_property.address.geolocation.location.lat = 0
    rental_property.address.geolocation.location.lon = 0
    assert zap_restrictions.is_restricted(sale_property)
    assert zap_restrictions.is_restricted(rental_property)
    assert viva_real_restrictions.is_restricted(sale_property)
    assert viva_real_restrictions.is_restricted(rental_property)


def test_zap_rental_should_ignore_price_less_than_3500(zap_restrictions, rental_property):
    rental_property.pricing_info.price = '3499'
    assert zap_restrictions.is_restricted(rental_property)


def test_zap_sale_should_ignore_price_less_than_600000(zap_restrictions, sale_property):
    sale_property.pricing_info.price = '599999'
    assert zap_restrictions.is_restricted(sale_property)


def test_zap_sale_should_ignore_zero_usable_area(zap_restrictions, sale_property):
    sale_property.usable_areas = 0
    assert zap_restrictions.is_restricted(sale_property)


def test_zap_sale_should_ignore_usable_area_price_less_or_equal_3500(zap_restrictions, sale_property):
    sale_property.usable_areas = 172
    sale_property.pricing_info.price = '600000'
    assert zap_restrictions.is_restricted(sale_property)


def test_zap_sale_should_decrease_min_price_if_in_zap_bounds(zap_restrictions, sale_property):
    sale_property.address.geolocation.location.lat = -23.552211
    sale_property.address.geolocation.location.lon = -46.652211
    sale_property.pricing_info.price = '539999'
    assert zap_restrictions.is_restricted(sale_property)


def test_zap_valid_sale_and_rental_properties(zap_restrictions, sale_property, rental_property):
    rental_property.pricing_info.price = '3500'
    assert not zap_restrictions.is_restricted(rental_property)

    sale_property.pricing_info.price = '600000'
    assert not zap_restrictions.is_restricted(sale_property)


def test_viva_real_rental_should_ignore_price_bigger_than_4000(viva_real_restrictions, rental_property):
    rental_property.pricing_info.price = '4001'
    assert viva_real_restrictions.is_restricted(rental_property)


def test_viva_real_sale_should_ignore_price_bigger_than_700000(viva_real_restrictions, sale_property):
    sale_property.pricing_info.price = '700001'
    assert viva_real_restrictions.is_restricted(sale_property)


def test_viva_real_rental_should_ignore_zero_or_none_monthly_condo_fee(viva_real_restrictions, rental_property):
    rental_property.pricing_info.monthly_condo_fee = '0'
    assert viva_real_restrictions.is_restricted(rental_property)

    rental_property.pricing_info.monthly_condo_fee = None
    assert viva_real_restrictions.is_restricted(rental_property)


def test_viva_real_rental_should_ignore_condo_fee_30_p_bigger_than_price(viva_real_restrictions, rental_property):
    rental_property.pricing_info.monthly_condo_fee = '661'
    assert viva_real_restrictions.is_restricted(rental_property)


def test_viva_real_rental_should_increase_condo_fee_tolerance_if_in_zap_bounds(viva_real_restrictions, rental_property):
    rental_property.address.geolocation.location.lat = -23.552211
    rental_property.address.geolocation.location.lon = -46.652211
    rental_property.pricing_info.monthly_condo_fee = '989'
    assert not viva_real_restrictions.is_restricted(rental_property)

    rental_property.pricing_info.monthly_condo_fee = '990'
    assert viva_real_restrictions.is_restricted(rental_property)


def test_base_restrictions_no_effect_at_sale_and_rental(base_restrictions, sale_property, rental_property):
    assert not base_restrictions.is_restricted(sale_property)
    assert not base_restrictions.is_restricted(rental_property)


def test_zap_portal(zap_portal):
    items = zap_portal.load_filters([], 1, 5)
    assert len(items) == 2


def test_viva_real_portal(viva_real_portal):
    items = viva_real_portal.load_filters([], 1, 100)
    assert len(items) == 2
