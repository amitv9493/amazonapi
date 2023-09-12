
import requests
from usercredential.models import user_credentials
from amazon.auth.base import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, authentication
from rest_framework.pagination import PageNumberPagination
from amazon.orders import get_first_order, get_full_orders
from datetime import datetime
from core.utils import save_data_to_session
class AllOrdersView(APIView):

    pagination_class = PageNumberPagination

    def get(self, request, format=None):
            
        first_response = get_first_order(request)
        order_data = get_full_orders(request, first_response)
        
        return Response(order_data)
    


class SessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]
    
    def get(self, request):
        request.session["test"] = "New Value"
        return Response(request.session)
    
    
class OrderInstanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]
    
    def get(self, request,orderid):
        url = f"https://sellingpartnerapi-eu.amazon.com/orders/v0/orders/{orderid}/orderItems"

        # def get_orders(params=None):
        payload = {}
        token = request.session["access_token"]
        headers = {
            "x-amz-access-token": token,
        }
        params = {}
        response = requests.get(url, headers=headers, data=payload, params=params)
        
        return Response(response.json())
    

class BuyerInfoView(APIView):
    def get(self, request, orderid):
        pass