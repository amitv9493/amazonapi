from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path("csrf", views.GetCSRFToken.as_view(), name="csrf"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("authenticate_amazon", views.authenticate_amazon.as_view(), name="authenticate_amazon"),
    path("callback", views.save_credentials.as_view(), name="save_credentials"),
    
]
