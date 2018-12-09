import pytest
from app import *

@pytest.fixture
def client():
    client = app.test_client()
    return client

def test_root(client):
    """Test the default route."""

    res = client.get('/')
    assert b'Hello World' in res.data
