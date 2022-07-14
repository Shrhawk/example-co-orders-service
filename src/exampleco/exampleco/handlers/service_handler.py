import json

from src.exampleco.exampleco.database import get_session
from src.exampleco.exampleco.models import Service
from src.exampleco.exampleco.schemas import ServiceSchema
from src.exampleco.exampleco.constants import OK_STATUS_CODE, BAD_REQUEST_STATUS_CODE


# pylint: disable=unused-argument
def get_service_by_id(event, context):
    """
    Lambda function that get service by its database id

    Returns:
        Returns a single service
    """
    session = get_session()
    params = event.get('queryStringParameters', {}) or {}
    service_id = params.get('service-id')
    if not service_id or not str(service_id).isdigit():
        response = {
            "statusCode": BAD_REQUEST_STATUS_CODE,
            "body": json.dumps({"message": "service-id is required with valid integer"})
        }
    else:
        service = session.query(Service).get(service_id)
        if not service:
            return {"statusCode": OK_STATUS_CODE, "body": json.dumps([])}
        results = ServiceSchema.from_orm(service).json()
        response = {"statusCode": OK_STATUS_CODE, "body": results}
    return response


# pylint: disable=unused-argument
def get_services(event, context):
    """
    Lambda function that get all services from database

    Returns:
        Returns a list of services
    """
    session = get_session()
    services = session.query(Service).all()
    results = []
    for service in services:
        results.append(json.loads(ServiceSchema.from_orm(service).json()))
    response = {"statusCode": OK_STATUS_CODE, "body": json.dumps(results)}
    return response
