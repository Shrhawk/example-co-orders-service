import datetime

import pytest

from src.exampleco.exampleco.constants import (
    OK_STATUS_CODE,
    BAD_REQUEST_STATUS_CODE,
    CREATED_STATUS_CODE,
    UNPROCESSABLE_ENTITY_STATUS_CODE,
    UPDATE_STATUS_CODE,
    NOT_FOUND_STATUS_CODE
)
from src.exampleco.exampleco.models.database import Session
from src.exampleco.exampleco.models.database.order_items import OrderItems
from src.exampleco.exampleco.models.database.orders import Order
from src.exampleco.exampleco.models.database.services import Service
from src.exampleco.exampleco.tests.conftest import TestCase


class TestOrders(TestCase):
    """
    Tests for Orders Apis
    """

    @pytest.mark.run(order=27)
    def test_get_orders_without_any_data_in_db(self):
        """
        Test GET Orders without Any data in database
        """
        response = self.client.get(self.base_url + "/orders")
        response_data = response.json()
        assert response.status_code == OK_STATUS_CODE
        assert not response_data

    @pytest.mark.run(order=7)
    def test_get_orders_with_one_data_in_db(self):
        """
        Test GET Orders with One data in database
        """
        response = self.client.get(self.base_url + "/orders")
        response_data = response.json()
        assert response.status_code == OK_STATUS_CODE
        assert len(response_data) >= 1
        assert response_data[0]["name"] == "Order order_this_week"  # noqa
        assert response_data[0]["description"] == "Order Description 2"
        assert response_data[0]["price"] == 20

    @pytest.mark.run(order=8)
    def test_get_orders_with_more_than_one_data_in_db(self):
        """
        Test GET Orders with more than one data in database
        """
        response = self.client.get(self.base_url + "/orders")
        response_data = response.json()
        assert response.status_code == OK_STATUS_CODE
        assert len(response_data) >= 2
        assert response_data[0]["name"] == "Order order_this_week"  # noqa
        assert response_data[0]["description"] == "Order Description 2"
        assert response_data[0]["price"] == 20
        assert response_data[1]["name"] == "Order order_this_week2"
        assert response_data[1]["description"] == "Order Description 3"
        assert response_data[1]["price"] == 20
        assert response_data[1]["order_items"][0]["name"] == "Order Item 6"
        assert response_data[1]["order_items"][0]["description"] == "Order Item Description 6"
        assert response_data[1]["order_items"][0]["price"] == 10

    @pytest.mark.run(order=9)
    def test_get_order_by_id_without_any_data_in_db(self):
        """
        Test GET Orders without Any data in database
        """
        
        response = self.client.get(self.base_url + "/orders/" + str(1))
        response_data = response.json()
        assert response.status_code == NOT_FOUND_STATUS_CODE
        assert response_data == {'message': 'Order not found'}

    @pytest.mark.run(order=10)
    def test_get_order_by_id_with_valid_id(self):
        """
        Test GET Orders with data in database
        """
        order = Session.query(Order).filter(Order.price == 100).first()
        response = self.client.get(self.base_url + "/orders/" + str(order.id + 1))
        response_data = response.json()
        assert response.status_code == OK_STATUS_CODE
        assert response_data["name"] == "Order 2"
        assert response_data["description"] == "Order Description 2"
        assert response_data["price"] == 20
        assert response_data["order_items"][0]["name"] == "Order Item 3"
        assert response_data["order_items"][0]["description"] == "Order Item Description"
        assert response_data["order_items"][0]["price"] == 10

    @pytest.mark.run(order=11)
    def test_get_order_by_id_with_invalid_id(self):
        """
        Test GET Orders with invalid order id
        """
        response = self.client.get(self.base_url + "/orders/" + str(99999))
        response_data = response.json()
        assert response.status_code == NOT_FOUND_STATUS_CODE
        assert response_data == {"message": "Order not found"}

    @pytest.mark.run(order=12)
    def test_get_order_by_id_with_non_digit_order_id(self):
        """
        Test GET Orders with non-digit order id
        """
        response = self.client.get(self.base_url + "/orders/" + "nondigit")
        response_data = response.json()
        assert response.status_code == BAD_REQUEST_STATUS_CODE
        assert response_data == {"message": "order_id is required with valid integer"}

    @pytest.mark.run(order=13)
    def test_create_order_with_valid_data(self):
        """
        Test POST Orders with valid data in payload
        """
        service = Session.query(Service).first()
        json_data = {
            "name": "hello",
            "price": 10,
            "order_items": [
                {
                    "service_id": service.id,
                    "name": "hello",
                    "price": 10
                }
            ]
        }
        response = self.client.post(self.base_url + "/orders", json=json_data)
        response_data = response.json()
        assert response.status_code == CREATED_STATUS_CODE
        assert response_data
        assert response_data["name"] == json_data["name"]
        assert response_data.get("description") == json_data.get("description")
        assert response_data["price"] == json_data["price"]
        assert response_data["order_items"][0]["name"] == json_data["order_items"][0]["name"]
        assert response_data["order_items"][0].get("description") == json_data["order_items"][0].get("description")
        assert response_data["order_items"][0]["price"] == json_data["order_items"][0]["price"]

    @pytest.mark.run(order=14)
    def test_create_order_without_data(self):
        """
        Test POST Orders without data in payload
        """
        response = self.client.post(self.base_url + "/orders", json={})
        response_data = response.json()
        assert response.status_code == UNPROCESSABLE_ENTITY_STATUS_CODE
        assert response_data == {
            'name': ['Missing data for required field.'],
            'order_items': ['Missing data for required field.'],
            'price': ['Missing data for required field.']
        }

    @pytest.mark.run(order=15)
    def test_create_order_without_order_items(self):
        """
        Test POST Orders without order_items in payload
        """
        json_data = {
            "name": "hello",
            "price": 10
        }
        response = self.client.post(self.base_url + "/orders", json=json_data)
        response_data = response.json()
        assert response.status_code == UNPROCESSABLE_ENTITY_STATUS_CODE
        assert response_data == {
            'order_items': ['Missing data for required field.']
        }

        json_data = {
            "name": "hello",
            "price": 10,
            "order_items": []
        }
        response = self.client.post(self.base_url + "/orders", json=json_data)
        response_data = response.json()
        assert response.status_code == UNPROCESSABLE_ENTITY_STATUS_CODE
        assert response_data == {'message': 'order_items is mandatory'}

        json_data = {
            "name": "hello",
            "price": 10,
            "order_items": [{}]
        }
        response = self.client.post(self.base_url + "/orders", json=json_data)
        response_data = response.json()
        assert response.status_code == UNPROCESSABLE_ENTITY_STATUS_CODE
        assert response_data == {
            'order_items': {
                '0': {
                    'price': ['Missing data for required field.'],
                    'service_id': ['Missing data for required field.'],
                    'name': ['Missing data for required field.']
                }
            }
        }

    @pytest.mark.run(order=16)
    def test_create_order_with_invalid_service_id(self):
        """
        Test POST Orders with invalid service id in payload
        """
        service = Session.query(Service).first()
        json_data = {
            "name": "hello",
            "price": 10,
            "order_items": [
                {
                    "service_id": service.id,
                    "name": "hello",
                    "price": 10
                },
                {
                    "service_id": service.id + 99,
                    "name": "hello 2",
                    "price": 20
                }
            ]
        }
        response = self.client.post(self.base_url + "/orders", json=json_data)
        response_data = response.json()
        assert response.status_code == UNPROCESSABLE_ENTITY_STATUS_CODE
        assert response_data == {
            'order_items': {'1': {'service_id': ['Service Id is invalid']}}
        }

    @pytest.mark.run(order=17)
    def test_update_order_with_valid_data(self):
        """
        Test PUT Orders with valid data in payload
        """
        order = Session.query(Order).filter(Order.price == 100).first()
        service = Session.query(Service).first()
        order_item = order.order_items[0]
        order_item2 = order.order_items[1]
        json_data = {
            "id": order.id,
            "name": "hello",
            "price": 10,
            "order_items": [
                {
                    "id": order_item.id,
                    "service_id": service.id,
                    "name": "hello",
                    "price": 10
                },
                {
                    "id": order_item2.id,
                    "service_id": service.id,
                    "name": "hello 2",
                    "price": 20
                }
            ]
        }
        Session.expire_all()
        response = self.client.put(self.base_url + "/orders", json=json_data)
        assert response.status_code == CREATED_STATUS_CODE
        Session.refresh(order)
        order_ = Session.query(Order).filter(Order.id == order.id).first()
        assert order_
        assert len(order_.order_items) == 2

    @pytest.mark.run(order=18)
    def test_put_order_with_invalid_service_id(self):
        """
        Test PUT Orders with invalid service id in payload
        """
        order = Session.query(Order).filter(Order.price == 100).first()
        service = Session.query(Service).first()
        order_item = order.order_items[0]
        order_item2 = order.order_items[1]
        json_data = {
            "id": order.id,
            "name": "hello",
            "price": 10,
            "order_items": [
                {
                    "id": order_item.id,
                    "service_id": service.id,
                    "name": "hello",
                    "price": 10
                },
                {
                    "id": order_item2.id,
                    "service_id": service.id,
                    "name": "hello 2",
                    "price": 20
                },
                {
                    "service_id": service.id + 999,
                    "name": "hello New",
                    "price": 30
                }
            ]
        }
        Session.expire_all()
        response = self.client.put(self.base_url + "/orders", json=json_data)
        response_data = response.json()
        assert response.status_code == UNPROCESSABLE_ENTITY_STATUS_CODE
        assert response_data == {
            'order_items': {'2': {'service_id': ['Service Id is invalid']}}
        }

    @pytest.mark.run(order=19)
    def test_delete_order_by_id_with_invalid_id(self):
        """
        Test DELETE Orders with invalid id
        """
        response = self.client.delete(self.base_url + "/orders/" + str(999999))
        assert response.status_code == NOT_FOUND_STATUS_CODE

    @pytest.mark.run(order=20)
    def test_delete_order_by_id_with_nondigit_id(self):
        """
        Test DELETE Orders with invalid id
        """
        response = self.client.delete(self.base_url + "/orders/" + "hello")
        response_data = response.json()
        assert response.status_code == BAD_REQUEST_STATUS_CODE
        assert response_data == {"message": "order_id is required with valid integer"}

    @pytest.mark.run(order=21)
    def test_delete_order_by_id_without_id(self):
        """
        Test DELETE Orders without id
        """
        response = self.client.delete(self.base_url + "/orders/")
        assert response.status_code == NOT_FOUND_STATUS_CODE

    @pytest.mark.run(order=22)
    def test_get_order_analytics_by_year(self):
        """
        Test GET Orders analytics by year
        """
        response = self.client.get(self.base_url + "/orders-analytics", params={"time_period": "THIS_YEAR"})
        response_data = response.json()
        assert response.status_code == OK_STATUS_CODE
        assert response_data == [[1, 1], [2, 1], [datetime.datetime.now().month, 1]]

    @pytest.mark.run(order=23)
    def test_get_order_analytics_by_month(self):
        """
        Test GET Orders analytics by month
        """
        response = self.client.get(self.base_url + "/orders-analytics", params={"time_period": "THIS_MONTH"})
        response_data = response.json()
        assert response.status_code == OK_STATUS_CODE
        assert response_data == [[3, 1], [7, 1], [datetime.datetime.now().day, 1], [datetime.datetime.now().day+1, 1]]

    @pytest.mark.run(order=24)
    def test_get_order_analytics_by_week(self):
        """
        Test GET Orders analytics by week
        """
        response = self.client.get(self.base_url + "/orders-analytics", params={"time_period": "THIS_WEEK"})
        response_data = response.json()
        assert response.status_code == OK_STATUS_CODE
        assert response_data == [[datetime.datetime.now().day, 1], [datetime.datetime.now().day + 1, 1]]

    @pytest.mark.run(order=25)
    def test_get_order_analytics_with_invalid_time_period(self):
        """
        Test GET Orders analytics invalid time period
        """
        response = self.client.get(self.base_url + "/orders-analytics", params={"time_period": "INVALID"})
        response_data = response.json()
        assert response.status_code == BAD_REQUEST_STATUS_CODE
        assert response_data == {'message': 'time_period is required with valid string'}

    @pytest.mark.run(order=26)
    def test_delete_order_by_id(self):
        """
        Test DELETE Orders with id
        """
        order = Session.query(Order).first()
        response = self.client.delete(self.base_url + "/orders/" + str(order.id))
        assert response.status_code == UPDATE_STATUS_CODE
