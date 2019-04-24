from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from zeep import Client
from zeep.xsd import SkipValue
from functions import notifications
from functions import passwords
from functions import validator
from functions import employee as e
from functions import login as l

# Create your views here.
def index(request):
    return render(request, 'dochadzkovy_is/index.html')

# Registration
def registration(request):
    # Check if employee is authenticated
    if not l.is_logged(request): return HttpResponseRedirect('/sign-in')

    return render(request, 'dochadzkovy_is/registration.html')

def registrate(request):
    # Check if employee is authenticated
    if not l.is_logged(request): return HttpResponseRedirect('/sign-in')
    
    name = request.POST['name']
    email = request.POST['email']

    errors = []
    if not validator.validate_length(name,min_length=2, max_length=50):
        errors += ["Zadajte prosím meno z rozsahu 2 až 50 znakov!"]

    if not validator.validate_email(email):
        errors += ['Zadajte prosím platný email.']

    if errors:
        return render(
            request,
            'dochadzkovy_is/registration.html',
            {'message_type': "danger", "message": '\n'.join(errors)}
        )

    # create new employee using web service
    employee_id = e.create(name, email, l.get_logged_employee(request))

    message = 'Dobrý deň ' + name + ', práve ste boli zaregistrovaní. Kliknite prosím, na nasledujúci odkaz\
                pre doplnenie údajov: /complete-registration/' + str(employee_id)

    notifications.send_email(email, 'Nová registrácia', message)

    return render(
        request, 
        'dochadzkovy_is/registration.html',
        { 'message_type': 'success', 'message': 'Registrácia úspešne dokončená.' }
    )


def complete_registration(request, employee_id):

    employee = e.get(employee_id)

    if employee is not None and employee.password is not None:
        return HttpResponseRedirect('/')

    return render(
        request, 
        'dochadzkovy_is/complete_registration.html',
        { 'employee_id': employee_id }
    )


# Employee
def update_employee(request):
    employee_id = request.POST['employee_id']
    password = request.POST['password']
    password_repeat = request.POST['password_repeat']
    phone = request.POST['phone']

    if not employee_id or len(employee_id) == 0:
        return HttpResponseRedirect('/')

    employee = e.get(employee_id)

    if not employee or employee.password is not None:
        return HttpResponseRedirect('/')

    validation_errors = []

    if not validator.validate_phone(phone): 
        validation_errors += ['Telefónne číslo je v nesprávnom tvare.']

    if str(password) == str(password_repeat):
        password_to_store = passwords.hash_password(str(password))
    else:
        validation_errors += ['Heslá sa nezhodujú.']

    if len(validation_errors) != 0:
        return render(
            request, 
            'dochadzkovy_is/complete_registration.html', 
            { 
                'message_type': 'danger',
                'message': '\n'.join(validation_errors),
                'employee_id': employee_id
            }
        )

    if e.update(employee_id, password_to_store, phone):
        message = { 
            'message_type': 'success',
            'message': 'Informácie úspešne uložené.',
            'employee_id': employee_id
        }
    else:
        message = { 
            'message_type': 'danger',
            'message': 'Vyskytla sa chyba pri ukladaní údajov.',
            'employee_id': employee_id
        }

    return render(
        request, 
        'dochadzkovy_is/complete_registration.html', 
        message
    )


# Login
def sign_in(request):
    return render(request, 'dochadzkovy_is/sign_in.html')

def login(request):
    email = request.POST['email']
    password = request.POST['password']

    if l.login(request, email, password):
        return HttpResponseRedirect('/applications')
    else:
        return render(
            request,
            'dochadzkovy_is/sign_in.html',
            { 'message': 'Nesprávne prihlasovacie údaje.' }
        )

def logout(request):
    l.logout(request)
    return HttpResponseRedirect('/sign-in')