
def test_home_page_returns_404(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response status is 404
    """
    response = test_client.get('/')
    assert response.status_code == 404
