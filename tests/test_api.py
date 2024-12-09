from fastapi.testclient import TestClient

from apollo.server import app


class TestAPI:
    def setup_method(self):
        self.client = TestClient(app)

    def test_answer(self, use_db):
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == []
