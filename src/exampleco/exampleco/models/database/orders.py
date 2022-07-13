from sqlalchemy import Column, Float, Integer, String, text, TEXT, TIMESTAMP, Boolean
from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemySchema
from sqlalchemy.orm import relationship

from . import Base, Session
from .order_items import OrderItems, OrderItemSchema


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(TEXT, nullable=True)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    order_items = relationship(OrderItems, back_populates="order", uselist=True)
    created_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_on = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP'),
        server_onupdate=text('CURRENT_TIMESTAMP')
    )

    def __repr__(self) -> str:
        return "<Service(name='{}', price='{}', created_on='{}')>".format(self.name, self.price, self.created_on)


class OrderSchema(SQLAlchemySchema):
    class Meta:
        model = Order
        sqla_session = Session
        load_instance = True

    id = fields.Integer()
    name = fields.String(required=True)
    description = fields.String()
    price = fields.Float(required=True)
    created_on = fields.DateTime()
    modified_on = fields.DateTime()
    order_items = fields.List(fields.Nested(OrderItemSchema), required=True)
