"use client";
import { useState, useEffect } from 'react';
import api from "@/lib/axios";
import { Plus, Trash2, Edit } from "lucide-react";
export default function ProductsPage() {
  const [products, setProducts] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    product_name: '',
    selling_price: 0,
    cost_price: 0, // Quan trọng: Giá vốn theo yêu cầu
    stock_quantity: 0
  });

  // 1. Lấy danh sách sản phẩm
  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      // Giả sử API chạy ở localhost:5000
      const res = await fetch('http://localhost:3000/product', {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') } 
      });
      if (res.ok) {
        const data = await res.json();
        setProducts(data);
      }
    } catch (error) {
      console.error("Lỗi tải sản phẩm:", error);
    }
  };

  // 2. Xử lý thêm mới
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:3000/product', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        body: JSON.stringify(formData)
      });
      
      if (res.ok) {
        alert("Thêm thành công!");
        setShowModal(false);
        fetchProducts(); // Tải lại danh sách
        setFormData({ product_name: '', selling_price: 0, cost_price: 0, stock_quantity: 0 });
      } else {
        alert("Lỗi khi thêm sản phẩm");
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Danh sách hàng hóa</h1>
        <button 
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          + Thêm mới
        </button>
      </div>

      {/* Bảng danh sách */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tên SP</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Giá bán</th>
              {/* <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Giá vốn</th> Ẩn nếu không muốn show */}
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tồn kho</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {products.map((product: any) => (
              <tr key={product.id}>
                <td className="px-6 py-4">{product.name}</td>
                <td className="px-6 py-4 text-green-600 font-medium">
                  {new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(product.price)}
                </td>
                <td className="px-6 py-4">{product.stock_quantity || 0}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal Popup Thêm mới */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white p-6 rounded-lg w-96">
            <h2 className="text-xl font-bold mb-4">Thêm sản phẩm mới</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium">Tên sản phẩm</label>
                <input 
                  type="text" 
                  className="w-full border p-2 rounded"
                  required
                  value={formData.product_name}
                  onChange={e => setFormData({...formData, product_name: e.target.value})}
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium">Giá bán</label>
                  <input 
                    type="number" 
                    className="w-full border p-2 rounded"
                    required
                    value={formData.selling_price}
                    onChange={e => setFormData({...formData, selling_price: Number(e.target.value)})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-red-600">Giá vốn</label>
                  <input 
                    type="number" 
                    className="w-full border p-2 rounded border-red-200"
                    required
                    value={formData.cost_price}
                    onChange={e => setFormData({...formData, cost_price: Number(e.target.value)})}
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium">Tồn kho ban đầu</label>
                <input 
                  type="number" 
                  className="w-full border p-2 rounded"
                  value={formData.stock_quantity}
                  onChange={e => setFormData({...formData, stock_quantity: Number(e.target.value)})}
                />
              </div>
              <div className="flex justify-end gap-2 mt-6">
                <button 
                  type="button"
                  onClick={() => setShowModal(false)} 
                  className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded"
                >
                  Hủy
                </button>
                <button 
                  type="submit" 
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Lưu lại
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}