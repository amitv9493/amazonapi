
from django.shortcuts import redirect
from usercredential.models import user_credentials
from amazon.auth.base import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, authentication
from django.contrib.auth import get_user_model, login, logout
import os
from core.utils import save_data_to_session
from rest_framework import decorators
from django.utils import decorators
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

@decorators.method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = [permissions.AllowAny,]
    def get(self, request, format=None):
        
        get_csrf = get_token(request)
        token = request.COOKIES.get('csrftoken')
        return Response({"csrfToken":get_csrf
                         
                         }, 200)
    
@decorators.method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []


    def post(self, request, format=None):
        
        username  = request.data.get("username")
        password  = request.data.get("password")
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            print()
            return Response({"success": "Successfully logged in",
                             "sessionid":request.session.session_key,
                             "csrftoken":request.COOKIES.get('csrftoken')
                             }, status=200)
        
        else:
            return Response({"error": "Invalid credentials"}, status=400)
   
   
@decorators.method_decorator(ensure_csrf_cookie, name='dispatch')  
class LogoutView(APIView):
    
    def post(self, request, format):
        try:
            logout(request)
            return Response({"detail": "logged out."}, status=200)
        
        except Exception as e:
            return Response({"error":"Something went wrong"}, status=400)
        


class authenticate_amazon(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    authentication_classes = [JWTAuthentication]

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
