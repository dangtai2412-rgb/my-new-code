# src/api/controllers/ai_core_control/ai_draft_order_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

ai_draft_order_bp = Blueprint('ai_draft_order_bp', __name__)

@ai_draft_order_bp.route('/', methods=['POST'])
@token_required
@inject
def post_voice_command(ai_service = Provide[Container.ai_draft_order_service]):
    """
    Gửi lệnh thoại/văn bản để AI trích xuất đơn hàng
    ---
    tags: [AI Draft Orders]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          properties:
            voice_content: {type: string, example: "Bán cho anh Nam 5 bao xi măng Hà Tiên, ghi nợ nhé"}
    responses:
      201: {description: "Đã tạo đơn hàng nháp"}
    """
    try:
        data = request.get_json()
        emp_id = getattr(request, 'current_user_id', None)
        result = ai_service.create_draft_from_voice(data.get('voice_content'), emp_id)
        return jsonify({"draft_id": result.draft_id, "message": "Draft created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_draft_order_bp.route('/', methods=['GET'])
@token_required
@inject
def get_drafts(ai_service = Provide[Container.ai_draft_order_service]):
    """
    Lấy danh sách các đơn hàng nháp đang chờ xác nhận
    ---
    tags: [AI Draft Orders]
    security: [{BearerAuth: []}]
    responses:
      200: {description: "Danh sách bản nháp"}
    """
    drafts = ai_service.draft_repo.get_pending_drafts()
    return jsonify([{
        "id": d.draft_id,
        "content": d.recognized_content,
        "json": d.extracted_json,
        "time": d.created_at.isoformat()
    } for d in drafts]), 200

@ai_draft_order_bp.route('/<int:draft_id>/confirm', methods=['POST'])
@token_required
@inject
def confirm_draft(draft_id, ai_service = Provide[Container.ai_draft_order_service]):
    """
    Xác nhận đơn nháp để tạo Hóa đơn và ghi nợ thật
    ---
    tags: [AI Draft Orders]
    security: [{BearerAuth: []}]
    responses:
      200: {description: "Đã tạo hóa đơn thật thành công"}
    """
    try:
        emp_id = getattr(request, 'current_user_id', None)
        order = ai_service.confirm_and_create_order(draft_id, emp_id)
        return jsonify({"message": "Order created", "order_id": order.order_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400