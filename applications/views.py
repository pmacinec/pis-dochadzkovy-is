from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from zeep import Client
from functions import application as a
from functions import employee as e
from functions import login as l

def index(request):
    # Check if employee is authenticated
    if not l.is_logged(request): return HttpResponseRedirect('/sign-in')

    employee_id = request.session['employee_id']
    
    applications = a.get_user_applications(employee_id)
    approvals = e.get_manager_approvals(employee_id)

    return render(request, 'applications/index.html', {'applications': applications, 'approvals': approvals})

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
        { 'application':application, 'employee':employee, 'managers':managers }
    )


