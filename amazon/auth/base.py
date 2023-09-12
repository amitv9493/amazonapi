import os
import requests
from datetime import timedelta

from datetime import datetime
class Token:
    url = "https://api.amazon.com/auth/o2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    def __init__(
        self,
    ) -> None:
        self._user_data = None
        self._access_token = None
        self._refresh_token = None
        self.validity = None
        
    def initial_data(self):
        try:
            self._access_token = self._user_data.access_token
            self._refresh_token = self._user_data.refresh_token  
        except:
            pass
        
        return self
        
    def GenerateAccessToken(self, grant_type: str) -> None:
        
        if grant_type == "authorization_code":
            token = self._user_data.code
            type = "code"
            
        elif grant_type == "refresh_token":
            token = self._user_data.refresh_token
            type = "refresh_token"

        payload = f"grant_type={grant_type}&{type}={token}&client_id={os.getenv('client_id')}&client_secret={os.getenv('client_secret')}"

        response = requests.post(self.url, headers=self.headers, data=payload)

        token_data = response.json()
        # print(token_data)
        if token_data.get("error"):
            raise ValueError(f"Got this error \
                             {token_data.get('error')} \
                             with status code {response.status_code}")
        
        elif response.status_code == 200:
            self._access_token = token_data.get(
                "access_token"
            )
            self._refresh_token = token_data.get(
                "refresh_token"
            )
            
            self.validity = (datetime.now() + timedelta(seconds=3600)).isoformat()

    @property
    def access_token(self) -> str:
        return self._access_token

    @property
    def refresh_token(self) -> str:
        return self._refresh_token
    
    @property
    def user_data(self):
        return self._user_data
    
    @user_data.setter
    def user_data(self,user_data:object):
        self._user_data = user_data
        
