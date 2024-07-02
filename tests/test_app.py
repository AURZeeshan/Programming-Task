import pytest
import requests

@pytest.fixture
def api_url():
    return 'http://localhost:5000'  # Update with your Flask app URL

def test_add_visitor(api_url):
    data = {'name': 'John Doe'}
    response = requests.post(f'{api_url}/add_visitor', json=data)
    assert response.status_code == 201
    assert response.json()['message'] == 'Visitor added successfully.'

def test_get_visitors(api_url):
    response = requests.get(f'{api_url}/get_visitors')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

if __name__ == '__main__':
    pytest.main()
