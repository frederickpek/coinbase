from coinbase.sdk.client import Client
from coinbase.sdk.consts import (
    CANCEL_ORDERS,
    LIST_ORDERS,
    LIST_ACCOUNTS,
    GET_ACCOUNT,
    LIST_PRODUCTS,
    GET_PRODUCT,
    GET,
    POST,
)
from typing import List


class CoinbaseApi(Client):
    def get_account(self, account_uuid: str, should_log=True) -> dict:
        endpoint = GET_ACCOUNT.format(account_uuid)
        data = self.request(GET, endpoint, should_log=should_log)
        account: dict = data["account"]
        return account

    def get_accounts(self, should_log=True) -> List[dict]:
        data = self.request(GET, LIST_ACCOUNTS, should_log=should_log)
        accounts: List[dict] = data["accounts"]
        return list(filter(lambda x: float(x["available_balance"]["value"]), accounts))

    def get_product(self, product_id: str, should_log=True) -> dict:
        endpoint = GET_PRODUCT.format(product_id)
        data = self.request(GET, endpoint, should_log=should_log)
        return data

    def get_products(self, product_type: str = None, should_log=True) -> List[dict]:
        # product_type: SPOT & FUTURE, default is SPOT
        params = {}
        if product_type:
            params["product_type"] = product_type
        data = self.request(GET, LIST_PRODUCTS, params=params, should_log=should_log)
        products: List[dict] = data["products"]
        return products

    def get_open_orders(self, should_log=True) -> List[dict]:
        params = {"order_status": "OPEN"}
        data = self.request(GET, LIST_ORDERS, params=params, should_log=should_log)
        open_orders: List[dict] = data["orders"]
        return open_orders

    def cancel_orders(self, order_ids: List[str], should_log=True) -> List[dict]:
        if not order_ids:
            return list()
        params = {"order_ids": order_ids}
        data = self.request(POST, CANCEL_ORDERS, params=params, should_log=should_log)
        results: List[dict] = data["results"]
        return results

    def cancel_all_orders(self, should_log=True) -> List[dict]:
        open_orders = self.get_open_orders(should_log=should_log)
        order_ids = list(map(lambda x: x["order_id"], open_orders))
        results = self.cancel_orders(order_ids=order_ids, should_log=should_log)
        return results
