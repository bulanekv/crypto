import unittest

from fastapi.testclient import TestClient

from app.api.api_v1.models.currency_init import create_table, remove_table
from app.main import app

client = TestClient(app)


class CurrencyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        create_table()

    @classmethod
    def tearDownClass(cls):
        remove_table()

    def tearDown(self):
        remove_table()
        create_table()

    def test_get_currency_empty(self):
        response = client.get(
            "/api/v1/currencies/bitcoin",
        )
        assert response.status_code == 404
        assert response.json().get("detail") == "Currency not found"

    def test_get_currencies_empty(self):
        response = client.get(
            "/api/v1/currencies",
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

    def test_delete_currency_empty(self):
        response = client.delete(
            "/api/v1/currencies/bitcoin",
        )
        assert response.status_code == 404
        assert response.json().get("detail") == "Currency not found"

    def test_create_currency(self) -> None:
        data = {
            "id": "bitcoin",
        }
        response = client.post(
            "/api/v1/currencies/",
            json=data,
        )
        assert response.status_code == 201

        response = client.get(
            "/api/v1/currencies/bitcoin",
        )
        assert response.status_code == 200
        assert response.json().get("id") == "bitcoin"
        assert response.json().get("symbol") == "btc"
        assert response.json().get("meta") not in [None, ""]

    def test_create_currency_twice(self):
        data = {
            "id": "bitcoin",
        }
        response = client.post(
            "/api/v1/currencies/",
            json=data,
        )
        assert response.status_code == 201
        data = {
            "id": "bitcoin",
        }
        response = client.post(
            "/api/v1/currencies/",
            json=data,
        )
        assert response.status_code == 409

    def test_get_currency(self):
        data = {
            "id": "solana",
        }
        response = client.post(
            "/api/v1/currencies/",
            json=data,
        )
        assert response.status_code == 201
        response = client.get(
            "/api/v1/currencies/solana",
        )
        assert response.status_code == 200
        assert response.json().get("id") == "solana"
        assert response.json().get("symbol") == "sol"
        assert response.json().get("meta") not in [None, ""]

    def test_get_currencies(self):
        data = {
            "id": "bitcoin",
        }
        response = client.post(
            "/api/v1/currencies/",
            json=data,
        )
        assert response.status_code == 201
        data = {
            "id": "solana",
        }
        response = client.post(
            "/api/v1/currencies/",
            json=data,
        )
        assert response.status_code == 201

        response = client.get(
            "/api/v1/currencies",
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0].get("id") == "bitcoin"
        assert data[0].get("name") == "Bitcoin"
        assert data[0].get("symbol") == "btc"
        assert data[0].get("meta") not in [None, ""]
        assert data[1].get("id") == "solana"
        assert data[1].get("name") == "Solana"
        assert data[1].get("symbol") == "sol"
        assert data[1].get("meta") not in [None, ""]

    def test_delete_currency(self):
        data = {
            "id": "bitcoin",
        }
        response = client.post(
            "/api/v1/currencies/",
            json=data,
        )
        assert response.status_code == 201
        response = client.delete(
            "/api/v1/currencies/bitcoin",
        )
        assert response.status_code == 200
        response = client.get(
            "/api/v1/currencies",
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0


if __name__ == "__main__":
    unittest.main()
