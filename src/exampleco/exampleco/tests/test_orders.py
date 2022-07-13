from src.exampleco.exampleco.constants import OK_STATUS_CODE, BAD_REQUEST_STATUS_CODE, CREATED_STATUS_CODE, \
    UNPROCESSABLE_ENTITY_STATUS_CODE, UPDATE_STATUS_CODE, NOT_FOUND_STATUS_CODE
from src.exampleco.exampleco.models.database import Session
from src.exampleco.exampleco.models.database.order_items import OrderItems
from src.exampleco.exampleco.models.database.orders import Order
from src.exampleco.exampleco.models.database.services import Service
from src.exampleco.exampleco.tests.conftest import TestCase


class TestOrders(TestCase):
    """
    Tests for Orders Apis
    """

    def test_get_orders_without_any_data_in_db(self):
        """
        Test GET Orders without Any data in database
        """
        response = self.client.get(self.base_url + "/orders")
        response_data = response.json()
        assert response.status_code == OK_STATUS_CODE
        assert not response_data

    def test_get_orders_with_one_data_in_db(self):
        """
        Test GET Orders with One data in database
        """
        order = Order(
            name="Order 1",
            description="Order Description",
            price=10
        )
        service = Service(
            name="Service 1",
            description="Service Description",
            price=10
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
        Session.add(service)
        Session.add(order)
        Session.commit()
        response = self.client.get(self.base_url + "/orders")
        response_data = response.json()
        assert response.status_code == OK_STATUS_CODE
        assert len(response_data) == 1
        assert response_data[0]["name"] == "Order 1"  # noqa
        assert response_data[0]["description"] == "Order Description"
        assert response_data[0]["price"] == 10
        assert response_data[0]["order_items"][0]["name"] == "Order Item 1"
        assert response_data[0]["order_items"][0]["description"] == "Order Item Description"
        assert response_data[0]["order_items"][0]["price"] == 10
        assert response_data[0]["order_items"][1]["name"] == "Order Item 2"
        assert response_data[0]["order_items"][1]["description"] == "Order Item Description 2"
        assert response_data[0]["order_items"][1]["price"] == 10
        Session.query(OrderItems).filter(OrderItems.order_id == order.id).delete(synchronize_session=False)
        Session.query(Order).filter(Order.id == order.id).delete(synchronize_session=False)
        Session.query(Service).filter(Service.id == service.id).delete(synchronize_session=False)
        Session.commit()

    def test_get_orders_with_more_than_one_data_in_db(self):
        """
        Test GET Orders with more than one data in database
        """
        order = Order(  # noqa
            name="Order 1",
            description="Order Description",
            price=10
        )
        service = Service(
            name="Service 1",
            description="Service Description",
            price=10
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
        Session.add(service)
        Session.add(order)
        order2 = Order(
            name="Order 2",
            description="Order Description 2",
            price=20
        )
        order_item3 = OrderItems(
            name="Order Item 3",
            description="Order Item Description",
            price=10,
            order=order2,
            service=service
        )
        order2.order_items = [order_item3]
        Session.add(order2)
        Session.commit()
        response = self.client.get(self.base_url + "/orders")
        response_data = response.json()
        assert response.status_code == OK_STATUS_CODE
        assert len(response_data) == 2
        assert response_data[0]["name"] == "Order 1"  # noqa
        assert response_data[0]["description"] == "Order Description"
        assert response_data[0]["price"] == 10
        assert response_data[0]["order_items"][0]["name"] == "Order Item 1"
        assert response_data[0]["order_items"][0]["description"] == "Order Item Description"
        assert response_data[0]["order_items"][0]["price"] == 10
        assert response_data[0]["order_items"][1]["name"] == "Order Item 2"
        assert response_data[0]["order_items"][1]["description"] == "Order Item Description 2"
        assert response_data[0]["order_items"][1]["price"] == 10
        assert response_data[1]["name"] == "Order 2"
        assert response_data[1]["description"] == "Order Description 2"
        assert response_data[1]["price"] == 20
        assert response_data[1]["order_items"][0]["name"] == "Order Item 3"
        assert response_data[1]["order_items"][0]["description"] == "Order Item Description"
        assert response_data[1]["order_items"][0]["price"] == 10
        Session.query(OrderItems).filter(OrderItems.order_id.in_([order.id, order2.id])).delete(synchronize_session=False)
        Session.query(Order).filter(Order.id.in_([order.id, order2.id])).delete(synchronize_session=False)
        Session.query(Service).filter(Service.id == service.id).delete(synchronize_session=False)
        Session.commit()

    def test_get_order_by_id_without_any_data_in_db(self):
        """
        Test GET Orders without Any data in database
        """
        
        response = self.client.get(self.base_url + "/orders/" + str(1))
        response_data = response.json()
        assert response.status_code == NOT_FOUND_STATUS_CODE
        assert not response_data

    def test_get_order_by_id_with_valid_id(self):
        """
        Test GET Orders without Any data in database
        """
        order = Order(  # noqa
            name="Order 1",
            description="Order Description",
            price=10
        )
        service = Service(
            name="Service 1",
            description="Service Description",
            price=10
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
        Session.add(service)
        Session.add(order)
        order2 = Order(
            name="Order 2",
            description="Order Description 2",
            price=20
        )
        order_item3 = OrderItems(
            name="Order Item 3",
            description="Order Item Description",
            price=10,
            order=order2,
            service=service
        )
        order2.order_items = [order_item3]
        Session.add(order2)
        Session.commit()
        response = self.client.get(self.base_url + "/orders/" + str(order2.id))
        response_data = response.json()
        assert response.status_code == OK_STATUS_CODE
        assert response_data["name"] == "Order 2"
        assert response_data["description"] == "Order Description 2"
        assert response_data["price"] == 20
        assert response_data["order_items"][0]["name"] == "Order Item 3"
        assert response_data["order_items"][0]["description"] == "Order Item Description"
        assert response_data["order_items"][0]["price"] == 10
        Session.query(OrderItems).filter(OrderItems.order_id.in_([order.id, order2.id])).delete(synchronize_session=False)
        Session.query(Order).filter(Order.id.in_([order.id, order2.id])).delete(synchronize_session=False)
        Session.query(Service).filter(Service.id == service.id).delete(synchronize_session=False)
        Session.commit()

    def test_get_order_by_id_with_invalid_id(self):
        """
        Test GET Orders with invalid order id
        """
        order2 = Order(
            name="Order 2",
            description="Order Description 2",
            price=20
        )
        service = Service(
            name="Service 1",
            description="Service Description",
            price=10
        )
        order_item3 = OrderItems(
            name="Order Item 3",
            description="Order Item Description",
            price=10,
            order=order2,
            service=service
        )
        order2.order_items = [order_item3]
        Session.add(service)
        Session.add(order2)
        Session.commit()
        response = self.client.get(self.base_url + "/orders/" + str(99999))
        response_data = response.json()
        assert response.status_code == NOT_FOUND_STATUS_CODE
        assert response_data == {"message": "Order not found"}
        Session.query(OrderItems).filter(OrderItems.order_id.in_([order2.id])).delete(synchronize_session=False)
        Session.query(Order).filter(Order.id.in_([order2.id])).delete(synchronize_session=False)
        Session.query(Service).filter(Service.id == service.id).delete(synchronize_session=False)
        Session.commit()

    def test_get_order_by_id_with_non_digit_order_id(self):
        """
        Test GET Orders with non-digit order id
        """
        order2 = Order(
            name="Order 2",
            description="Order Description 2",
            price=20
        )
        service = Service(
            name="Service 1",
            description="Service Description",
            price=10
        )
        order_item3 = OrderItems(
            name="Order Item 3",
            description="Order Item Description",
            price=10,
            order=order2,
            service=service
        )
        order2.order_items = [order_item3]
        Session.add(service)
        Session.add(order2)
        Session.commit()
        response = self.client.get(self.base_url + "/orders/" + "nondigit")
        response_data = response.json()
        assert response.status_code == BAD_REQUEST_STATUS_CODE
        assert response_data == {"message": "order_id is required with valid integer"}
        Session.query(OrderItems).filter(OrderItems.order_id.in_([order2.id])).delete(synchronize_session=False)
        Session.query(Order).filter(Order.id.in_([order2.id])).delete(synchronize_session=False)
        Session.query(Service).filter(Service.id == service.id).delete(synchronize_session=False)
        Session.commit()

    def test_create_order_with_valid_data(self):
        """
        Test POST Orders with valid data in payload
        """
        service = Service(
            name="Service 1",
            description="Service Description",
            price=10
        )
        Session.add(service)
        Session.commit()
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
        Session.expire_all()
        order = Session.query(Order).filter(Order.id == response_data.get("id")).first()
        assert order.name == json_data["name"]
        assert order.description == json_data.get("description")
        assert order.price == json_data["price"]
        assert order.order_items[0].name == json_data["order_items"][0]["name"]
        assert order.order_items[0].description == json_data["order_items"][0].get("description")
        assert order.order_items[0].price == json_data["order_items"][0]["price"]
        Session.query(OrderItems).filter(OrderItems.order_id.in_([order.id])).delete(synchronize_session=False)
        Session.query(Order).filter(Order.id.in_([order.id])).delete(synchronize_session=False)
        Session.query(Service).filter(Service.id == service.id).delete(synchronize_session=False)
        Session.commit()

    def test_create_order_without_data(self):
        """
        Test POST Orders without data in payload
        """
        response = self.client.post(self.base_url + "/orders", json={})
        response_data = response.json()
        assert response.status_code == UNPROCESSABLE_ENTITY_STATUS_CODE
        assert response_data == {
            'name': ['Missing data for required field.'],
            'price': ['Missing data for required field.']
        }

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

    def test_create_order_with_invalid_service_id(self):
        """
        Test POST Orders with invalid service id in payload
        """
        service = Service(
            name="Service 1",
            description="Service Description",
            price=10
        )
        Session.add(service)
        Session.commit()
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

    def test_update_order_with_valid_data(self):
        """
        Test PUT Orders with valid data in payload
        """
        order = Order(  # noqa
            name="Order 1",
            description="Order Description",
            price=10
        )
        service = Service(
            name="Service 1",
            description="Service Description",
            price=10
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
        Session.add(service)
        Session.add(order)
        Session.commit()
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
                    "service_id": service.id,
                    "name": "hello New",
                    "price": 30
                }
            ]
        }
        Session.expire_all()
        response = self.client.put(self.base_url + "/orders", json=json_data)
        assert response.status_code == CREATED_STATUS_CODE
        Session.refresh(order)
        order_ = Session.query(Order).filter(Order.id == order.id).first()
        assert order_
        assert len(order_.order_items) == 3
        Session.query(OrderItems).filter(OrderItems.order_id.in_([order.id])).delete(synchronize_session=False)
        Session.query(Order).filter(Order.id.in_([order.id])).delete(synchronize_session=False)
        Session.query(Service).filter(Service.id == service.id).delete(synchronize_session=False)
        Session.commit()

    def test_put_order_with_invalid_service_id(self):
        """
        Test PUT Orders with invalid service id in payload
        """
        order = Order(  # noqa
            name="Order 1",
            description="Order Description",
            price=10
        )
        service = Service(
            name="Service 1",
            description="Service Description",
            price=10
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
        Session.add(service)
        Session.add(order)
        Session.commit()
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
        Session.query(OrderItems).filter(OrderItems.order_id.in_([order.id])).delete(synchronize_session=False)
        Session.query(Order).filter(Order.id.in_([order.id])).delete(synchronize_session=False)
        Session.query(Service).filter(Service.id == service.id).delete(synchronize_session=False)
        Session.commit()

    def test_delete_order_by_id(self):
        """
        Test DELETE Orders with id
        """
        order = Order(  # noqa
            name="Order 1",
            description="Order Description",
            price=10
        )
        service = Service(
            name="Service 1",
            description="Service Description",
            price=10
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
        Session.add(service)
        Session.add(order)
        Session.commit()
        response = self.client.delete(self.base_url + "/orders/" + str(order.id))
        assert response.status_code == UPDATE_STATUS_CODE
        Session.expire_all()
        order = Session.query(Order).filter(Order.id == order.id).first()
        assert not order.is_active
        Session.query(OrderItems).filter(OrderItems.order_id.in_([order.id])).delete(synchronize_session=False)
        Session.query(Order).filter(Order.id.in_([order.id])).delete(synchronize_session=False)
        Session.query(Service).filter(Service.id == service.id).delete(synchronize_session=False)
        Session.commit()

    def test_delete_order_by_id_with_invalid_id(self):
        """
        Test DELETE Orders with invalid id
        """
        order = Order(  # noqa
            name="Order 1",
            description="Order Description",
            price=10
        )
        service = Service(
            name="Service 1",
            description="Service Description",
            price=10
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
        Session.add(service)
        Session.add(order)
        Session.commit()
        Session.expire_all()
        response = self.client.delete(self.base_url + "/orders/" + str(order.id + 999))
        assert response.status_code == NOT_FOUND_STATUS_CODE
        Session.query(OrderItems).filter(OrderItems.order_id.in_([order.id])).delete(synchronize_session=False)
        Session.query(Order).filter(Order.id.in_([order.id])).delete(synchronize_session=False)
        Session.query(Service).filter(Service.id == service.id).delete(synchronize_session=False)
        Session.commit()

    def test_delete_order_by_id_with_nondigit_id(self):
        """
        Test DELETE Orders with invalid id
        """
        response = self.client.delete(self.base_url + "/orders/" + "hello")
        response_data = response.json()
        assert response.status_code == BAD_REQUEST_STATUS_CODE
        assert response_data == {"message": "order_id is required with valid integer"}

    def test_delete_order_by_id_without_id(self):
        """
        Test DELETE Orders without id
        """
        response = self.client.delete(self.base_url + "/orders/")
        assert response.status_code == NOT_FOUND_STATUS_CODE
