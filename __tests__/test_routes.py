def test_index_route(client):
    """Test the root (/) route."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode() == "Welcome to my Flask App!"


def test_api_route(client):
    """Test the /api route."""
    response = client.get('/api')
    assert response.status_code == 200
    assert response.json == {"message": "This is the API endpoint", "status": "success"}


def test_hello_name_route(client):
    """Test the /hello/<name> route."""
    name = "Alice"
    response = client.get(f'/hello/{name}')
    assert response.status_code == 200
    assert response.data.decode() == f"Hello, {name.capitalize()}!"


def test_square_route(client):
    """Test the /square/<number> route."""
    number = 8
    expected_result = number * number
    response = client.get(f'/square/{number}')
    assert response.status_code == 200
    assert response.json == {"number": number, "square": expected_result}


def test_square_route_with_invalid_type(client):
    """Test the /square/<number> route with invalid input."""
    response = client.get('/square/string')
    assert response.status_code == 404  # Flask returns 404 for routes that don't match


def test_status_route(client):
    """Test the /status route."""
    response = client.get('/status')
    assert response.status_code == 200
    assert response.json == {"app": "Flask Sample App", "status": "OK"}
