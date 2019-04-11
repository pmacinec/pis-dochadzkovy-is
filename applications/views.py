from django.shortcuts import render
from django.http import HttpResponse


def index(request):

    # WS get applications of logged in user

    return render(request, 'applications/index.html')


def create(request):
    return render(request, 'applications/create.html')


def new(request):
    print("bbbb")
    print(request.POST['type'])
    print(request.POST['begin_date'])
    print(request.POST['end_date'])

    return True
