"use client";
import { useState, useEffect } from 'react';
import api from "@/lib/axios"; // 1. Dùng axios đã cấu hình để tự động gửi Token
import { Plus, Trash2, Edit } from "lucide-react"; // Import icon cho đẹp

export default function ProductsPage() {
  const [products, setProducts] = useState([]);
  const [showModal, setShowModal] = useState(false);
  
  // State form bao gồm cả cost_price (giá vốn)
  const [formData, setFormData] = useState({
    product_name: '',
    selling_price: 0,
    cost_price: 0, 
    stock_quantity: 0
  });

  // 2. Lấy danh sách sản phẩm
  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      // SỬA QUAN TRỌNG: Dùng api.get và sửa đường dẫn thành '/products' (số nhiều)
      const res = await api.get('/products');
      setProducts(res.data);
    } catch (error) {
      console.error("Lỗi tải sản phẩm:", error);
    }
  };

  // 3. Xử lý thêm mới
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // SỬA QUAN TRỌNG: Dùng api.post, không cần truyền header Authorization thủ công nữa
      await api.post('/products', formData);
      
      alert("Thêm thành công!");
      setShowModal(false);
      fetchProducts(); // Tải lại danh sách ngay lập tức
      
      // Reset form
      setFormData({ product_name: '', selling_price: 0, cost_price: 0, stock_quantity: 0 });
    } catch (error: any) {
      console.error(error);
      alert(error.response?.data?.error || "Lỗi khi thêm sản phẩm");
    }
  };

  // 4. Hàm xóa sản phẩm (Thêm vào cho đầy đủ chức năng)
  const handleDelete = async (id: number) => {
    if(!confirm("Bạn chắc chắn muốn xóa sản phẩm này?")) return;
    try {
      await api.delete(`/products/${id}`);
      fetchProducts(); // Tải lại sau khi xóa
    } catch (error) {
       console.error("Lỗi xóa:", error);
       alert("Không thể xóa sản phẩm này");
    }
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Danh sách hàng hóa</h1>
        <button 
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 flex items-center gap-2 shadow"
        >
          <Plus size={18}/> Thêm mới
        </button>
      </div>

      {/* Bảng danh sách */}
      <div className="bg-white rounded-lg shadow overflow-hidden border border-gray-200">
        <table className="min-w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Tên SP</th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Giá bán</th>
              {/* Đã mở comment cột Giá vốn để hiển thị */}
              <th className="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Giá vốn</th> 
              <th className="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Tồn kho</th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Thao tác</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {products.length === 0 ? (
                <tr><td colSpan={5} className="text-center py-4 text-gray-500">Chưa có sản phẩm nào</td></tr>
            ) : products.map((product: any) => (
              <tr key={product.id || product.product_id} className="hover:bg-gray-50">
                <td className="px-6 py-4 text-gray-900 font-medium">{product.name || product.product_name}</td>
                <td className="px-6 py-4 text-green-600 font-semibold">
                  {new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(product.price || product.selling_price)}
                </td>
                <td className="px-6 py-4 text-gray-500">
                   {/* Hiển thị giá vốn (nếu backend trả về) */}
                   {product.cost_price ? new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(product.cost_price) : '-'}
                </td>
                <td className="px-6 py-4 text-gray-700">{product.stock_quantity || 0}</td>
                <td className="px-6 py-4 flex gap-3">
                   <button className="text-blue-600 hover:text-blue-800 p-1 rounded hover:bg-blue-50"><Edit size={18}/></button>
                   <button 
                    onClick={() => handleDelete(product.id || product.product_id)} 
                    className="text-red-600 hover:text-red-800 p-1 rounded hover:bg-red-50"
                   >
                    <Trash2 size={18}/>
                   </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal Popup Thêm mới */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-8 rounded-xl w-96 shadow-2xl animate-fade-in-down">
            <h2 className="text-xl font-bold mb-6 text-gray-800 border-b pb-2">Thêm sản phẩm mới</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Tên sản phẩm</label>
                <input 
                  type="text" 
                  className="w-full border border-gray-300 p-2 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"
                  required
                  placeholder="Ví dụ: Cà phê đá xay"
                  value={formData.product_name}
                  onChange={e => setFormData({...formData, product_name: e.target.value})}
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Giá bán</label>
                  <input 
                    type="number" 
                    className="w-full border border-gray-300 p-2 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"
                    required
                    value={formData.selling_price}
                    onChange={e => setFormData({...formData, selling_price: Number(e.target.value)})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-red-600 mb-1">Giá vốn</label>
                  <input 
                    type="number" 
                    className="w-full border border-red-200 p-2 rounded-lg focus:ring-2 focus:ring-red-500 outline-none transition bg-red-50"
                    required
                    value={formData.cost_price}
                    onChange={e => setFormData({...formData, cost_price: Number(e.target.value)})}
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Tồn kho ban đầu</label>
                <input 
                  type="number" 
                  className="w-full border border-gray-300 p-2 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"
                  value={formData.stock_quantity}
                  onChange={e => setFormData({...formData, stock_quantity: Number(e.target.value)})}
                />
              </div>
              
              <div className="flex justify-end gap-3 mt-8">
                <button 
                  type="button"
                  onClick={() => setShowModal(false)} 
                  className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition"
                >
                  Hủy bỏ
                </button>
                <button 
                  type="submit" 
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition shadow-md"
                >
                  Lưu sản phẩm
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}