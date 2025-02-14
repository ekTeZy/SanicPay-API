from app.db.session import AsyncSessionLocal
from app.utils.email_utils import validate_email
from app.utils.password_utils import validate_password
from app.middleware.protected import protected, admin_required
from app.repos.UserRepo import UserRepo
from app.repos.AdminRepo import AdminRepo
from sanic.exceptions import Forbidden, NotFound
from sanic.response import json
from sanic import Blueprint

users_bp = Blueprint("users_bp")
user_repo, admin_repo = UserRepo(), AdminRepo()
"""
Получение информации пользователем
"""




@users_bp.get("/api/v1/users/<user_id:int>")
@protected
async def get_user_data(request, user_id):
    
    auth_user = request.ctx.user
    if not auth_user:
        return json({"msg": "Unauthorized"}, status=401)

    if auth_user.get("id") != user_id:
        return json({"msg": "Access denied"}, status=403)

    try:
        async with AsyncSessionLocal() as db:
            user = await user_repo.get_user(db, user_id)
            if user is None:
                return json({"error": "User not found"}, status=404)
            
            response_data = {
                "id": str(user_id),
                "email": user.email,
                "full_name": user.full_name,
                "is_admin": str(user.is_admin == 1),
            }
            
            return json(response_data, 200)    

    except Exception as e:
        return json({"error": f"{str(e)}"}, status=500)
    

"""
CRUD операции админа
"""
    
@users_bp.post("/api/v1/users")
@protected
@admin_required
async def create_user(request):
    request_data = request.json
    
    email = request_data.get("email", "").strip()
    password = request_data.get("password", "").strip()
    full_name = request_data.get("full_name", "").strip()
    
    try:
    
        validate_email(email) and validate_password(password)            
        
        async with AsyncSessionLocal() as db:
            try:
                new_user = await admin_repo.create_user(
                    db=db, 
                    full_name=full_name,
                    email=email, 
                    password=password
                )
                response_data = {
                    "msg": "User created successfuly!",
                    "createdUserData": {
                        "id": f"{new_user.id}",
                        "email": f"{new_user.email}",
                        "full_name": f"{new_user.full_name}",
                        "is_admin": str(new_user.is_admin == 1),
                        "api_token": f"{new_user.api_token}"
                    }
                }
                
                return json(response_data, status=201)
            
            except Exception as e:
                return json({"error": f"{str(e)}"}, status=400)
    
    except Forbidden:
        return json(Forbidden)

    except Exception as e:
        return json({"error": f"{str(e)}"})
    

            
@users_bp.patch("/api/v1/users/<user_id:int>")
@protected
@admin_required
async def patch_user(request, user_id):
    
    user_id = user_id
    request_data = request.json
    new_password = request_data.get("password", "").strip()
    full_name = request_data.get("full_name", "").strip()
    
    if full_name == "":
        return json({"error": "Name must contain at least 1 symbol"}, status=400)

    try:

        validate_password(new_password)            
        
        async with AsyncSessionLocal() as db:
            try:
                patched_user = await admin_repo.patch_user(
                    db=db, 
                    user_id=user_id,
                    full_name=full_name,
                    new_password=new_password
                )

                response_data = {
                    "msg": "User patched successfuly!",
                    "patchedUserData": {
                        "id": str(user_id),
                        "email": patched_user.email,
                        "full_name": patched_user.full_name,
                        "is_admin": str(patched_user.is_admin == 1),
                        "api_token": patched_user.api_token
                    }
                }
                
                return json(response_data, status=200)

            except Exception as NotFound:
                return json(NotFound)
    
    except Forbidden:
        return json(Forbidden)
    
    except Exception as e:
        return json({"error": f"{str(e)}"}, status=500)
    
    

@users_bp.delete("/api/v1/users/<user_id:int>")
@protected
@admin_required
async def delete_user(request, user_id):
    
    user_id = user_id
    
    try:
        async with AsyncSessionLocal() as db:
            try:
                await admin_repo.delete_user(
                    db=db,
                    user_id=user_id
                )

                response_data = {
                    "msg": f"User with id == {user_id} deleted successfuly!",
                }
                
                return json(response_data, status=200)

            except NotFound:
                return json(NotFound)
            
    except Exception as e:
        return json({"error": f"{str(e)}"}, status=500)
    