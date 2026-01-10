from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

ai_draft_order_bp = Blueprint('ai_draft_order_bp', __name__)

@ai_draft_order_bp.route('/', methods=['POST'])
@token_required
@inject
def post_voice_command(ai_service = Provide[Container.ai_draft_order_service]):
    try:
        data = request.get_json()
        voice_text = data.get('voice_content')
        emp_id = getattr(request, 'current_user_id', None)
        
        result = ai_service.create_draft_from_voice(voice_text, emp_id)
        return jsonify({"draft_id": result.draft_id, "message": "Draft created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_draft_order_bp.route('/', methods=['GET'])
@token_required
@inject
def get_all_drafts(ai_service = Provide[Container.ai_draft_order_service]):
    try:
        drafts = ai_service.draft_repo.get_pending_drafts()
        output = [{
            "draft_id": d.draft_id,
            "recognized_content": d.recognized_content,
            "extracted_json": d.extracted_json,
            "created_at": d.created_at.isoformat()
        } for d in drafts]
        return jsonify(output), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_draft_order_bp.route('/<int:draft_id>/confirm', methods=['POST'])
@token_required
@inject
def confirm_draft(draft_id, ai_service = Provide[Container.ai_draft_order_service]):
    try:
        emp_id = getattr(request, 'current_user_id', None)
        result = ai_service.confirm_and_create_order(draft_id, emp_id)
        return jsonify({"message": "Order created successfully", "order_id": result.order_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400