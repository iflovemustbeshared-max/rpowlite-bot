import requests
import os

BASE_URL = "https://rpow.hopeware.ltd"

class RpowClient:
    def __init__(self):
        self.session = requests.Session()
        # Potentially add headers if needed, based on HAR analysis
        # self.session.headers.update({
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
        # })

    def get_challenge(self):
        url = f"{BASE_URL}/beta/challenge"
        response = self.session.post(url)
        response.raise_for_status()
        return response.json()

    def submit_mint(self, challenge_id, solution_nonce):
        url = f"{BASE_URL}/beta/mint"
        payload = {
            "challenge_id": challenge_id,
            "solution_nonce": str(solution_nonce)
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_my_info(self):
        url = f"{BASE_URL}/alpha/me"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_chat_messages(self, since=None):
        url = f"{BASE_URL}/alpha/chat"
        params = {}
        if since:
            params["since"] = since
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
