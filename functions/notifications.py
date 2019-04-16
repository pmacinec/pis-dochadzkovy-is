from zeep import Client

def send_email(email, subject, message):
    # connect to web service
    email_client = Client('http://labss2.fiit.stuba.sk/pis/ws/NotificationServices/Email?WSDL')
    
    res = email_client.service.notify('071', 'Vreqif', email, subject, message)

    return True if res == 'success' else False
    