"use client";

import React, { useState, useEffect } from 'react';
import { Search, Plus, Edit, Trash2, MoreHorizontal, Loader2 } from 'lucide-react';
import api from '@/lib/axios'; // <--- 1. Import axios thần thánh

interface Unit {
  id: number; // Backend thường trả về number, check lại nếu là string
  name: string;
  description?: string;
}

export default function UnitsPage() {
  const [units, setUnits] = useState<Unit[]>([]);
  const [loading, setLoading] = useState(true); // <--- 2. Thêm state loading
  const [searchTerm, setSearchTerm] = useState('');

  // Hàm gọi API thật
  const fetchUnits = async () => {
    try {
      setLoading(true);
      // Gọi xuống Backend (Route này phải khớp với file unit_controller.py)
      const response = await api.get('/units'); 
      setUnits(response.data);
    } catch (error) {
      console.error("Lỗi lấy danh sách đơn vị:", error);
      // Có thể thêm toast thông báo lỗi ở đây
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUnits(); // <--- 3. Gọi hàm khi trang vừa load
  }, []);

  return (
    <div className="p-6">
      {/* Header Section */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Danh sách Đơn vị tính</h1>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors">
          <Plus size={20} />
          Thêm đơn vị
        </button>
      </div>

      {/* Filter & Search */}
      <div className="bg-white p-4 rounded-t-xl border-x border-t flex flex-wrap gap-4 items-center justify-between">
        <div className="relative w-full max-w-md">
          <span className="absolute inset-y-0 left-0 pl-3 flex items-center text-gray-400">
            <Search size={18} />
          </span>
          <input
            type="text"
            placeholder="Tìm kiếm đơn vị..."
            className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-blue-500 sm:text-sm"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="text-sm text-gray-500">
          Hiển thị <b>{units.length}</b> đơn vị
        </div>
      </div>

      {/* Table Section */}
      <div className="bg-white border rounded-b-xl overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tên đơn vị</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ghi chú</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Thao tác</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {/* Xử lý trường hợp Loading và Dữ liệu trống */}
            {loading ? (
              <tr>
                <td colSpan={4} className="px-6 py-8 text-center text-gray-500">
                  <div className="flex justify-center items-center gap-2">
                    <Loader2 className="animate-spin" /> Đang tải dữ liệu...
                  </div>
                </td>
              </tr>
            ) : units.length === 0 ? (
              <tr>
                <td colSpan={4} className="px-6 py-8 text-center text-gray-500">
                  Chưa có dữ liệu đơn vị tính nào.
                </td>
              </tr>
            ) : (
              // Render dữ liệu thật
              units
                .filter(u => u.name.toLowerCase().includes(searchTerm.toLowerCase()))
                .map((unit) => (
                  <tr key={unit.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">#{unit.id}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{unit.name}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{unit.description || '-'}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex justify-end gap-3">
                        <button className="text-blue-600 hover:text-blue-900"><Edit size={18} /></button>
                        <button className="text-red-600 hover:text-red-900"><Trash2 size={18} /></button>
                      </div>
                    </td>
                  </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}