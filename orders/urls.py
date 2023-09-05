from django.urls import path
from . import views
urlpatterns = [
    path("", views.AllOrdersView.as_view(), name="orders"),
    path("session/", views.SessionView.as_view(), name="session"),
    path("instance/<str:orderid>/", views.OrderInstanceView.as_view(), name="order_instance"),
    path("<str:orderid>/buyerInfo/", views.BuyerInfoView.as_view(), name="buyer_info"),
]
