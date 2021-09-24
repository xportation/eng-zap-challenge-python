from unittest import mock

import pytest
import responses
from fastapi.testclient import TestClient

from portal_api import application, config


@pytest.fixture
def server_app():
    return application.create_app()


@pytest.fixture
def client(server_app):
    return TestClient(server_app)


def test_zap_empty_response(client, server_app):
    mock_data_loader = mock.MagicMock()
    mock_data_loader.all.return_value = []

    with server_app.container.data_loader.override(mock_data_loader):
        response = client.get('/api/properties/zap')
        assert response.status_code == 200


def test_viva_real_empty_response(client, server_app):
    mock_data_loader = mock.MagicMock()
    mock_data_loader.all.return_value = []

    with server_app.container.data_loader.override(mock_data_loader):
        response = client.get('/api/properties/viva-real')
        assert response.status_code == 200


def test_not_found_url(client):
    response = client.get('/api/properties')
    assert response.status_code == 404


def test_viva_real_items_response(client, mock_data_json):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as mock_data_api:
        mock_data_api.add(responses.GET, config.data_url(), body=mock_data_json, content_type='application/json')
        response = client.get('/api/properties/viva-real')
        assert response.status_code == 200

        json_data = response.json()
        assert_json_response(json_data, 1, 10, 2, 2)


def test_zap_items_response(client, mock_data_json):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as mock_data_api:
        mock_data_api.add(responses.GET, config.data_url(), body=mock_data_json, content_type='application/json')
        response = client.get('/api/properties/zap')
        assert response.status_code == 200

        json_data = response.json()
        assert_json_response(json_data, 1, 10, 0, 0)


def assert_json_response(json_data, page_number, page_size, total_count, items_count):
    assert json_data
    assert json_data.get('pageNumber', 0) == page_number
    assert json_data.get('pageSize', 0) == page_size
    assert json_data.get('totalCount', 0) == total_count
    assert len(json_data.get('listings', [])) == items_count


def test_ignore_invalid_properties_from_data_api(client):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as mock_data_api:
        mock_data_api.add(responses.GET, config.data_url(),
                          body='[{"invalid": "yep"}]',
                          content_type='application/json')
        response = client.get('/api/properties/viva-real')
        assert response.status_code == 200

        json_data = response.json()
        assert_json_response(json_data, 1, 10, 0, 0)
