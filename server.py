from sanic import Sanic
from sanic.response import json

from app.core.config import settings

from app.api.v1.auth import auth_bp
from app.api.v1.users import users_bp
from app.api.v1.payments import payments_bp
from app.api.v1.accounts import account_bp

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> Sanic:
    app = Sanic("SanicPay")
    app.update_config(settings)

    app.blueprint(auth_bp)
    app.blueprint(users_bp)    
    app.blueprint(account_bp)
    app.blueprint(payments_bp)
        
    @app.get("/")
    async def check_app(request):
        return json({"status": "ok"})   
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
