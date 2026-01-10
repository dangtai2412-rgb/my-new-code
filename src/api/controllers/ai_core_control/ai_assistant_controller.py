# src/api/controllers/ai_core_control/ai_assistant_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

ai_assistant_bp = Blueprint('ai_assistant_bp', __name__)

@ai_assistant_bp.route('/settings', methods=['POST'])
@token_required
@inject
def update_settings(ai_service = Provide[Container.ai_assistant_service]):
    """
    Cập nhật cấu hình model AI
    ---
    tags: [AI Assistant]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          properties:
            version: {type: string, example: "v1.5"}
            model_type: {type: string, example: "gemini-1.5-flash"}
    responses:
      200: {description: "Thành công"}
    """
    try:
        data = request.get_json()
        ai_service.update_ai_settings(data)
        return jsonify({"message": "Settings updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_assistant_bp.route('/config', methods=['GET'])
@token_required
@inject
def get_config(ai_service = Provide[Container.ai_assistant_service]):
    """
    Lấy cấu hình AI hiện tại
    ---
    tags: [AI Assistant]
    security: [{BearerAuth: []}]
    responses:
      200: {description: "Thông tin cấu hình"}
    """
    config = ai_service.get_current_config()
    return jsonify({"version": config.version, "model": config.ai_model_type}) if config else ({}, 404)