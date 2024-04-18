"""
Creating a fixture
"""
import pytest
from expirience import create_app


class NewConfig:
    """
    class to config 
    """
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI = "sqlite://"


@pytest.fixture()
def app():
    """
    app testing
    """
    app = create_app(NewConfig)  # create db in memory
    app.config['TESTING'] = True
    yield app


@pytest.fixture()
def client(app):
    """
    tests clients
    """
    return app.test_client()
