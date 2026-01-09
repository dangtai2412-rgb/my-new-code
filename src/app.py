from flask import Flask
from flasgger import Swagger
from infrastructure.databases import init_db
from api.routes import register_routes
import infrastructure.models 



def create_app():
    app = Flask(__name__)
    

    # Cấu hình Swagger duy nhất, hỗ trợ nút Authorize (Ổ khóa)
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/",
        "securityDefinitions": {
            "BearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Nhập theo cú pháp: Bearer <token>"
            }
        }
    }

    Swagger(app, config=swagger_config)
    
    # Đăng ký các Route
    register_routes(app)

    try:
        init_db(app)
        print("✅ Kết nối Database thành công!")
    except Exception as e:
        print(f"❌ Lỗi DB: {e}")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=9999, debug=True)