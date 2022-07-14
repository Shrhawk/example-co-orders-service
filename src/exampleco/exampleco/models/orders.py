from sqlalchemy import Column, Float, Integer, String, text, TEXT, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship

from src.exampleco.exampleco.database import Base


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(TEXT, nullable=True)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    order_items = relationship("OrderItems", back_populates="order", uselist=True)
    created_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_on = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP'),
        server_onupdate=text('CURRENT_TIMESTAMP')
    )

    def __repr__(self) -> str:
        return "<Order(name='{}', price='{}', created_on='{}')>".format(self.name, self.price, self.created_on)
