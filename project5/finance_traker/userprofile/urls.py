from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'userprofile'

urlpatterns= [
    # path('', views.userbase_view, name='user_profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transaction/', views.transaction, name='transaction'),
    path('delete_transaction/<int:id>', views.delete_transaction, name='delete_transaction'),
    path('update_transaction/<int:id>/', views.update_transaction, name='update_transaction'),
    path('category/', views.category, name='category')
]
