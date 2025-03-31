# user_management/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'), #Retrieve user profile(GET) & Update user profile(PUT)
    path('password/change/', ChangePasswordView.as_view(), name='change_password'),
    path('address/', AddressListCreateView.as_view(), name='list-create-address'), #List all addresses (POST) & Create user address
    path('role/assign/',RoleAssignmentView.as_view(), name='role-assign'), #Assign role to user(POST)
    
]