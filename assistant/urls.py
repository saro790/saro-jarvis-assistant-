from django.urls import path
from assistant import views

urlpatterns = [
    path('', views.home, name='home'),  # root URL
    # add other URLs if needed
]

