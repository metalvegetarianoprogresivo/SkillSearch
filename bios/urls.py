from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='bios_index'),
    path('get_documents/', views.get_documents, name='get_documents'),
    path('send_logs/', views.send_logs, name='send_logs'),
]
