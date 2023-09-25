from django.urls import path
from . import views

urlpatterns = [
    path("csrf/", views.get_csrf, name="csrf"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("authenticate_amazon/", views.authenticate_amazon.as_view(), name="authenticate_amazon"),
    path("callback/", views.save_credentials.as_view(), name="save_credentials"),
    
]
