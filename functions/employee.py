from zeep import Client
from zeep.xsd import SkipValue

def create(name=None, email=None, password=None, phone=None):
    """Function to create new employee using web service."""

    if name == None or email == None: return False

    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071employee?WSDL')

    new_employee = {
        'id': SkipValue,
        'name': name,
        'email': email,
        'password': password if password is not None else SkipValue,
        'phone': phone if phone is not None else SkipValue
    }

    return client.service.insert('071', 'Vreqif', new_employee)


def get(employee_id):
    """Function to get employee from web service."""

    if employee_id is None: return
        
    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071employee?WSDL')

    return client.service.getById(int(employee_id))


def update(employee_id, password=None, phone=None):
    """Function to update employee using web service."""
    
    if employee_id is None: return False

    if password is None and phone is None: return False

    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071employee?WSDL')

    employee_data = {
        'id': SkipValue,
        'name': SkipValue,
        'email': SkipValue,
        'password': password if password is not None else SkipValue,
        'phone': phone if phone is not None else SkipValue
    }

    return client.service.update('071', 'Vreqif', employee_id, employee_data)