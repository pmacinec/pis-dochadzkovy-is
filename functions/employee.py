from zeep import Client
from zeep.xsd import SkipValue
from functions import application as a
from functions import validator

def create(name, email, manager_id, password=None, phone=None):
    """Function to create new employee using web service."""

    if name is None or email is None or manager_id is None: return False

    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071employee?WSDL')

    new_employee = {
        'id': SkipValue,
        'name': name,
        'email': email,
        'password': password if password is not None else SkipValue,
        'phone': phone if phone is not None else SkipValue
    }

    employee_id = client.service.insert('071', 'Vreqif', new_employee)

    # Create relationship between manager and employee
    relationships_client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071relationship?WSDL')
    relationship = {
        'id': SkipValue,
        'name': '',
        'employee_id': employee_id,
        'superior_id': manager_id
    }
    relationships_client.service.insert('071', 'Vreqif', relationship)

    return employee_id


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

def get_by_email(email):
    
    if not validator.validate_email(email): return False
    
    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071employee?WSDL')

    return client.service.getByAttributeValue('email', email, [])

def get_manager_approvals(manager_id=None):

    if manager_id is None: return

    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071approval?WSDL') 

    approvals = client.service.getByAttributeValue('manager_id', str(manager_id), [])

    if not approvals: return

    for approval in approvals:
        approval.application = a.get(approval.application_id)

    return approvals

def is_manager(employee_id):
    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071relationship?WSDL')

    employees = client.service.getByAttributeValue('superior_id', employee_id, [])

    return False if employees is None or len(employees) == 0 else True
