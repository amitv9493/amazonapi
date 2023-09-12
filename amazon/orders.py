
import requests
from .auth.base import Token
import datetime

def get_first_order(request,created_after:str=None,params={}):
    # request.session
    user_data = request.user.cred
    payload = {}
    access_token = request.session["access_token"]
    headers = {
        "x-amz-access-token": access_token,
    }
    
    if not created_after:
        created_after = datetime.datetime.now() - datetime.timedelta(weeks=1)
        created_after = created_after.isoformat()
        
    url = f"https://sellingpartnerapi-eu.amazon.com/orders/v0/orders/?MarketplaceIds={user_data.market_place_id}&CreatedAfter={created_after}"
    sandbox_url = f"https://sandbox.sellingpartnerapi-eu.amazon.com/orders/v0/orders?MarketplaceIds=ATVPDKIKX0DER&CreatedAfter=TEST_CASE_200"
    
    
    response_data = requests.get(sandbox_url, headers=headers, data=payload, params=params)
    
    if response_data.status_code != 200:
        raise Exception(response_data.json())
    
    return response_data
    
def get_full_orders(request,first_response):
    order_data = {}
    order_data["data"] = first_response.json()["payload"]["Orders"]
    
    NextToken = first_response.json()["payload"].get("NextToken", None)
    
    while NextToken is not None:
        params = {"NextToken": NextToken}
        print("paginating")
        try:
            response = get_first_order(request,params=params)
            
        except Exception as e:
            return {"error": str(e)}
        
        try:
            order_data["data"].extend(response.json()["payload"]["Orders"])
            NextToken = response.json()["payload"]["NextToken"]
        except KeyError:
            NextToken = None
    
    order_data["count"] = len(order_data["data"])
    return order_data