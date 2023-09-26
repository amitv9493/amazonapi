
from django.shortcuts import redirect
from usercredential.models import user_credentials
from amazon.auth.base import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.http import HttpResponse
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
from django.utils import decorators
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate
from django.views.decorators.http import require_http_methods
# Create your views here.
def csrf_token(request):
    response = HttpResponse()
    csrf = get_csrf_token(request)
    response.set_cookie(key='csrftoken', value=csrf)
    return response


@require_http_methods(["POST"])
def LoginView(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return JsonResponse({"msg": "Invalid credentials"}, status=400)
    
    else:
        login(request, user)
        return JsonResponse({"msg": "Logged in successfully"}, status=200)
        

def LogoutView(request):
    logout(request)
    return JsonResponse({"msg": "Logged out successfully"}, status=200)

    

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
