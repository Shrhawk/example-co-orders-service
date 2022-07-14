from sqlalchemy import Column, Float, Integer, String, text, TEXT, TIMESTAMP

from src.exampleco.exampleco.database import Base


class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(TEXT, nullable=True)
    price = Column(Float, nullable=False)
    created_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_on = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text(
            'CURRENT_TIMESTAMP'),
        server_onupdate=text('CURRENT_TIMESTAMP')
    )

    def __repr__(self) -> str:
        return "<Service(name='{}', price='{}', created_on='{}')>".format(self.name, self.price, self.created_on)
