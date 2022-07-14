import datetime
from typing import List, Optional

from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from src.exampleco.exampleco.models import Order, OrderItems, Service

OrderSchemaBase = sqlalchemy_to_pydantic(Order)

OrderItemSchemaBase = sqlalchemy_to_pydantic(OrderItems)

ServiceSchemaBase = sqlalchemy_to_pydantic(Service)


class ServiceSchema(ServiceSchemaBase):
    id: Optional[int]
    name: str
    description: Optional[str]
    price: float
    created_on: Optional[datetime.datetime]
    modified_on: Optional[datetime.datetime]


class OrderItemSchema(OrderItemSchemaBase):
    id: Optional[int]
    name: str
    description: Optional[str]
    price: float
    service_id: int
    created_on: Optional[datetime.datetime]
    modified_on: Optional[datetime.datetime]


class OrderSchema(OrderSchemaBase):
    id: Optional[int]
    name: str
    description: Optional[str]
    price: float
    created_on: Optional[datetime.datetime]
    modified_on: Optional[datetime.datetime]
    order_items: List[OrderItemSchema]
