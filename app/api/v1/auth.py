from app.db.session import AsyncSessionLocal
from app.utils.email_utils import validate_email
from app.repos.UserRepo import UserRepo
from sanic.response import json
from sanic import Blueprint

auth_bp = Blueprint("auth_bp")

user_repo = UserRepo()

@auth_bp.post("/api/v1/auth")
async def auth_user(request):
    request_data = request.json
    
    email = request_data.get("email", "").strip()
    plain_password = request_data.get("password", "").strip()

    if not email or not plain_password:
        return json({"error": "Email and password are required"}, status=400)

    if not validate_email(email=email):
        return json({"error": "Invalid email format"}, status=400)
    
    try:
        async with AsyncSessionLocal() as db:
            user = await user_repo.authenticate_user(db=db, email=email, password=plain_password)
            if user is None:
                return json({"error": f"Invalid email or password"}, status=401)

            response_data = {
                "msg": "Successful auth",
                "userProperties": {
                    "id": str(user.id),
                    "email": user.email,
                    "full_name": user.full_name,
                    "is_admin": str(user.is_admin == 1),
                    "api_token": user.api_token
                }        
            } 
            
            return json(response_data, status=201)
    
    except Exception as ServerError:
        return json({"msg": f"Server error: {str(ServerError)}"}, status=500)
