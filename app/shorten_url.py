import hashlib
import base64

async def shorten_url(url: str):
    encoded_str = base64.urlsafe_b64encode(
        hashlib.sha256(url.encode()).digest()).decode()
    return encoded_str[:7]
