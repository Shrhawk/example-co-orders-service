import json

from exampleco.models.database import Session
from exampleco.models.database.orders import Order, OrderSchema


# pylint: disable=unused-argument
def get_all_orders(event, context):
    """
    Example function that demonstrates grabbing list or orders from database

    Returns:
        Returns a list of all orders pulled from the database.
    """

    orders_schema = OrderSchema(many=True)
    orders = Session.query(Order).all()
    results = orders_schema.dump(orders)

    response = {"statusCode": 200, "body": json.dumps(results)}

    return response
