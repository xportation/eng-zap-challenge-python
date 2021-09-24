from portal_api import filters, models, schemas


def test_business_type_filter(sale_property, rental_property):
    sale_filter = filters.BusinessTypeFilter(models.BusinessType.sale)
    assert sale_filter.is_allowed(sale_property)
    assert not sale_filter.is_allowed(rental_property)

    rental_filter = filters.BusinessTypeFilter(models.BusinessType.rental)
    assert rental_filter.is_allowed(rental_property)
    assert not rental_filter.is_allowed(sale_property)


def test_city_filter(sale_property):
    city_filter = filters.CityFilter('Florianópolis')
    assert not city_filter.is_allowed(sale_property)

    sale_property.address.city = 'Florianópolis'
    assert city_filter.is_allowed(sale_property)


def test_min_price_filter(rental_property):
    min_price_filter = filters.MinPriceFilter(2200)
    assert min_price_filter.is_allowed(rental_property)

    min_price_filter = filters.MinPriceFilter(2201)
    assert not min_price_filter.is_allowed(rental_property)


def test_max_price_filter(rental_property):
    max_price_filter = filters.MaxPriceFilter(2200)
    assert max_price_filter.is_allowed(rental_property)

    max_price_filter = filters.MaxPriceFilter(2199)
    assert not max_price_filter.is_allowed(rental_property)


def test_bedrooms_filter(sale_property):
    bedrooms_filter = filters.BedroomsFilter(2)
    assert bedrooms_filter.is_allowed(sale_property)

    sale_property.bedrooms = 3
    assert not bedrooms_filter.is_allowed(sale_property)


def test_bathrooms_filter(rental_property):
    bathrooms_filter = filters.BathroomsFilter(2)
    assert bathrooms_filter.is_allowed(rental_property)

    rental_property.bathrooms = 1
    assert not bathrooms_filter.is_allowed(rental_property)


def test_filters_factory(rental_property):
    filters_query = schemas.Filter()
    filters_query.bedrooms = 3
    filters_query.bathrooms = 2
    expected = [False, True]
    for i, f in enumerate(filters.filters_factory(filters_query)):
        assert f.is_allowed(rental_property) == expected[i]
