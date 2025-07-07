from django.urls import path
from . import views

urlpatterns = [
    path('', views.optimizar_view, name='optimizar'),
]