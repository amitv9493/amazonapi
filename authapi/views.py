
from django.shortcuts import redirect
from usercredential.models import user_credentials
from amazon.auth.base import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import permissions, authentication
from django.contrib.auth import get_user_model, login, logout
import os
from .serializers import LoginSerializer
from rest_framework import status
from django.middleware.csrf import get_token as get_csrf_token
import time
from core.utils import save_data_to_session
from django.views.decorators.csrf import csrf_exempt
from rest_framework import decorators
import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
# Create your views here.

@ensure_csrf_cookie
def get_csrf(request):
    response = JsonResponse({"detail": "CSRF cookie set"})
    response["X-CSRFToken"] = get_csrf_token(request)
    return response

@method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []


    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]

            login(request, user)
            return Response({"detail": "Successfully logged in"}, status=200)

class LogoutView(APIView):
    
    authentication_classes = [authentication.SessionAuthentication]
    
    def get(self, request, format=None):
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=200)
    


class authenticate_amazon(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    authentication_classes = [authentication.SessionAuthentication]

    def get(self, request):
        url_base = f"https://sellercentral.amazon.in/apps/authorize/consent?application_id={os.getenv('LWA_APP_ID')}&state={request.user.id}&version=beta"

        print(url_base)
        return redirect(url_base)


class save_credentials(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        # complete_uri = request.build_absolute_uri()

        data = request.query_params
        code = data.get("spapi_oauth_code")
        selling_partner_id = data.get("selling_partner_id")
        print(selling_partner_id)
        state = int(data.get("state"))
        print(code)
        user = get_user_model().objects.get(id=state)

        cred, _ = user_credentials.objects.get_or_create(user=user)
        cred.code = code
        cred.selling_partner_id = selling_partner_id
        cred.save()

        token = Token()
        token.user_data = cred
        try:
            token.GenerateAccessToken(grant_type="authorization_code")

        except ValueError as e:
            return Response(
                {"msg": f"Authorization failed Please re authorize {e}"}, status=400
            )

        cred.refresh_token = token.refresh_token
        cred.access_token = token.access_token
        data = {
            "refresh_token" : token.refresh_token,
            "access_token" : token.access_token,
            "validity": token.validity,
        }
        
        save_data_to_session(request, **data)
        cred.save()
        return Response({"msg": "Authenticated successfully !"}, status=200)
