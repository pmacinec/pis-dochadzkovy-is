from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('registration', views.registration, name='registration'),
    path('registrate', views.registrate, name='registrate'),
    path('complete-registration/<int:employee_id>', views.complete_registration, name='complete_registration'),
    path('employee/update', views.update_employee, name='update_employee'),

    path('sign-in', views.sign_in, name='sign_in'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout')
]
