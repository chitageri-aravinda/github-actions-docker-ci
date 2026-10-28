import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import HTTPServer

from app.main import Handler, greeting


class GreetingTests(unittest.TestCase):
    def test_default(self):
        self.assertEqual(greeting(), "Hello, world!")

    def test_name(self):
        self.assertEqual(greeting("Aravinda"), "Hello, Aravinda!")

    def test_blank_name_falls_back(self):
        self.assertEqual(greeting("   "), "Hello, world!")


class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), Handler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def get(self, path):
        return urllib.request.urlopen(f"http://127.0.0.1:{self.port}{path}")

    def test_health(self):
        with self.get("/health") as resp:
            self.assertEqual(resp.status, 200)
            self.assertEqual(json.load(resp), {"status": "ok"})

    def test_root(self):
        with self.get("/") as resp:
            self.assertEqual(json.load(resp), {"message": "Hello, world!"})

    def test_not_found(self):
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            self.get("/missing")
        self.assertEqual(ctx.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
