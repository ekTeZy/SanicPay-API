from sanic.response import json
from app.db.session import AsyncSessionLocal
from functools import wraps
from app.repos.UserRepo import UserRepo

def protected(func):
    """Декоратор для проверки API-токена"""
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization", None)
        
        if not auth_header or not auth_header.startswith("Token "):
            return json({"msg": "Missing or invalid Authorization header"}, status=401)

        api_token = auth_header.split(" ")[1]

        async with AsyncSessionLocal() as db:
            user_repo = UserRepo()
            user = await user_repo.get_user_by_token(db, api_token)
            if user is None:
                return json({"msg": "Invalid API token"}, status=401)

            request.ctx.user = {
                "id": user.id,
                "email": user.email,
                "is_admin": user.is_admin
            }

        return await func(request, *args, **kwargs)

    return wrapper


def admin_required(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        if not hasattr(request.ctx, "user") or not request.ctx.user.get("is_admin"):
            return json({"msg": "Admin access required"}, status=403)
        return await func(request, *args, **kwargs)
    
    return wrapper