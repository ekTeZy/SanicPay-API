from sanic import Blueprint
from sanic.response import json
from sanic.exceptions import Forbidden, BadRequest
from app.db.session import AsyncSessionLocal
from app.core.config import settings
from app.middleware.protected import protected
from app.repos.UserAccountRepo import UserAccountRepo
from app.repos.PaymentRepo import PaymentRepo

import hashlib

secret_key = settings.SECRET_KEY
user_account_repo, payment_repo = UserAccountRepo(), PaymentRepo()

payments_bp = Blueprint("payments_bp")

@payments_bp.post("/api/v1/webhook")
async def process_payment(request):

    try:
        payment_data = request.json

        transaction_id = payment_data["transaction_id"]
        user_id = int(payment_data["user_id"])
        account_id = int(payment_data["account_id"])
        amount = float(payment_data["amount"])

        data_string = f"{account_id}{amount}{transaction_id}{user_id}{secret_key}"
        request_signature = hashlib.sha256(data_string.encode()).hexdigest()

        async with AsyncSessionLocal() as db:
            payment, account = await payment_repo.process_webhook(
                db=db, 
                transaction_id=transaction_id, 
                user_id=user_id, 
                account_id=account_id, 
                amount=amount, 
                request_signature=request_signature
            )
            
            response_data = {
                "msg": "Balance replenished successfuly!",
                "paymentData": {
                    "id": str(payment.id),
                    "transaction_id": str(payment.transaction_id),
                    "account_id": str(payment.account_id),
                    "user_id": str(payment.user_id),
                    "amount": str(payment.amount)
                },
                "accountData": {
                    "id": str(account_id),
                    "user_id": str(user_id),
                    "balance": str(account.balance)
                }
            }

        return json(response_data, status=201)

    except Forbidden as e:
        return json({"error": str(e)}, status=403)

    except BadRequest as e:
        return json({"error": str(e)}, status=400)
    
    except Exception as e:
        return json({"error": f"{str(e)}"}, status=500)


@payments_bp.get("/api/v1/payments/<user_id:int>")
@protected
async def get_user_payments(request, user_id):
    
    auth_user = request.ctx.user
    if not auth_user:
        return json({"msg": "Unauthorized"}, status=401)

    if auth_user.get("id") != user_id:
        return json({"msg": "Access denied"}, status=403)
    
    try:   
        async with AsyncSessionLocal() as db:
            try:
                all_payments = await user_account_repo.get_payments_list(db, user_id)
                
                response_data = []
                
                for payment in all_payments:
                    response_data.append({
                        "userID": str(user_id),
                        "paymentID": str(payment.id),
                        "transactionId": str(payment.transaction_id),
                        "amount": str(payment.amount),
                        "signature": payment.signature
                    })
                
                return json(response_data, 200)    
            
            except Exception as e:
              return json({"error": f"{str(e)}"}, status=400)
            
    except Exception as e:
        return json({"error": f"{str(e)}"}, status=500)