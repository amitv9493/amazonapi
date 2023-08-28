
import requests
from django.shortcuts import redirect
from usercredential.models import user_credentials
from amazon.auth.base import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, authentication
from django.contrib.auth import get_user_model, authenticate, login
import os

token = Token()


class authenticate_amazon(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    authentication_classes = [authentication.BasicAuthentication]

    def get(self, request):
        url_base = f"https://sellercentral.amazon.in/apps/authorize/consent?application_id={os.getenv('LWA_APP_ID')}&state={request.user.id}&version=beta"

        return redirect(url_base)


class save_credentials(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        complete_uri = request.build_absolute_uri()
        print(complete_uri)

        data = request.query_params
        code = data.get("spapi_oauth_code")
        selling_partner_id = data.get("selling_partner_id")
        state = int(data.get("state"))

        user = get_user_model().objects.get(id=state)

        cred, _ = user_credentials.objects.get_or_create(user=user)
        cred.code = code
        cred.selling_partner_id = selling_partner_id
        cred.save()

        get_token(user=user, grant_type="authorization_code", request=None)

        return Response({"msg": "success"}, status=200)


def get_token(user, grant_type, request=None):
    url = "https://api.amazon.com/auth/o2/token"

    user_data = user_credentials.objects.get(user=user)

    if grant_type == "authorization_code":
        token = user_data.code
        type = "code"
    elif grant_type == "refresh_token":
        token = user_data.refresh_token
        type = "refresh_token"

    payload = f"grant_type={grant_type}&{type}={token}&client_id={os.getenv('client_id')}&client_secret={os.getenv('client_secret')}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, headers=headers, data=payload)

    token_data = response.json()
    print(token_data)

    if token_data.get("error"):
        return Response(token_data, status=400)

    user_data.access_token = token_data.get("access_token")
    user_data.refresh_token = token_data.get("refresh_token")

    user_data.save()


def set_session_token(request, user_data):
    request.session["access_token"] = user_data.access_token




class Orders(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        # JWTAuthentication,
        authentication.BasicAuthentication,
        authentication.SessionAuthentication,
    ]

    def get(self, request, format=None):
        data = user_credentials.objects.filter(user=request.user).first()
        token.user_data = data
        print(token.access_token)
        created_after = request.query_params.get("created_after", None)
        url = f"https://sellingpartnerapi-eu.amazon.com/orders/v0/orders?MarketplaceIds={data.market_place_id}&CreatedAfter={created_after}"
        sandbox_url = f"https://sandbox.sellingpartnerapi-eu.amazon.com/orders/v0/orders?MarketplaceIds={data.market_place_id}&CreatedAfter=TEST_CASE_200"

        def get_orders():
            payload = {}

            headers = {
                "x-amz-access-token": token.access_token,
            }
            response = requests.get(sandbox_url, headers=headers, data=payload)
            return response

        response = get_orders()
        if 400 <= response.status_code <= 499:
            # get_token(request=request, user=request.user, grant_type="refresh_token")
            token.GenerateAccessToken(grant_type="refresh_token")
            print(token.access_token)

            response = get_orders()
        elif response.status_code >=500:
            return Response({"error": "Internal Server occured"}, status=500)
        print(response)
        print(response.status_code)
        return Response(response.json(), status=200)


class hello(APIView):
    permission_classes = [permissions.AllowAny]
    # authentication_classes = [authentication.a]
    
    def post(self, request):
        return Response("hello", status=200)
        
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get("username")
            password = serializer.data.get("password")
            
            user = authenticate(username=username, password=password)
            
            if user:
                login(request, user)
                
            return Response({"msg":"logged In successfully"},status=200)