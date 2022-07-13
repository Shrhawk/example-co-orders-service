import datetime
import json

from marshmallow import ValidationError
from sqlalchemy import extract

from src.exampleco.exampleco.constants import (
    NOT_FOUND_STATUS_CODE,
    CREATED_STATUS_CODE,
    OK_STATUS_CODE,
    UPDATE_STATUS_CODE,
    UNPROCESSABLE_ENTITY_STATUS_CODE,
    BAD_REQUEST_STATUS_CODE
)
from src.exampleco.exampleco.models.database import Session
from src.exampleco.exampleco.models.database.order_items import OrderItems
from src.exampleco.exampleco.models.database.orders import Order, OrderSchema
from src.exampleco.exampleco.models.database.services import Service


# pylint: disable=unused-argument
def get_all_orders(event, context):
    """
    Example function that demonstrates grabbing list or orders from database

    Returns:
        Returns a list of all orders pulled from the database.
    """

    orders_schema = OrderSchema(many=True)
    orders = Session.query(Order).filter(Order.is_active).all()
    results = orders_schema.dump(orders)
    response = {"statusCode": OK_STATUS_CODE, "body": json.dumps(results)}
    return response


def get_order_by_id(event, context):
    """
    Example function that demonstrates grabbing order and its order items from database

    Returns:
        Returns order and its list order_items pulled from the database.
    """
    orders_schema = OrderSchema(many=False)
    order_data = event.get('pathParameters', {}) or {}
    order_id = order_data.get("order_id")
    if not order_id or not str(order_id).isdigit():
        response = {
            "statusCode": BAD_REQUEST_STATUS_CODE,
            "body": json.dumps({"message": "order_id is required with valid integer"})
        }
        return response
    order = Session.query(Order).filter(Order.id == order_id, Order.is_active).first()
    if not order:
        return {"statusCode": NOT_FOUND_STATUS_CODE, "body": json.dumps({"message": "Order not found"})}
    results = orders_schema.dump(order)
    response = {"statusCode": OK_STATUS_CODE, "body": json.dumps(results)}
    return response


# pylint: disable=unused-argument
def create_order(event, context):
    """
    Example function that create order with its items

    Returns:
        Returns order and its order items which or created.
    """
    errors = {}
    order_data = event.get('body', {}) or {}
    order_data = json.loads(order_data)
    orders_schema = OrderSchema(many=False)
    try:
        order = orders_schema.load(order_data, transient=True)
    except ValidationError as err:
        return {"statusCode": UNPROCESSABLE_ENTITY_STATUS_CODE, "body": json.dumps(err.messages)}
    services = Session.query(Service).all()
    all_services = {}
    for service in services:
        all_services[service.id] = service
    if not order.order_items:
        result = {"message": "order_items is mandatory"}
        return {"statusCode": UNPROCESSABLE_ENTITY_STATUS_CODE, "body": json.dumps(result)}
    order_item_objects = []
    order_object = Order(
        name=order.name,
        description=order.description,
        price=order.price
    )
    for order_item_index, order_item in enumerate(order.order_items):
        if not all_services.get(order_item.service_id):
            errors[str(order_item_index)] = {"service_id": ["Service Id is invalid"]}
        order_item_objects.append(OrderItems(
            name=order_item.name,
            description=order_item.description,
            price=order_item.price,
            order=order_object,
            service=all_services.get(order_item.service_id)
        ))
    if errors:
        result = {"order_items": errors}
        return {"statusCode": UNPROCESSABLE_ENTITY_STATUS_CODE, "body": json.dumps(result)}
    order_object.order_items = order_item_objects
    Session.add(order_object)
    Session.commit()
    response = {"statusCode": CREATED_STATUS_CODE, "body": json.dumps(order_data)}
    return response


# pylint: disable=unused-argument
def update_order(event, context):
    """
    Example function that update order with its items

    Returns:
        Returns order and its order items which or update.
    """
    errors = {}
    order_data = event.get('body', {}) or {}
    order_data = json.loads(order_data)
    if not order_data.get("id") or not str(order_data.get("id")).isdigit():
        response = {
            "statusCode": BAD_REQUEST_STATUS_CODE,
            "body": json.dumps({"message": "id is required with valid integer"})
        }
        return response
    order = Session.query(Order).filter(Order.id == order_data.get("id"), Order.is_active).first()
    if not order:
        return {"statusCode": UNPROCESSABLE_ENTITY_STATUS_CODE, "body": json.dumps({"message": "Order not found"})}
    services = Session.query(Service).all()
    all_services = {}
    for service in services:
        all_services[service.id] = service
    for order_item_index, order_item in enumerate(order_data.get("order_items")):
        if not all_services.get(order_item.get("service_id")):
            errors[str(order_item_index)] = {"service_id": ["Service Id is invalid"]}
    if errors:
        result = {"order_items": errors}
        return {"statusCode": UNPROCESSABLE_ENTITY_STATUS_CODE, "body": json.dumps(result)}
    orders_schema = OrderSchema(many=False)
    try:
        order = orders_schema.load(order_data, instance=order)
    except ValidationError as err:
        return {"statusCode": UNPROCESSABLE_ENTITY_STATUS_CODE, "body": json.dumps(err.messages)}
    Session.add(order)
    Session.commit()
    response = {"statusCode": CREATED_STATUS_CODE, "body": json.dumps(orders_schema.dump(order))}
    return response


def delete_order(event, context):
    """
    Example function that delete order with its items

    Returns:
        Returns order and its order items which or delete.
    """
    order_data = event.get('pathParameters', {}) or {}
    order_id = order_data.get("order_id")
    if not order_id or not str(order_id).isdigit():
        response = {
            "statusCode": BAD_REQUEST_STATUS_CODE,
            "body": json.dumps({"message": "order_id is required with valid integer"})
        }
        return response
    order = Session.query(Order).filter(Order.id == order_id, Order.is_active).first()
    if not order:
        return {"statusCode": NOT_FOUND_STATUS_CODE, "body": json.dumps({"message": "Order not found"})}
    order.is_active = False
    Session.add(order)
    Session.commit()
    return {"statusCode": UPDATE_STATUS_CODE}
