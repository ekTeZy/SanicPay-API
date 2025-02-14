from app.db.session import AsyncSessionLocal
from app.middleware.protected import protected, admin_required
from app.repos.UserAccountRepo import UserAccountRepo
from app.repos.AdminRepo import AdminRepo
from sanic.response import json
from sanic import Blueprint

account_bp = Blueprint("account_bp")
user_account_repo, admin_repo = UserAccountRepo(), AdminRepo()

"""
Получение информации по аккаунтам и балансам
"""

@account_bp.get("/api/v1/accounts/<user_id:int>")
@protected
async def get_user_accounts(request, user_id):
    
    auth_user = request.ctx.user

    if not auth_user:
        return json({"msg": "Unauthorized"}, status=401)

    if auth_user.get("id") != user_id:
        return json({"msg": "Access denied"}, status=403)
 
    
    try:   
        async with AsyncSessionLocal() as db:
            try:
                all_accounts = await user_account_repo.get_accounts_data(db, user_id)
                
                response_data = []
                
                for account in all_accounts:
                    response_data.append({
                        "userID": str(user_id),
                        "accountId": str(account.id),
                        "balance": str(account.balance)
                    })
                
                return json(response_data, 200)    
            
            except Exception as e:
                return json({"error": f"{str(e)}"}, status=400)
            
    except Exception as e:
        return json({"error": f"{str(e)}"}, status=500)
    

@account_bp.get("/api/v1/accounts")
@protected
@admin_required
async def get_users_and_accounts(request):
    
    try:   
        async with AsyncSessionLocal() as db:
            users_and_accounts = await admin_repo.get_all_users_accounts(db)
            
            response_data = []
            
            for user in users_and_accounts:
                accounts = user.accounts
                for account in accounts:
                    
                    if account:
                        response_data.append({
                            "userID": str(user.id),
                            "email": user.email,
                            "accountId": str(account.id),
                            "balance": str(account.balance)
                        })
                    
                    else:
                        response_data.append({
                            "userID": str(user.id),
                            "email": user.email,
                            "accountId": None,
                            "balance": str(account.balance)                            
                        })
            
            return json(response_data, 200)    
            
    except Exception as e:
        return json({"error": f"{str(e)}"}, status=500)