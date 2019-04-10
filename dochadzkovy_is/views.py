from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('Hello World.')

def registration(request):
    return render(request, 'dochadzkovy_is/registration.html')

def registrate(request):
    print(request.POST['name'])
    print(request.POST['email'])

    # ws

    # email zamestnancovi

    # return redirect a hlaska
    
    return True