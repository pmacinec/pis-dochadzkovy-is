from zeep import Client
from zeep.xsd import SkipValue
from functions import employee as e
from functions import approval as a
from functions import notifications

def create(application_type=None, begin_date=None, end_date=None, notification_type=None, comment=None, employee_id=None, file=None):
    """Function to create new application using web service."""

    if employee_id is None or application_type is None or begin_date is None or end_date is None: return False

    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071application?WSDL')

    new_application = {
        'id' : SkipValue,
        'name': '',
        'type': application_type,
        'begin_date' : begin_date,
        'end_date' : end_date,
        'notification_type' : notification_type,
        'comment' : comment if comment is not None else SkipValue,
        'employee_id' : employee_id,
        'file' : file if file is not None else SkipValue
    }

    application_id = client.service.insert('071', 'Vreqif', new_application)

    create_approvals(employee_id, application_id)

    return application_id

def create_approvals(employee_id=None, application_id=None):

    client = Client("http://labss2.fiit.stuba.sk/pis/ws/Students/Team071relationship?WSDL")

    relationships = client.service.getByAttributeValue('employee_id', str(employee_id), [])

    for relationship in relationships:
        a.create(application_id,relationship.superior_id)


def get(application_id=None):
    """Function to get application from web service."""

    if application_id is None: return
        
    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071application?WSDL')
    application = client.service.getById(int(application_id))
    application.state = get_state(application.id)

    return application

def delete(application_id=None):
    """Function to get application from web service."""

    if application_id is None: return
        
    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071application?WSDL')
    application = client.service.delete('071', 'Vreqif', int(application_id))

    return application

def get_state(id=None):

    if id is None: return

    approvals = get_approvals(id)

    if not approvals:
        return ''

    status = [approval.state for approval in approvals]

    if(2 in status):
        return 'zamietnuté'
    elif(0 in status):
        return 'riešené'
    else:
        return 'schválené' 

def get_user_applications(user_id=None):
    """Function to get all user applications from web service."""

    if user_id is None: return 
        
    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071application?WSDL')

    applications = client.service.getByAttributeValue('employee_id', str(user_id), [])
    if not applications: return []

    for application in applications:
        application.state = get_state(application.id)

    return applications

def get_approvals(id=None):

    if id is None: return

    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071approval?WSDL') 

    return client.service.getByAttributeValue('application_id', str(id), [])

def translate_state(state):

    if(2 == state):
        return 'zamietnuté'
    elif(0 == state):
        return 'riešené'
    else:
        return 'schválené' 


def get_managers(id=None):

    if id is None: return

    approvals = get_approvals(id)
    
    managers = []
    if approvals is None: return managers

    for approval in approvals:
        manager = e.get(approval.manager_id)
        manager.state = translate_state(approval.state)
        managers.append(manager)

    return managers

def check_limit(application_id, limit):

    application = get(application_id)

    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071application?WSDL')

    applications = client.service.getByAttributeValue('employee_id', str(application.employee_id), [])

    sum = 0
    for application in applications:
        var = application.end_date - application.begin_date
        sum += var.days

    return sum > limit

def delete(application_id):


    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071approval?WSDL')
    approvals = client.service.getByAttributeValue('application_id', str(application_id), [])
    if approvals:
        for approval in approvals:
            a.delete(approval.id)

    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071application?WSDL')

    return client.service.delete('071', 'Vreqif', int(application_id))


