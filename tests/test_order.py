import sys
import os
import pytest


@pytest.fixture

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    return response