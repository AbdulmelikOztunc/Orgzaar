"""
Pytest configuration ve fixtures
"""

import pytest
from app import create_app


@pytest.fixture
def app():
    """Flask uygulama fixture'ı"""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Test client fixture'ı"""
    return app.test_client()

