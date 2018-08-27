from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_roster_bios, name='get_roster_bios'),
    path('add/', views.add_to_roster, name='add_to_roster'),
    path('remove/', views.remove_from_roster, name='remove_from_roster'),
    path('detail/', views.roster_detail, name='roster_detail'),
    path('send/', views.send_roster, name='send_roster')
]
