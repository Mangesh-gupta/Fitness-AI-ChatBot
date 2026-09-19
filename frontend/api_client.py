import os
import json
import requests
from typing import Optional, Dict, Any, Generator

class FitnessAPIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip("/")

    def _headers(self, token: Optional[str] = None) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    # ==================== Auth ====================

    def register(self, username: str, email: str, password: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/auth/register"
        resp = requests.post(url, json={"username": username, "email": email, "password": password})
        if resp.status_code != 201:
            raise Exception(resp.json().get("detail", "Registration failed"))
        return resp.json()

    def login(self, username_or_email: str, password: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/auth/login"
        resp = requests.post(url, json={"username_or_email": username_or_email, "password": password})
        if resp.status_code != 200:
            raise Exception(resp.json().get("detail", "Login failed"))
        return resp.json()

    def get_me(self, token: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/auth/me"
        resp = requests.get(url, headers=self._headers(token))
        if resp.status_code != 200:
            raise Exception("Failed to fetch user data")
        return resp.json()

    # ==================== Profile ====================

    def get_profile(self, token: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/profile"
        resp = requests.get(url, headers=self._headers(token))
        if resp.status_code != 200:
            raise Exception("Failed to load profile")
        return resp.json()

    def update_profile(self, token: str, data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/api/profile"
        resp = requests.put(url, json=data, headers=self._headers(token))
        if resp.status_code != 200:
            raise Exception(resp.json().get("detail", "Failed to update profile"))
        return resp.json()

    # ==================== Sessions ====================

    def list_sessions(self, token: str):
        url = f"{self.base_url}/api/sessions"
        resp = requests.get(url, headers=self._headers(token))
        if resp.status_code != 200:
            return []
        return resp.json()

    def create_session(self, token: str, title: str = "New Fitness Consultation") -> Dict[str, Any]:
        url = f"{self.base_url}/api/sessions"
        resp = requests.post(url, json={"title": title}, headers=self._headers(token))
        if resp.status_code != 201:
            raise Exception("Failed to create session")
        return resp.json()

    def get_session(self, token: str, session_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/sessions/{session_id}"
        resp = requests.get(url, headers=self._headers(token))
        if resp.status_code != 200:
            raise Exception("Failed to load session details")
        return resp.json()

    def delete_session(self, token: str, session_id: str):
        url = f"{self.base_url}/api/sessions/{session_id}"
        requests.delete(url, headers=self._headers(token))

    # ==================== Chat ====================

    def send_chat(self, token: str, session_id: str, message: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/chat"
        resp = requests.post(
            url,
            json={"session_id": session_id, "message": message, "stream": False},
            headers=self._headers(token)
        )
        if resp.status_code != 200:
            raise Exception(resp.json().get("detail", "Chat error"))
        return resp.json()

    def stream_chat(self, token: str, session_id: str, message: str) -> Generator[Dict[str, Any], None, None]:
        url = f"{self.base_url}/api/chat"
        resp = requests.post(
            url,
            json={"session_id": session_id, "message": message, "stream": True},
            headers=self._headers(token),
            stream=True
        )
        if resp.status_code != 200:
            raise Exception(f"Chat stream error: {resp.status_code}")

        for line in resp.iter_lines():
            if line:
                decoded = line.decode("utf-8")
                if decoded.startswith("data: "):
                    payload = decoded[6:]
                    try:
                        data = json.loads(payload)
                        yield data
                    except json.JSONDecodeError:
                        continue

    # ==================== Products ====================

    def get_products(self):
        url = f"{self.base_url}/api/products"
        resp = requests.get(url)
        if resp.status_code != 200:
            return []
        return resp.json()
