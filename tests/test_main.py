"""
Tests main page files
"""


def test_home(client):
    """
    Test home page texts after response
    """

    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>Home Page</title>" in response.data
