from django.urls import path
from .views import login
# proyectoPor
urlpatterns = [
    path('',login,name="login"),
    
]
