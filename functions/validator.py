from zeep import Client
from zeep.xsd import SkipValue
from datetime import datetime as dt

def validate_email(email):
    """Function to validate email using web service."""

    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Validator?WSDL')

    return client.service.validateEmail(email)


def validate_phone(phone):
    """Function to validate phone number using web service."""

    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Validator?WSDL')

    return client.service.validatePhone(phone)


def validate_length(string, min_length=5, max_length=100):
    """Function to validate string length."""
    return min_length <= len(string) <= max_length


def validate_date(begin, end):
    """
    Function to validate date range,

    inputs:
    @begin : date-string in format 'YYYY-MM-DD'
    @end : date-string in format 'YYYY-MM-DD'
    """
    return dt.strptime(begin, "%Y-%m-%d").date() <= dt.strptime(end, "%Y-%m-%d").date()
