from django.test import SimpleTestCase


class HelloApiTests(SimpleTestCase):
    def test_hello_endpoint_returns_success_payload(self):
        response = self.client.get("/qlmvt/hello/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("application/json", response["Content-Type"])
        self.assertEqual(
            response.json(),
            {
                "message": "Django API đang hoạt động!",
                "database": "QuanLyMangVienThong",
            },
        )

    def test_hello_endpoint_contains_expected_message(self):
        response = self.client.get("/qlmvt/hello/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Django API đang hoạt động!")
