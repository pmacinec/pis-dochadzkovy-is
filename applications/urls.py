from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('new', views.new, name='new'),
    path('<int:id>', views.show, name='show'),
    path('<int:application_id>/approval/<int:approval_id>', views.approval_show, name='approval_show'),
    path('<int:application_id>/conversation/<int:manager_id>', views.conversation, name='conversation'),
    path('<int:application_id>/conversation/<int:manager_id>/send-message', views.send_message, name='send_message')
]
