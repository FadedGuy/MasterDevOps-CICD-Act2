import http.client
import os
import unittest
from urllib.request import urlopen, Request
import json
import pytest

BASE_URL = os.environ.get("BASE_URL")
DEFAULT_TIMEOUT = 2  # in secs


@pytest.mark.api
class TestApi(unittest.TestCase):

    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")
        self.validUser = "user1"
        self.invalidUser = "user2"

    def test_api_add_success(self):
        url = f"{BASE_URL}/calc/add/2/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )

    def test_api_add_failure(self):
        url = f"{BASE_URL}/calc/add/2/a"
        try:
            urlopen(url, timeout=DEFAULT_TIMEOUT)
            pytest.fail("Expected HTTP 400 error but request succeeded")
        except Exception as e:
            self.assertEqual(e.code, http.client.BAD_REQUEST)

    def test_api_substract_success(self):
        url = f"{BASE_URL}/calc/substract/5/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )

    def test_api_substract_failure(self):
        url = f"{BASE_URL}/calc/substract/2/a"
        try:
            urlopen(url, timeout=DEFAULT_TIMEOUT)
        except Exception as e:
            self.assertEqual(e.code, http.client.BAD_REQUEST)

    def test_api_multiply_success(self):
        url = f"{BASE_URL}/calc/multiply/{self.validUser}/2/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )

    def test_api_multiply_failure(self):
        url = f"{BASE_URL}/calc/multiply/{self.validUser}/2/a"
        try:
            urlopen(url, timeout=DEFAULT_TIMEOUT)
        except Exception as e:
            self.assertEqual(e.code, http.client.BAD_REQUEST)

    def test_api_multiply_auth_failure(self):
        url = f"{BASE_URL}/calc/multiply/{self.invalidUser}/2/2"
        try:
            urlopen(url, timeout=DEFAULT_TIMEOUT)
        except Exception as e:
            self.assertEqual(e.code, http.client.UNAUTHORIZED)

    def test_api_divide_success(self):
        url = f"{BASE_URL}/calc/divide/10/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )

    def test_api_divide_failure(self):
        url = f"{BASE_URL}/calc/divide/10/0"
        try:
            urlopen(url, timeout=DEFAULT_TIMEOUT)
        except Exception as e:
            self.assertEqual(e.code, http.client.BAD_REQUEST)

    def test_api_power_success(self):
        url = f"{BASE_URL}/calc/power/2/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )

    def test_api_power_failure(self):
        url = f"{BASE_URL}/calc/power/2/a"
        try:
            urlopen(url, timeout=DEFAULT_TIMEOUT)
        except Exception as e:
            self.assertEqual(e.code, http.client.BAD_REQUEST)

    def test_api_sqrt_success(self):
        url = f"{BASE_URL}/calc/sqrt/9"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
    
    def test_api_sqrt_failure(self):
        url = f"{BASE_URL}/calc/sqrt/-9"
        try:
            urlopen(url, timeout=DEFAULT_TIMEOUT)
        except Exception as e:
            self.assertEqual(e.code, http.client.BAD_REQUEST)

    def test_api_log10_success(self):
        url = f"{BASE_URL}/calc/log10/100"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )

    def test_api_log10_failure(self):
        url = f"{BASE_URL}/calc/log10/0"
        try:
            urlopen(url, timeout=DEFAULT_TIMEOUT)
        except Exception as e:
            self.assertEqual(e.code, http.client.BAD_REQUEST)