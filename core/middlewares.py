from functools import cached_property
from typing import Any
from amazon.auth.base import Token
from django.utils.deprecation import MiddlewareMixin
import datetime
from datetime import datetime
from core.utils import save_data_to_session
import logging 

class TokenMiddleware(MiddlewareMixin):
    
    def process_view(self, request, view_func, view_args, view_kwargs):   
        print("Token Middleware Ran")
        if request.user.is_authenticated:
            
            if request.user.amazon_authorization:
                access_token = request.session.get("access_token") 
                if access_token:
                    if datetime.now() >=datetime.fromisoformat(request.session["validity"]):
                        token = Token()
                        token.user_data = request.user.cred
                        token.GenerateAccessToken(grant_type="refresh_token")
                        
                            
                        data = {"access_token": token.access_token, "validity": token.validity}
                        save_data_to_session(request, **data)
                
                else:
                    token = Token()
                    token.user_data = request.user.cred
                    token.GenerateAccessToken(grant_type="refresh_token")
                    
                    data = {"access_token": token.access_token, "validity": token.validity, "market_place_id": token.user_data.market_place_id}
                    save_data_to_session(request, **data)                                
                        