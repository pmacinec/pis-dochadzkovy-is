from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from zeep import Client
from functions import application as a
from functions import employee as e
from functions import approval as p
from functions import login as l
from functions import comment as c
from functions import notifications as n

def index(request):
    # Check if employee is authenticated
    if not l.is_logged(request): return HttpResponseRedirect('/sign-in')

    employee_id = l.get_logged_employee(request)
    
    applications = a.get_user_applications(employee_id)
    approvals = e.get_manager_approvals(employee_id)

    return render(
        request, 
        'applications/index.html',
        { 'applications': applications, 'approvals': approvals, 'is_manager': e.is_manager(employee_id) }
    )

def create(request):
    # Check if employee is authenticated
    if not l.is_logged(request): return HttpResponseRedirect('/sign-in')

    return render(request, 'applications/create.html')

def new(request):
    # Check if employee is authenticated
    if not l.is_logged(request): return HttpResponseRedirect('/sign-in')
    
    application_type = request.POST['type']
    notification = request.POST['notification']
    comment = request.POST['comment']
    begin_date = request.POST['begin_date']
    end_date = request.POST['end_date']
    
    application_id = a.create(
        application_type, 
        begin_date, 
        end_date, 
        notification,
        comment, 
        l.get_logged_employee(request)
    )

    return HttpResponseRedirect('/applications/' + str(application_id))

def show(request, id):
    # Check if employee is authenticated
    if not l.is_logged(request): return HttpResponseRedirect('/sign-in')

    application = a.get(id)
    employee = e.get(application.employee_id)
    managers = a.get_managers(application.id)

    return render(
        request, 
        'applications/show.html', 
        { 
            'application': application, 
            'employee': employee, 
            'managers': managers,
            'is_manager': l.get_logged_employee(request) != application.employee_id
        }
    )

def approval_show(request, application_id, approval_id):
    if not l.is_logged(request): return HttpResponseRedirect('/sign-in')
    current_user = l.get_logged_employee(request)

    if request.method == 'GET':

        approval = p.get(approval_id)
        application = a.get(application_id)
        employee = e.get(application.employee_id)
        managers = a.get_managers(application_id)

        return render(
            request, 
            'applications/show.html',
            {
                'approval': approval,
                'application': application,
                'employee': employee,
                'managers': managers,
                'is_manager': current_user != application.employee_id,
                'current_user': current_user
            }
        )

    elif request.method == 'POST':

        if not l.is_logged(request): return HttpResponseRedirect('/sign-in')

        if request.POST['approved'] == "1":
            p.update(approval_id, 1)
        else:
            p.update(approval_id, 2)

        approval = p.get(approval_id)
        application = a.get(application_id)
        employee = e.get(application.employee_id)
        managers = a.get_managers(application_id)

        return render(
            request, 
            'applications/show.html',
            {
                'approval': approval,
                'application': application,
                'employee': employee,
                'managers': managers,
                'is_manager': current_user != application.employee_id
            }
        )


# Comments
def conversation(request, application_id, manager_id):
    if not l.is_logged(request): return HttpResponseRedirect('/sign-in')

    comments = c.get_comments_for_application(application_id, manager_id)

    return render(
        request,
        'applications/conversation.html',
        { 
            'application_id': application_id,
            'manager_id': manager_id,
            'user_id': l.get_logged_employee(request),
            'messages': comments 
        }
    )

def send_message(request, application_id, manager_id):
    if not l.is_logged(request): return HttpResponseRedirect('/sign-in')

    message = request.POST['message']
    current_user = l.get_logged_employee(request)

    c.create(
        application_id,
        manager_id,
        current_user,
        message
    )

    if current_user == manager_id:
        application = a.get(application_id)
        oposite_user = e.get(application.employee_id)
        # @TODO dorobit notifikaciu podla toho, aku si vybral
    else:
        oposite_user = e.get(manager_id)
        n.send_email(
            oposite_user.email, 
            'Nová správa pri schvaľovaní žiadosti',
            'Pri schvaľovaní žiadosti č. ' + str(application_id) + ' pribudla nová správa.'
        )

    return HttpResponseRedirect('/applications/' + str(application_id) + '/conversation/' + str(manager_id))