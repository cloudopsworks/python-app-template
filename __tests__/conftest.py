import pytest
from app import create_app

@pytest.fixture
def client():
    # Create the Flask app using the factory method
    app = create_app()
    app.config['TESTING'] = True  # Enable testing mode for the app

    # Provide the app's test client for making requests
    with app.test_client() as client:
        yield client