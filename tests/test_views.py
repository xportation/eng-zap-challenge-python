import pytest
from fastapi.testclient import TestClient

from portal_api import application

app = application.create_app()


@pytest.fixture
def client():
    return TestClient(app)


def test_zap_empty_response(client):
    response = client.get('/api/properties/zap')
    assert response.status_code == 200


def test_viva_real_empty_response(client):
    response = client.get('/api/properties/viva-real')
    assert response.status_code == 200
