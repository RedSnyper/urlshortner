import hashlib
import base64
import uuid

async def get_url_code(url: str):
    encoded_str = base64.urlsafe_b64encode(
        hashlib.sha256(url.encode()).digest()).decode()
    return encoded_str[:7]



async def get_uuid():
    return uuid.uuid1().hex
