from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterationView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
