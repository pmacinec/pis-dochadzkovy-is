from zeep import Client
from zeep.xsd import SkipValue


def get(approval_id=None):
    """Function to get application from web service."""

    if approval_id is None: return
        
    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071approval?WSDL')
    approval = client.service.getById(int(approval_id))

    return approval

def update(approval_id=None,state=None):
    """Function to get application from web service."""

    if approval_id is None or state is None: return
        
    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071approval?WSDL')
    approval = get(int(approval_id))
    approval.state = int(state)
    approval.name = ""

    client.service.update('071', 'Vreqif', approval.id, approval)

    return approval

def create(application_id=None,manager_id=None):

    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071approval?WSDL')

    new_approval = {
        'id' : SkipValue,
        'name': '',
        'application_id' : application_id,
        'manager_id': manager_id,
        'state' : 0
    }

    client.service.insert('071', 'Vreqif', new_approval)