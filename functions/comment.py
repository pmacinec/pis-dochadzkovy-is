from zeep import Client
from zeep.xsd import SkipValue
import datetime

def create(application_id, manager_id, sender_id, message):
    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071comment?WSDL')

    if application_id is None or manager_id is None or sender_id is None or message is None: return False

    new_comment = {
        'id': SkipValue,
        'name': '',
        'application_id': application_id,
        'manager_id': manager_id,
        'message': message,
        'sender_id': sender_id,
        'sent_at': datetime.datetime.now()
    }

    return client.service.insert('071', 'Vreqif', new_comment)

def get_comments_for_application(application_id, manager_id):
    client = Client('http://labss2.fiit.stuba.sk/pis/ws/Students/Team071comment?WSDL')

    comments_for_application = client.service.getByAttributeValue('application_id', application_id, [])

    if comments_for_application is None: return []
    print(comments_for_application)
    filtered = filter(lambda x: x.manager_id == manager_id, comments_for_application)

    return sorted(filtered, key=lambda x: x['sent_at'])