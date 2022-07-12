import json

from src.exampleco.exampleco.models.database import Session
from src.exampleco.exampleco.models.database.services import Service, ServiceSchema
from src.exampleco.exampleco.constants import OK_STATUS_CODE, BAD_REQUEST_STATUS_CODE


# pylint: disable=unused-argument
def get_service_by_id(event, context):
    """
    Lambda function that get service by its database id

    Returns:
        Returns a single service
    """

    params = event.get('queryStringParameters', {}) or {}
    service_id = params.get('service-id')
    if not service_id or not str(service_id).isdigit():
        response = {
            "statusCode": BAD_REQUEST_STATUS_CODE,
            "body": json.dumps({"message": "service-id is required with valid integer"})
        }
    else:
        service_schema = ServiceSchema()
        service = Session.query(Service).get(service_id)
        results = service_schema.dump(service)
        response = {"statusCode": OK_STATUS_CODE, "body": json.dumps(results)}
    return response


# pylint: disable=unused-argument
def get_services(event, context):
    """
    Lambda function that get all services from database

    Returns:
        Returns a list of services
    """
    service_schema = ServiceSchema(many=True)
    services = Session.query(Service).all()
    response = {"statusCode": OK_STATUS_CODE, "body": json.dumps(service_schema.dump(services))}
    return response
