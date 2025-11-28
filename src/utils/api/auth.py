import asyncio
import time

import jwt
from aiohttp import ClientSession

AUTH_API_URL = "https://pub.fsa.gov.ru/login"

# Default credentials for anon users
body = {
    "username": "anonymous",
    "password": "hrgesf7HDR67Bd",
}

AUTH_HEADER_KEYWORD = "Bearer "

# Simple in-memory cache
_CACHED_TOKEN = None
_CACHED_TOKEN_EXP = None
_CACHE_LOCK = asyncio.Lock()


def _decode_jwt_exp(token: str):
    try:
        # Используем pyjwt для декодирования токена без проверки подписи
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload.get("exp")
    except Exception:
        return None


def _is_token_fresh(exp: int, skew: int = 60):
    # skew: time in seconds to consider token "almost expired"
    return exp is not None and exp - skew > int(time.time())


async def get_auth_token():
    """
    Кеширует токен авторизации. Если токен протух, запрашивает новый.
    Проверяет свежесть токена по полю "exp" (JWT payload).
    """
    global _CACHED_TOKEN, _CACHED_TOKEN_EXP

    async with _CACHE_LOCK:
        if _CACHED_TOKEN and _is_token_fresh(_CACHED_TOKEN_EXP):
            return _CACHED_TOKEN

        async with ClientSession() as session:
            response = await session.post(
                url=AUTH_API_URL,
                json=body,
            )
            response.raise_for_status()

            auth_header = response.headers.get("Authorization")
            if not (auth_header and auth_header.startswith(AUTH_HEADER_KEYWORD)):
                raise Exception("Authorization token not found")

            token = auth_header[len(AUTH_HEADER_KEYWORD) :].strip()
            exp = _decode_jwt_exp(token)

            if exp is None:
                raise Exception("Can't decode JWT token's exp field")

            _CACHED_TOKEN = token
            _CACHED_TOKEN_EXP = exp
            return token
