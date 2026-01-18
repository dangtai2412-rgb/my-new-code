"use client"
import { useEffect, useState } from 'react';
import { ClipboardCheck, Save, Search, AlertTriangle, Loader2, History } from "lucide-react";
import api from '@/lib/axios';

export default function InventoryCheckPage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [checkData, setCheckData] = useState<{[key: number]: number}>({}); // Lưu số lượng thực tế
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [history, setHistory] = useState([]);
  const [activeTab, setActiveTab] = useState('check'); // 'check' | 'history'

  // 1. Tải danh sách sản phẩm & Lịch sử
  const fetchData = async () => {
    try {
      setLoading(true);
      const [prodRes, histRes] = await Promise.all([
        api.get('/products/'),
        api.get('/inventory-checks/')
      ]);
      setProducts(prodRes.data);
      setHistory(histRes.data);
      
      // Khởi tạo số lượng thực tế = tồn kho hiện tại (để tiện sửa)
      const initialData: any = {};
      prodRes.data.forEach((p: any) => {
        initialData[p.product_id] = p.stock_quantity;
      });
      setCheckData(initialData);

    } catch (error) {
      console.error("Lỗi tải dữ liệu:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // 2. Xử lý nhập số lượng thực tế
  const handleInputChange = (productId: number, value: string) => {
    setCheckData(prev => ({
      ...prev,
      [productId]: parseInt(value) || 0
    }));
  };

  // 3. Gửi phiếu kiểm kho (Cân bằng kho)
  const handleSubmitCheck = async () => {
    if(!confirm("Hành động này sẽ cập nhật lại tồn kho của tất cả sản phẩm. Bạn có chắc chắn?")) return;

    try {
      setIsSubmitting(true);
      
      // Chuẩn bị payload đúng chuẩn Backend yêu cầu
      const payload = {
        note: `Kiểm kho ngày ${new Date().toLocaleDateString('vi-VN')}`,
        details: Object.keys(checkData).map(pid => ({
          product_id: parseInt(pid),
          actual_quantity: checkData[parseInt(pid)]
        }))
      };

      await api.post('/inventory-checks/', payload);
      alert("Cân bằng kho thành công!");
      fetchData(); // Tải lại số liệu mới
      setActiveTab('history'); // Chuyển sang tab lịch sử để xem kết quả
    } catch (error) {
      alert("Lỗi khi cân bằng kho!");
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Lọc sản phẩm
  const filteredProducts = products.filter((p: any) => 
    p.product_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6 animate-in fade-in duration-500 pb-20">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <ClipboardCheck className="text-green-600"/> Kiểm kê & Cân bằng kho
          </h1>
          <p className="text-gray-500 text-sm mt-1">Đối chiếu tồn kho hệ thống và thực tế.</p>
        </div>
        
        <div className="flex bg-gray-100 p-1 rounded-lg">
          <button 
            onClick={() => setActiveTab('check')}
            className={`px-4 py-2 text-sm font-medium rounded-md transition-all ${activeTab === 'check' ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-500'}`}
          >
            Đang kiểm
          </button>
          <button 
            onClick={() => setActiveTab('history')}
            className={`px-4 py-2 text-sm font-medium rounded-md transition-all ${activeTab === 'history' ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-500'}`}
          >
            Lịch sử phiếu
          </button>
        </div>
      </div>

      {/* TAB 1: KIỂM KHO */}
      {activeTab === 'check' && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          
          {/* Toolbar */}
          <div className="p-4 border-b border-gray-100 bg-gray-50 flex flex-col md:flex-row gap-4 justify-between items-center sticky top-0 z-10">
            <div className="relative w-full md:w-96">
              <Search className="absolute left-3 top-2.5 text-gray-400" size={18} />
              <input 
                type="text" 
                placeholder="Tìm tên sản phẩm..." 
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
              />
            </div>
            
            <button 
              onClick={handleSubmitCheck}
              disabled={isSubmitting}
              className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-bold flex items-center gap-2 shadow-lg shadow-green-200 transition-all disabled:opacity-50"
            >
              {isSubmitting ? <Loader2 className="animate-spin"/> : <Save size={18}/>}
              Hoàn tất & Cân bằng
            </button>
          </div>

          {/* Table */}
          <div className="overflow-x-auto max-h-[600px]">
            <table className="w-full text-left">
              <thead className="bg-gray-100 text-gray-600 font-semibold text-sm sticky top-0 z-10 shadow-sm">
                <tr>
                  <th className="px-6 py-3">Sản phẩm</th>
                  <th className="px-6 py-3 text-center">Tồn hệ thống</th>
                  <th className="px-6 py-3 text-center w-48">Thực tế (Nhập)</th>
                  <th className="px-6 py-3 text-center">Chênh lệch</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {loading ? (
                  <tr><td colSpan={4} className="text-center py-10">Đang tải danh sách...</td></tr>
                ) : filteredProducts.map((p: any) => {
                  const systemQty = p.stock_quantity;
                  const actualQty = checkData[p.product_id] ?? systemQty;
                  const diff = actualQty - systemQty;

                  return (
                    <tr key={p.product_id} className="hover:bg-blue-50 transition-colors">
                      <td className="px-6 py-4 font-medium text-gray-800">{p.product_name}</td>
                      <td className="px-6 py-4 text-center text-gray-500 bg-gray-50">{systemQty}</td>
                      <td className="px-6 py-4 text-center">
                        <input 
                          type="number" 
                          value={actualQty}
                          onChange={(e) => handleInputChange(p.product_id, e.target.value)}
                          className="w-24 text-center px-2 py-1 border-2 border-blue-100 rounded-md focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none font-bold text-gray-800"
                        />
                      </td>
                      <td className="px-6 py-4 text-center">
                        {diff !== 0 ? (
                          <span className={`px-2 py-1 rounded text-xs font-bold ${diff > 0 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                            {diff > 0 ? `+${diff}` : diff}
                          </span>
                        ) : (
                          <span className="text-gray-300">-</span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB 2: LỊCH SỬ PHIẾU KIỂM */}
      {activeTab === 'history' && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="font-bold text-gray-700 mb-4 flex items-center gap-2">
            <History size={20}/> Các phiếu đã tạo
          </h3>
          <div className="space-y-4">
            {history.length === 0 ? (
              <p className="text-gray-400">Chưa có lịch sử kiểm kho.</p>
            ) : (
              history.map((check: any) => (
                <div key={check.check_id} className="border border-gray-100 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex justify-between items-center mb-2">
                    <div>
                      <span className="font-bold text-blue-600">{check.check_code}</span>
                      <span className="text-gray-400 text-sm ml-2">
                        {new Date(check.check_date).toLocaleString('vi-VN')}
                      </span>
                    </div>
                    <span className="bg-green-100 text-green-700 px-2 py-1 rounded text-xs font-bold">
                      Đã hoàn thành
                    </span>
                  </div>
                  <p className="text-gray-600 text-sm italic mb-3">"{check.note}"</p>
                  
                  {/* Chi tiết rút gọn */}
                  <div className="bg-gray-50 p-3 rounded text-sm text-gray-600">
                    <p>Đã kiểm <b>{check.details.length}</b> mặt hàng.</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

    </div>
  );
}