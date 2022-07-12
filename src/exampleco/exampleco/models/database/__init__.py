import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig()
logger = logging.getLogger("exampleco.sqltime")
logger.setLevel(logging.DEBUG)

Base = declarative_base()

session_maker = sessionmaker()

try:
    engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format('admin', 'password', 'localhost', 'db'))
    engine.connect()
except SQLAlchemyError as error:
    logger.error("Error connecting to DB")
    logger.error(error)
else:
    session_maker.configure(bind=engine)

Session = session_maker()
