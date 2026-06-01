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

    def test_toggle_task(self):
        
        self.client.post(
            "/",
            data={"task": "Toggle test"},
            follow_redirects=True
        )

        with open("tasks.json", "r", encoding="utf-8") as file:
            tasks = json.load(file)

        task_id = len(tasks) - 1

        initial_status = tasks[task_id]["done"]

        response = self.client.get(
            f"/toggle/{task_id}",
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        with open("tasks.json", "r", encoding="utf-8") as file:
            tasks = json.load(file)

        self.assertEqual(
            tasks[task_id]["done"],
            not initial_status
        )

    def test_delete_task(self):
        self.client.post(
            "/",
            data={"task": "Delete test"},
            follow_redirects=True
        )

        with open("tasks.json", "r", encoding="utf-8") as file:
            tasks = json.load(file)

        task_id = len(tasks) - 1
        tasks_count = len(tasks)

        response = self.client.get(
            f"/delete/{task_id}",
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        with open("tasks.json", "r", encoding="utf-8") as file:
            tasks = json.load(file)

        self.assertEqual(
            len(tasks),
            tasks_count - 1
        )

    def test_tasks_file(self):

        with open("tasks.json", "r", encoding="utf-8") as file:

            tasks = json.load(file)

            self.assertIsInstance(tasks, list)

if __name__ == "__main__":
    unittest.main()