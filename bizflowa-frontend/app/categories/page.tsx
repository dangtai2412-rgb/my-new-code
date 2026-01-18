"use client"
import { useEffect, useState } from 'react';
import { Plus, Search, Trash2, Tag, Loader2 } from "lucide-react";
import api from '@/lib/axios';

export default function CategoriesPage() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  
  // State cho form thêm mới
  const [isCreating, setIsCreating] = useState(false);
  const [newCatName, setNewCatName] = useState('');
  const [newCatDesc, setNewCatDesc] = useState('');

  // 1. Hàm lấy danh sách
  const fetchCategories = async () => {
    try {
      setLoading(true);
      const res = await api.get('/categories/');
      setCategories(res.data);
    } catch (error) {
      console.error("Lỗi tải danh mục:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  // 2. Hàm tạo mới
  const handleCreate = async () => {
    if (!newCatName.trim()) return alert("Tên danh mục không được để trống!");
    
    try {
      setIsCreating(true);
      await api.post('/categories/', {
        category_name: newCatName,
        description: newCatDesc
      });
      
      // Reset form & tải lại
      setNewCatName('');
      setNewCatDesc('');
      fetchCategories();
      alert("Thêm danh mục thành công!");
    } catch (error) {
      alert("Lỗi khi thêm danh mục!");
    } finally {
      setIsCreating(false);
    }
  };

  // 3. Hàm xóa
  const handleDelete = async (id: number) => {
    if (!confirm("Bạn có chắc muốn xóa danh mục này?")) return;
    try {
      await api.delete(`/categories/${id}`);
      fetchCategories(); // Load lại
    } catch (error) {
      alert("Không thể xóa (Có thể danh mục đang chứa sản phẩm!)");
    }
  };

  // Lọc tìm kiếm
  const filteredCats = categories.filter((cat: any) => 
    cat.category_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <Tag className="text-blue-600"/> Quản lý Danh mục
          </h1>
          <p className="text-gray-500 text-sm mt-1">Phân loại hàng hóa (Sắt, Xi măng, Gạch...)</p>
        </div>
      </div>

      {/* Form thêm nhanh */}
      <div className="bg-white p-4 rounded-xl shadow-sm border border-blue-100 flex flex-col md:flex-row gap-3 items-end">
        <div className="flex-1 w-full">
          <label className="text-xs font-semibold text-gray-600 mb-1 block">Tên danh mục mới</label>
          <input 
            value={newCatName}
            onChange={(e) => setNewCatName(e.target.value)}
            placeholder="VD: Xi măng cao cấp"
className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
          />
        </div>
        <div className="flex-[2] w-full">
          <label className="text-xs font-semibold text-gray-600 mb-1 block">Mô tả (Tùy chọn)</label>
          <input 
            value={newCatDesc}
            onChange={(e) => setNewCatDesc(e.target.value)}
            placeholder="Mô tả thêm..." 
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
          />
        </div>
        <button 
          onClick={handleCreate}
          disabled={isCreating}
          className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium flex items-center gap-2 disabled:opacity-50 transition-colors"
        >
          {isCreating ? <Loader2 className="animate-spin" size={18}/> : <Plus size={18}/>}
          Thêm mới
        </button>
      </div>

      {/* Danh sách & Tìm kiếm */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        {/* Search Bar */}
        <div className="p-4 border-b border-gray-100 bg-gray-50">
          <div className="relative max-w-md">
            <Search className="absolute left-3 top-2.5 text-gray-400" size={18} />
            <input 
              type="text" 
              placeholder="Tìm kiếm danh mục..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
            />
          </div>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-gray-50 text-gray-600 font-medium text-sm">
              <tr>
                <th className="px-6 py-3">ID</th>
                <th className="px-6 py-3">Tên Danh Mục</th>
                <th className="px-6 py-3">Mô tả</th>
                <th className="px-6 py-3 text-center">Thao tác</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {loading ? (
                <tr><td colSpan={4} className="text-center py-8 text-gray-500">Đang tải...</td></tr>
              ) : filteredCats.length === 0 ? (
                <tr><td colSpan={4} className="text-center py-8 text-gray-400">Chưa có danh mục nào</td></tr>
              ) : (
                filteredCats.map((cat: any) => (
                  <tr key={cat.category_id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-3 text-gray-500">#{cat.category_id}</td>
                    <td className="px-6 py-3 font-medium text-gray-800">{cat.category_name}</td>
                    <td className="px-6 py-3 text-gray-500 text-sm">{cat.description || "—"}</td>
                    <td className="px-6 py-3 text-center">
<button 
                        onClick={() => handleDelete(cat.category_id)}
                        className="p-2 text-red-500 hover:bg-red-50 rounded-full transition-colors"
                        title="Xóa"
                      >
                        <Trash2 size={18} />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}