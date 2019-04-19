from zeep import Client
from zeep.xsd import SkipValue

def create(application_type=None, begin_date=None, end_date=None, notification_type=None, comment=None, employee_id = None, file = None):
    """Function to create new application using web service."""

    if employee_id == None or application_type == None or begin_date == None or end_date == None: return False

    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071application?WSDL')

    new_application = {
        'id' : SkipValue,
        'name': '',
        'type': application_type,
        'begin_date' : begin_date,
        'end_date' : end_date,
        'notification_type' : notification_type,
        'comment' : comment,
        'employee_id' : employee_id,
        'file' : file
    }

    return client.service.insert('071', 'Vreqif', new_application)


def get(application_id=None):
    """Function to get application from web service."""

    if application_id is None: return
        
    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071application?WSDL')

    return client.service.getById(int(application_id))

def get_user_applications(user_id=None):
    """Function to get all user applications from web service."""

    if user_id is None: return
        
    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071application?WSDL')

    return client.service.getByAttributeValue('employee_id', str(user_id), (0,1))


# def update(employee_id, password=None, phone=None):
#     """Function to update employee using web service."""
    
#     if employee_id is None: return False

#     if password is None and phone is None: return False

#     client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071employee?WSDL')

#     employee_data = {
#         'id': SkipValue,
#         'name': SkipValue,
#         'email': SkipValue,
#         'password': password if password is not None else SkipValue,
#         'phone': phone if phone is not None else SkipValue
#     }

#     return client.service.update('071', 'Vreqif', employee_id, employee_data)