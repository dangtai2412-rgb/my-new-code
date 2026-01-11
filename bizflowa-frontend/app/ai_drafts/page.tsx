"use client";

import { useEffect, useState } from "react";
import api from "@/lib/axios";
import { Check, X, Bot, User, Package, CreditCard, Mic } from "lucide-react";

interface AIDraftItem {
  product_name: string;
  quantity: number;
}

interface AIDraft {
  draft_id: number;
  recognized_content: string;
  extracted_json: string; 
  confirmation_status: string;
  created_at: string;
}

export default function AIDraftsPage() {
  const [drafts, setDrafts] = useState<AIDraft[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchDrafts = async () => {
    try {
      // Sửa URL cho khớp với Backend
      const res = await api.get("/ai_draft_order/"); 
      setDrafts(res.data);
    } catch (error) {
      console.error("Lỗi lấy dữ liệu:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDrafts();
  }, []);

  const handleConfirm = async (id: number) => {
    try {
      await api.post(`/ai_draft_order/${id}/confirm`);
      alert("Xác nhận đơn hàng thành công! Đã trừ kho và ghi nợ.");
      fetchDrafts(); 
    } catch (err: any) {
      alert("Lỗi: " + (err.response?.data?.error || "Không xác định"));
    }
  };

  if (loading) return <div className="p-8 text-center">Đang tải dữ liệu AI...</div>;

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <Bot className="text-blue-600" /> Đơn hàng AI nháp
          </h1>
          <p className="text-gray-500">Xem và xác nhận các đơn hàng được trích xuất từ giọng nói</p>
        </div>
        
        {/* Nút Micro (Thành viên Người 6 sẽ viết logic ghi âm ở đây) */}
        <button className="flex items-center gap-2 bg-red-600 text-white px-4 py-2 rounded-full hover:bg-red-700 transition-all shadow-lg animate-pulse">
          <Mic size={20} /> Bấm để nói
        </button>
      </div>

      {drafts.length === 0 ? (
        <div className="bg-blue-50 border-2 border-dashed border-blue-200 rounded-xl p-12 text-center">
          <p className="text-blue-600 font-medium">Hiện không có lệnh thoại nào cần xử lý.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {drafts.map((draft) => {
            // Giải mã JSON từ Backend
            const details = JSON.parse(draft.extracted_json);
            
            return (
              <div key={draft.draft_id} className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden flex flex-col">
                <div className="p-5 flex-1">
                  <div className="flex items-center gap-2 text-xs font-semibold text-blue-600 mb-3 bg-blue-50 w-fit px-2 py-1 rounded">
                    <User size={14} /> {details.customer_name || "Khách vãng lai"}
                  </div>
                  
                  <p className="text-gray-800 font-medium italic mb-4">"{draft.recognized_content}"</p>
                  
                  <div className="space-y-3">
                    <div className="bg-gray-50 rounded-lg p-3">
                      <p className="text-[10px] text-gray-400 uppercase font-bold mb-2">Sản phẩm trích xuất</p>
                      <ul className="space-y-2">
                        {details.items?.map((item: AIDraftItem, idx: number) => (
                          <li key={idx} className="flex justify-between text-sm">
                            <span className="text-gray-600 flex items-center gap-2">
                              <Package size={14} className="text-gray-400" /> {item.product_name}
                            </span>
                            <span className="font-bold">x{item.quantity}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>

                <div className="p-4 bg-gray-50 border-t flex justify-end gap-2">
                  <button className="text-sm px-3 py-1.5 text-gray-500 hover:text-red-600 font-medium">Bỏ qua</button>
                  <button 
                    onClick={() => handleConfirm(draft.draft_id)}
                    className="bg-blue-600 text-white text-sm px-4 py-1.5 rounded-lg font-bold hover:bg-blue-700 flex items-center gap-2"
                  >
                    <Check size={16} /> Xác nhận tạo đơn
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}