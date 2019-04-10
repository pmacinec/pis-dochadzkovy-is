from django.shortcuts import render
from django.http import HttpResponse


def index(request):

    # WS get applications of logged in user

    return render(request, 'applications/index.html')


def create(request):
    return render(request, 'applications/new.html')


def new(request):
    print(request.POST['name'])
    print(request.POST['email'])

    return True
