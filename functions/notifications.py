from zeep import Client
from functions import employee as e

def send_email(email, subject, message):
    # connect to web service
    email_client = Client('http://labss2.fiit.stuba.sk/pis/ws/NotificationServices/Email?WSDL')
    
    res = email_client.service.notify('071', 'Vreqif', email, subject, message)

    return True if res == 'success' else False


def send_notification(employee_id, type, subject, message):

	employee = e.get(employee_id)

	if type == 'email':
		client = Client('http://labss2.fiit.stuba.sk/pis/ws/NotificationServices/Email?WSDL')
		res = client.service.notify('071', 'Vreqif', employee.email, subject, message)
	else:
		client = Client('http://labss2.fiit.stuba.sk/pis/ws/NotificationServices/SMS?WSDL')
		res = client.service.notify('071', 'Vreqif', employee.phone, subject, message)

	return True if res == 'success' else False
    