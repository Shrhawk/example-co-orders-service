import unittest

import requests


class TestCase(unittest.TestCase):
    """
    Python api test client
    :return:
    """
    client = requests
    base_url = "http://0.0.0.0:8080"
