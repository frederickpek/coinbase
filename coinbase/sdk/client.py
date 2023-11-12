import hmac
import hashlib
import time
import json
import requests
from coinbase.sdk.consts import (
    BASE_URL,
    CB_ACCESS_KEY,
    CB_ACCESS_SIGN,
    CB_ACCESS_TIMESTAMP,
    GET,
    POST,
)
from coinbase.utils import get_query_params_str


class Client:
    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign(
        self, method: str, endpoint: str, timestamp: str, payload: str = ""
    ) -> str:
        message = timestamp + method + endpoint + payload
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            message.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()
        return signature

    def _get_headers(self, method: str, endpoint: str, payload: str = "") -> dict:
        timestamp = str(int(time.time()))
        sign = self._sign(method, endpoint, timestamp, payload=payload)
        return {
            CB_ACCESS_KEY: self.api_key,
            CB_ACCESS_SIGN: sign,
            CB_ACCESS_TIMESTAMP: timestamp,
            "Content-Type": "application/json",
        }

    def request(
        self, method: str, endpoint: str, params: dict = {}, should_log=True
    ) -> dict:
        url = BASE_URL + endpoint
        payload = json.dumps(params) if (method == POST and params) else ""
        headers = self._get_headers(method, endpoint, payload=payload)

        if should_log:
            print(f"[Coinbase Request] -- {method} '{endpoint}', params: {params}")

        if method == GET:
            query_params = get_query_params_str(params=params)
            resp = requests.get(url + query_params, headers=headers)
        elif method == POST:
            resp = requests.post(url, headers=headers, data=payload)
        else:
            raise NotImplementedError

        data = resp.json()

        if should_log:
            print(f"[Coinbase Response] -- {data}")

        return data
