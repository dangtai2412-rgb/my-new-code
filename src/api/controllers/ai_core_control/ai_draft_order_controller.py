# src/api/controllers/ai_core_control/ai_draft_order_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

ai_draft_order_bp = Blueprint('ai_draft_order_bp', __name__)

@ai_draft_order_bp.route('/', methods=['POST'])
@token_required
@inject
def create_ai_draft(ai_service = Provide[Container.ai_draft_order_service]):
    """AI tạo đơn hàng nháp từ giọng nói"""
    try:
        data = request.get_json()
        # Lấy ID nhân viên từ token để biết ai là người tạo
        data['employee_id'] = getattr(request, 'current_user_id', None)
        
        result = ai_service.create_draft_from_voice(data)
        return jsonify({"draft_id": result.draft_id, "message": "Đã tạo bản nháp"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_draft_order_bp.route('/', methods=['GET'])
@token_required
@inject
def get_drafts(ai_service = Provide[Container.ai_draft_order_service]):
    """Lấy danh sách đơn nháp (Dùng cho Frontend hiển thị)"""
    try:
        # Bạn cần đảm bảo trong Repo hoặc Service có hàm lấy tất cả đơn Pending
        drafts = ai_service.draft_repo.session.query(Container.draft_repo().model).filter_by(confirmation_status="Pending").all()
        # Chuyển đổi list object sang json (Ví dụ đơn giản)
        output = []
        for d in drafts:
            output.append({
                "draft_id": d.draft_id,
                "recognized_content": d.recognized_content,
                "extracted_json": d.extracted_json,
                "confirmation_status": d.confirmation_status,
                "created_at": d.created_at.isoformat() if d.created_at else None
            })
        return jsonify(output), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_draft_order_bp.route('/<int:draft_id>/confirm', methods=['POST'])
@token_required
@inject
def confirm_draft(draft_id, ai_service = Provide[Container.ai_draft_order_service]):
    """Xác nhận đơn nháp để tạo đơn hàng thật"""
    try:
        employee_id = getattr(request, 'current_user_id', None)
        result = ai_service.confirm_and_create_order(draft_id, employee_id)
        return jsonify({"message": "Xác nhận thành công", "order_id": result.order_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400