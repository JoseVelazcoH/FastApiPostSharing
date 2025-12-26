import requests
from requests.models import Response
from app.core.config import settings

def get_feed(token) -> Response:
    headers = _create_auth_headers(token)
    response = requests.get(f"{settings.base_url}/feed", headers=headers)
    return response

def delete_post(post_id, token) -> Response:
    headers = _create_auth_headers(token)
    response = requests.delete(f"{settings.base_url}/posts/{post_id}", headers=headers)
    return response

def upload_post(file_name, file_content, file_type, caption, token) -> Response:
    headers = _create_auth_headers(token)
    files = {"file": (file_name, file_content, file_type)}
    data = {"caption": caption}
    response = requests.post(f"{settings.base_url}/upload", files=files, data=data, headers=headers)
    return response

def _create_auth_headers(token):
    return {"Authorization": f"Bearer {token}"}
