import json
import unittest

from app import app

class FlaskAppTests(unittest.TestCase):

    def setUp(self):

        self.client = app.test_client()

        self.client.testing = True

    def test_home_page(self):

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

    def test_add_task(self):

        response = self.client.post(
            "/",
            data={"task": "Test task"},
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            b"Test task",
            response.data
        )

if __name__ == "__main__":
    unittest.main()