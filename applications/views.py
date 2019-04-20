from django.shortcuts import render
from django.http import HttpResponse
from zeep import Client
from functions import application as a
from functions import employee as e

def index(request):

    # WS get applications of logged in user
    applications = a.get_user_applications(190506)
    approvals = e.get_manager_approvals(190506)

    return render(request, 'applications/index.html', {'applications': applications, 'approvals': approvals})


def create(request):
    return render(request, 'applications/create.html')


def new(request):
    print("bbbb")
    print(request.POST['type'])
    print(request.POST['begin_date'])
    print(request.POST['end_date'])

    return True

def show(request,id):
    application = a.get(id)
    employee = e.get(application.employee_id)
    managers = a.get_managers(application.id)

    return render(request, 'applications/show.html', {'application':application, 'employee':employee, 'managers':managers })


