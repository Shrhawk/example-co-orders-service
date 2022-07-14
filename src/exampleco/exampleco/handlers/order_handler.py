import json

from pydantic import ValidationError
from sqlalchemy import extract, func

from src.exampleco.exampleco.constants import (
    NOT_FOUND_STATUS_CODE,
    CREATED_STATUS_CODE,
    OK_STATUS_CODE,
    UPDATE_STATUS_CODE,
    UNPROCESSABLE_ENTITY_STATUS_CODE,
    BAD_REQUEST_STATUS_CODE,
    THIS_YEAR,
    THIS_MONTH, THIS_WEEK
)
from src.exampleco.exampleco.helpers import time_period_to_time_convertor
from src.exampleco.exampleco.database import get_session
from src.exampleco.exampleco.models import OrderItems, Order, Service
from src.exampleco.exampleco.schemas import OrderSchema, OrderItemSchema


# pylint: disable=unused-argument
def get_all_orders(event, context):
    """
    Example function that demonstrates grabbing list or orders from database

    Returns:
        Returns a list of all orders pulled from the database.
    """
    session = get_session()
    orders = session.query(Order).filter(Order.is_active).all()
    results = []
    for order in orders:
        results.append(json.loads(OrderSchema.from_orm(order).json()))
    response = {"statusCode": OK_STATUS_CODE, "body": json.dumps(results)}
    return response


# pylint: disable=unused-argument
def get_order_analytics(event, context):
    """
    Example function that demonstrates order analytics from database

    Returns:
        Returns analytics of all orders pulled from the database.
    """
    session = get_session()
    data = event.get('queryStringParameters', {}) or {}
    time_period = data.get('time_period')
    if not time_period or time_period not in [THIS_WEEK, THIS_MONTH, THIS_YEAR]:
        response = {
            "statusCode": BAD_REQUEST_STATUS_CODE,
            "body": json.dumps({"message": "time_period is required with valid string"})
        }
        return response
    filters = [Order.is_active]
    date = time_period_to_time_convertor(time_period)
    if time_period == THIS_YEAR:
        filters.append(extract('year', Order.created_on) == date)
        query = session.query(func.month(Order.created_on), func.count(Order.created_on))
    elif time_period == THIS_MONTH:
        filters.append(extract('month', Order.created_on) == date)
        query = session.query(func.day(Order.created_on), func.count(Order.created_on))
    else:
        filters.append(extract('week', Order.created_on) == date)
        query = session.query(func.day(Order.created_on), func.count(Order.created_on))
    result = query.filter(*filters).group_by(Order.created_on).distinct(Order.id).all()
    response = {"statusCode": OK_STATUS_CODE, "body": json.dumps(result)}
    return response


def get_order_by_id(event, context):
    """
    Example function that demonstrates grabbing order and its order items from database

    Returns:
        Returns order and its list order_items pulled from the database.
    """
    session = get_session()
    order_data = event.get('pathParameters', {}) or {}
    order_id = order_data.get("order_id")
    if not order_id or not str(order_id).isdigit():
        response = {
            "statusCode": BAD_REQUEST_STATUS_CODE,
            "body": json.dumps({"message": "order_id is required with valid integer"})
        }
        return response
    order = session.query(Order).filter(Order.id == order_id, Order.is_active).first()
    if not order:
        return {"statusCode": NOT_FOUND_STATUS_CODE, "body": json.dumps({"message": "Order not found"})}
    response = {"statusCode": OK_STATUS_CODE, "body": OrderSchema.from_orm(order).json()}
    return response


# pylint: disable=unused-argument
def create_order(event, context):
    """
    Example function that create order with its items

    Returns:
        Returns order and its order items which or created.
    """
    session = get_session()
    errors = {}
    order_data = event.get('body', {}) or {}
    order_data = json.loads(order_data)
    try:
        order = OrderSchema(**order_data)
    except ValidationError as err:
        return {"statusCode": UNPROCESSABLE_ENTITY_STATUS_CODE, "body": json.dumps(err.errors())}
    services = session.query(Service).all()
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
    session.add(order_object)
    session.commit()
    response = {"statusCode": CREATED_STATUS_CODE, "body": OrderSchema.from_orm(order_object).json()}
    return response


# pylint: disable=unused-argument
def update_order(event, context):
    """
    Example function that update order with its items

    Returns:
        Returns order and its order items which or update.
    """
    session = get_session()
    errors = {}
    order_data = event.get('body', {}) or {}
    order_data = json.loads(order_data)
    if not order_data.get("id") or not str(order_data.get("id")).isdigit():
        response = {
            "statusCode": BAD_REQUEST_STATUS_CODE,
            "body": json.dumps({"message": "id is required with valid integer"})
        }
        return response
    order_object = session.query(Order).filter(Order.id == order_data.get("id"), Order.is_active).first()
    if not order_object:
        return {"statusCode": UNPROCESSABLE_ENTITY_STATUS_CODE, "body": json.dumps({"message": "Order not found"})}
    services = session.query(Service).all()
    all_services, old_order_items = {}, {}
    for service in services:
        all_services[service.id] = service
    for old_order_item in order_object.order_items:
        old_order_items[old_order_item.id] = old_order_item
    for order_item_index, order_item in enumerate(order_data.get("order_items")):
        if not all_services.get(order_item.get("service_id")):
            errors[str(order_item_index)] = {"service_id": ["Service Id is invalid"]}
    if errors:
        result = {"order_items": errors}
        return {"statusCode": UNPROCESSABLE_ENTITY_STATUS_CODE, "body": json.dumps(result)}
    try:
        order = OrderSchema(**order_data)
    except ValidationError as err:
        return {"statusCode": UNPROCESSABLE_ENTITY_STATUS_CODE, "body": json.dumps(err.errors())}
    for key, value in order.dict(exclude_unset=True, exclude={"order_items"}).items():
        setattr(order_object, key, value)
    new_order_items = []
    for order_item in order.order_items:
        if old_order_items.get(order_item.id):
            for key, value in order_item.dict(exclude_unset=True).items():
                setattr(old_order_items.get(order_item.id), key, value)
        else:
            new_order_items.append(OrderItems(**order_item.dict(exclude={"id", "is_active"})))
    old_order_items = list(old_order_items.values())
    old_order_items.extend(new_order_items)
    order_object.order_items = old_order_items
    session.add(order_object)
    session.commit()
    response = {"statusCode": CREATED_STATUS_CODE, "body": OrderSchema.from_orm(order).json()}
    return response


def delete_order(event, context):
    """
    Example function that delete order with its items

    Returns:
        Returns order and its order items which or delete.
    """
    session = get_session()
    order_data = event.get('pathParameters', {}) or {}
    order_id = order_data.get("order_id")
    if not order_id or not str(order_id).isdigit():
        response = {
            "statusCode": BAD_REQUEST_STATUS_CODE,
            "body": json.dumps({"message": "order_id is required with valid integer"})
        }
        return response
    order = session.query(Order).filter(Order.id == order_id, Order.is_active).first()
    if not order:
        return {"statusCode": NOT_FOUND_STATUS_CODE, "body": json.dumps({"message": "Order not found"})}
    order.is_active = False
    session.add(order)
    session.commit()
    return {"statusCode": UPDATE_STATUS_CODE}
