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