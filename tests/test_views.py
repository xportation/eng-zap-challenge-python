import pytest
from fastapi.testclient import TestClient

from portal_api import application

app = application.create_app()


@pytest.fixture
def client():
    return TestClient(app)


def test_empty_response(client):
    response = client.get('/api/properties')
    assert response.status_code == 200
