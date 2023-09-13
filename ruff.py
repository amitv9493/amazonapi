from sp_api.base import Marketplaces
from sp_api.api import Orders
import datetime
from datetime import timedelta

from dotenv import load_dotenv
load_dotenv()
# order_client = Orders(marketplace=Marketplaces.UK)
# order = order_client.get_order('your-order-id')
# print(order) # `order` is an `ApiResponse`
# print(order.payload) # `payload` contains the original response
# Orders().get_orders(CreatedAfter=(datetime.utcnow() - timedelta(days=7)).isoformat())

Orders().get_orders(CreatedAfter='TEST_CASE_200', MarketplaceIds=["ATVPDKIKX0DER"])