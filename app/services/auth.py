import requests
from app.core.config import settings
from requests.models import Response

def authenticate_user(email, password) -> Response:
    login_data = {"username": email, "password": password}
    response = requests.post(f"{settings.base_url}/auth/jwt/login", data=login_data)
    return response

def get_current_user(token) -> Response:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{settings.base_url}/users/me", headers=headers)
    return response

def register_user(email, password) -> Response:
    register_data = {"email": email, "password": password}
    response = requests.post(f"{settings.base_url}/auth/jwt/register", json=register_data)
    return response
