import unittest

import pytest
import requests

from src.exampleco.exampleco.models.database import Session
from src.exampleco.exampleco.models.database.order_items import OrderItems
from src.exampleco.exampleco.models.database.orders import Order
from src.exampleco.exampleco.models.database.services import Service


class TestCase(unittest.TestCase):
    """
    Python api test client
    :return:
    """
    client = requests
    base_url = "http://0.0.0.0:8080"


@pytest.fixture(scope="session", autouse=True)
def create_services():
    """
    delete previous services and create 3 new services
    Returns:

    """
    service = Service(
        name="Service 1",
        description="Service Description",
        price=10
    )
    service2 = Service(
        name="Service 2",
        description="Service Description 2",
        price=20
    )
    service3 = Service(
        name="Service 3",
        description="Service Description 3",
        price=30
    )
    Session.add(service)
    Session.add(service2)
    Session.add(service3)
    Session.commit()
