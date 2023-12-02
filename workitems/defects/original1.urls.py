from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('listinfra', views.list_infra, name='list_infra'),
    path('liststorage', views.list_storage, name='list_storage'),
    path('listinterface', views.list_interface, name='list_interface'),
    path('listframework', views.list_framework, name='list_framework'),
    path('listtechm', views.list_techm, name='list_techm'),
    path('listnovalink', views.list_novalink, name='list_novalink'),
    path('listexternal', views.list_external, name='list_external'),
]
