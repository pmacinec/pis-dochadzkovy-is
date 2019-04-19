from django.shortcuts import render
from django.http import HttpResponse
from zeep import Client
from functions import application as a

def index(request):

    # WS get applications of logged in user
    applications = a.get_user_applications(190506)

    return render(request, 'applications/index.html', {'applications': applications})


def create(request):
    return render(request, 'applications/create.html')


def new(request):
    print("bbbb")
    print(request.POST['type'])
    print(request.POST['begin_date'])
    print(request.POST['end_date'])

    return True


