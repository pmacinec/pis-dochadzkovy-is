from zeep import Client
from zeep.xsd import SkipValue
from functions import employee as e
from functions import passwords

def login(request, email, password):
    
    employee = e.get_by_email(email)

    print(employee)
    if not employee: return False

    if not passwords.verify_password(employee[0].password, password): return False

    request.session['employee_id'] = employee[0].id
    
    return True

def logout(request):
    if is_logged(request):
        del request.session['employee_id']
    
def is_logged(request):
    return 'employee_id' in request.session

def get_logged_employee(request):
    if is_logged(request):
        return request.session['employee_id']