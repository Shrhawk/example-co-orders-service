from sqlalchemy import Column, Float, Integer, String, text, TEXT, TIMESTAMP, ForeignKey, Boolean
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema
from sqlalchemy.orm import relationship

from . import Base


class OrderItems(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(TEXT, nullable=True)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    created_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_on = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text(
            'CURRENT_TIMESTAMP'),
        server_onupdate=text('CURRENT_TIMESTAMP')
    )
    parent = relationship("Order", back_populates="order_items")
    service = relationship('Service')

    def __repr__(self) -> str:
        return "<OrderItems(name='{}', price='{}', created_on='{}')>".format(self.name, self.price, self.created_on)


class OrderItemSchema(SQLAlchemySchema):
    class Meta:
        model = OrderItems
        load_instance = True

    id = fields.Integer()
    name = fields.String(required=True)
    description = fields.String()
    price = fields.Float(required=True)
    order_id = fields.Integer()
    service_id = fields.Integer()
    created_on = fields.DateTime()
    modified_on = fields.DateTime()
