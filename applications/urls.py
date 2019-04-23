from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('new', views.new, name='new'),
    path('<int:id>', views.show, name='show'),
    path('<int:application_id>/approval/<int:approval_id>',views.approval_show,name='approval_show')
]
