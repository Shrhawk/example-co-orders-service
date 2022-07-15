import datetime
from typing import Union

import pytest
import requests

from src.exampleco.exampleco.database import get_session
from src.exampleco.exampleco.models import OrderItems, Order, Service


class TestCase(object):
    """
    Python api test client
    :return:
    """
    client = requests
    base_url = "http://0.0.0.0:8080"


Session = get_session()


@pytest.fixture(scope="function")
def create_test_records():
    """
    create 3 new services, order-items and orders
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
    order = Order(  # noqa
        name="Order 1",
        description="Order Description",
        price=100,
        created_on=datetime.datetime.now().replace(year=2022, month=1)
    )
    order_item = OrderItems(
        name="Order Item 1",
        description="Order Item Description",
        price=10,
        order=order,
        service=service
    )
    order_item2 = OrderItems(
        name="Order Item 2",
        description="Order Item Description 2",
        price=10,
        order=order,
        service=service
    )
    order.order_items = [order_item, order_item2]
    order2 = Order(
        name="Order 2",
        description="Order Description 2",
        price=20,
        created_on=datetime.datetime.now().replace(year=2022, month=2)
    )
    order_item3 = OrderItems(
        name="Order Item 3",
        description="Order Item Description",
        price=10,
        order=order2,
        service=service
    )
    order_item4 = OrderItems(
        name="Order Item 4",
        description="Order Item Description",
        price=10,
        order=order2,
        service=service
    )
    order2.order_items = [order_item3, order_item4]
    order3 = Order(
        name="Order 3",
        description="Order Description 3",
        price=20,
        created_on=datetime.datetime.now().replace(year=2021)
    )
    order_item5 = OrderItems(
        name="Order Item 5",
        description="Order Item Description",
        price=10,
        order=order3,
        service=service
    )
    order_item6 = OrderItems(
        name="Order Item 6",
        description="Order Item Description",
        price=10,
        order=order3,
        service=service
    )
    order3.order_items = [order_item5, order_item6]
    order_this_month = Order(  # noqa
        name="Order order_this_month",
        description="Order Description",
        price=10,
        created_on=datetime.datetime.now().replace(day=3)
    )
    order_this_month2 = Order(  # noqa
        name="Order order_this_month2",
        description="Order Description",
        price=10,
        created_on=datetime.datetime.now().replace(day=7)
    )
    order_this_week = Order(
        name="Order order_this_week",
        description="Order Description 2",
        price=20,
        created_on=datetime.datetime.now()
    )
    order_this_week2 = Order(
        name="Order order_this_week2",
        description="Order Description 3",
        price=20,
        created_on=datetime.datetime.now().replace(day=datetime.datetime.now().day + 1)
    )
    order_item6 = OrderItems(
        name="Order Item 6",
        description="Order Item Description 6",
        price=10,
        order=order_this_week2,
        service=service
    )
    order_this_week2.order_items = [order_item6]
    Session.add(order_this_week)
    Session.add(order_this_week2)
    Session.add(order_this_month)
    Session.add(order_this_month2)
    Session.add(order)
    Session.add(order2)
    Session.add(order3)
    Session.add(service)
    Session.add(service2)
    Session.add(service3)
    Session.commit()


@pytest.fixture(scope="session", autouse=True)
def clear_db():
    """
    delete services, order-items and orders records
    Returns:

    """
    Session.query(OrderItems).delete()
    Session.query(Order).delete()
    Session.query(Service).delete()
    Session.commit()


def pytest_sessionfinish(session: "Session", exitstatus: Union[int, "ExitCode"]) -> None:
    """
    delete services, order-items and orders records after pytest session
    Returns:
    """
    Session.query(OrderItems).delete()
    Session.query(Order).delete()
    Session.query(Service).delete()
    Session.commit()
