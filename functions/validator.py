from zeep import Client
from zeep.xsd import SkipValue

def validate_email(email):
    """Function to validate email using web service."""
    
    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Validator?WSDL')
    
    return client.service.validateEmail(email)


def validate_phone(phone):
    """Function to validate phone number using web service."""

    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Validator?WSDL')

    return client.service.validatePhone(phone)