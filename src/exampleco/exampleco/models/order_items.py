from sqlalchemy import Column, Float, Integer, String, text, TEXT, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.exampleco.exampleco.database import Base


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
        server_default=text('CURRENT_TIMESTAMP'),
        server_onupdate=text('CURRENT_TIMESTAMP')
    )
    order = relationship("Order", back_populates="order_items")
    service = relationship('Service')

    def __repr__(self) -> str:
        return "<OrderItems(name='{}', price='{}', created_on='{}')>".format(self.name, self.price, self.created_on)
