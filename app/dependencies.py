from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from passlib.context import CryptContext

from app.config import Config

api_key_header = APIKeyHeader(name="Access-Token")

crypt_ctx = CryptContext(schemes=["bcrypt"])


async def get_api_key(api_key: str = Security(api_key_header)) -> str:
    # Verify the provided API key with the stored secret
    api_key_valid = crypt_ctx.verify(api_key, Config.API_KEY_SECRET)

    if not api_key_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )

    return api_key