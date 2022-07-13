import pytest
from src.exampleco.exampleco.constants import OK_STATUS_CODE, BAD_REQUEST_STATUS_CODE
from src.exampleco.exampleco.models.database import Session
from src.exampleco.exampleco.models.database.order_items import OrderItems
from src.exampleco.exampleco.models.database.orders import Order
from src.exampleco.exampleco.models.database.services import Service
from src.exampleco.exampleco.tests.conftest import TestCase


class TestServices(TestCase):
    """
    Tests for Services Apis
    """
    @pytest.mark.run(order=1)
    def test_get_services_with_more_than_one_data_in_db(self):
        """
        Test GET Services with more than one data in database
        """
        response = self.client.get(self.base_url + "/services")
        response_data = response.json()
        assert response.status_code == OK_STATUS_CODE
        assert len(response_data) >= 3
        assert response_data[0]["name"] == "Service 1"
        assert response_data[0]["description"] == "Service Description"
        assert response_data[0]["price"] == 10
        assert response_data[1]["name"] == "Service 2"
        assert response_data[1]["description"] == "Service Description 2"
        assert response_data[1]["price"] == 20
        assert response_data[2]["name"] == "Service 3"
        assert response_data[2]["description"] == "Service Description 3"
        assert response_data[2]["price"] == 30

    @pytest.mark.run(order=2)
    def test_get_service_by_id_without_any_data_in_db(self):
        """
        Test GET Services without Any data in database
        """
        response = self.client.get(self.base_url + "/service-by-id", params={"service-id": 99999})
        response_data = response.json()
        assert response.status_code == OK_STATUS_CODE
        assert not response_data

    @pytest.mark.run(order=3)
    def test_get_service_by_id_with_valid_id(self):
        """
        Test GET Services without Any data in database
        """
        service = Session.query(Service).first()
        response = self.client.get(self.base_url + "/service-by-id", params={"service-id": service.id})
        response_data = response.json()
        assert response.status_code == OK_STATUS_CODE
        assert response_data["name"] == "Service 1"
        assert response_data["description"] == "Service Description"
        assert response_data["price"] == 10

    @pytest.mark.run(order=4)
    def test_get_service_by_id_with_invalid_id(self):
        """
        Test GET Services with invalid service id
        """
        response = self.client.get(self.base_url + "/service-by-id", params={"service-id": 99999})
        response_data = response.json()
        assert response.status_code == OK_STATUS_CODE
        assert not response_data

    @pytest.mark.run(order=5)
    def test_get_service_by_id_without_service_id(self):
        """
        Test GET Services without service id
        """
        response = self.client.get(self.base_url + "/service-by-id")
        response_data = response.json()
        assert response.status_code == BAD_REQUEST_STATUS_CODE
        assert response_data == {"message": "service-id is required with valid integer"}

    @pytest.mark.run(order=6)
    def test_get_service_by_id_with_non_digit_service_id(self):
        """
        Test GET Services with non-digit service id
        """
        response = self.client.get(self.base_url + "/service-by-id", params={"service-id": "nondigit"})
        response_data = response.json()
        assert response.status_code == BAD_REQUEST_STATUS_CODE
        assert response_data == {"message": "service-id is required with valid integer"}

    @pytest.mark.run(order=7)
    def test_get_services_with_one_data_in_db(self):
        """
        Test GET Services with One data in database
        """
        service = Session.query(Service).first()
        Session.query(OrderItems).delete()
        Session.query(Service).filter(Service.id != service.id).delete()
        Session.query(Order).delete()
        Session.commit()
        Session.expire_all()
        response = self.client.get(self.base_url + "/services")
        response_data = response.json()
        assert response.status_code == OK_STATUS_CODE
        assert len(response_data) >= 1
        assert response_data[0]["name"] == "Service 1"
        assert response_data[0]["description"] == "Service Description"
        assert response_data[0]["price"] == 10

    @pytest.mark.run(order=8)
    def test_get_services_without_any_data_in_db(self):
        """
        Test GET Services without Any data in database
        """
        Session.query(OrderItems).delete()
        Session.query(Service).delete()
        Session.query(Order).delete()
        Session.commit()
        response = self.client.get(self.base_url + "/services")
        response_data = response.json()
        assert response.status_code == OK_STATUS_CODE
        assert not response_data
