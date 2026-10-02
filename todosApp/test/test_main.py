from fastapi.testclient import TestClient
import main
from fastapi import status


client = TestClient(main.app)


def test_main_health():
    response = client.get('/healthy')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'Healthy'}  # the response must be the same as {'status': 'Healthy'}

