"use client"
import { useEffect, useState } from 'react';
import api from '@/lib/axios';
import { Users, Plus, Trash2, UserPlus } from "lucide-react";

// Định nghĩa kiểu dữ liệu cho Nhân viên (Khớp với Backend)
interface Employee {
  id: number;
  name: string;
  username: string;
  role: string;
}

export default function EmployeePage() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  
  // State cho Form thêm mới
  const [showModal, setShowModal] = useState(false);
  const [newEmp, setNewEmp] = useState({
    employee_name: '',
    username: '',
    password: '',
    role: 'SALES', // Mặc định là nhân viên bán hàng
    owner_id: 1 // TODO: Lấy ID này từ Token đăng nhập của Chủ shop
  });

  // 1. Hàm lấy danh sách nhân viên từ API
  const fetchEmployees = async () => {
    try {
      // Giả sử chủ shop có ID = 1 (Sau này lấy từ context)
      const ownerId = 1; 
      const res = await api.get(`/employees/owner/${ownerId}`);
      setEmployees(res.data);
    } catch (error) {
      console.error("Lỗi tải danh sách nhân viên:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEmployees();
  }, []);

  // 2. Hàm xử lý thêm nhân viên mới
  const handleCreateEmployee = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/employees/', newEmp);
      alert("Thêm nhân viên thành công!");
      setShowModal(false);
      fetchEmployees(); // Tải lại danh sách
      // Reset form
      setNewEmp({...newEmp, employee_name: '', username: '', password: ''});
    } catch (error: any) {
      alert("Lỗi: " + (error.response?.data?.error || "Không thể tạo nhân viên"));
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <Users className="w-8 h-8 text-blue-600" />
          Quản lý Nhân viên
        </h1>
        <button 
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700"
        >
          <UserPlus size={20} />
          Thêm nhân viên
        </button>
      </div>

      {/* Bảng danh sách */}
      <div className="bg-white rounded-xl shadow border overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="p-4 font-semibold text-gray-600">ID</th>
              <th className="p-4 font-semibold text-gray-600">Họ tên</th>
              <th className="p-4 font-semibold text-gray-600">Tài khoản</th>
              <th className="p-4 font-semibold text-gray-600">Vai trò</th>
              <th className="p-4 font-semibold text-gray-600">Hành động</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={5} className="p-4 text-center">Đang tải...</td></tr>
            ) : employees.map((emp) => (
              <tr key={emp.id} className="border-b hover:bg-gray-50">
                <td className="p-4">#{emp.id}</td>
                <td className="p-4 font-medium">{emp.name}</td>
                <td className="p-4 text-gray-500">{emp.username}</td>
                <td className="p-4">
                  <span className={`px-2 py-1 rounded text-xs font-bold ${
                    emp.role === 'SALES' ? 'bg-green-100 text-green-700' : 
                    emp.role === 'ACCOUNTANT' ? 'bg-purple-100 text-purple-700' : 'bg-gray-100'
                  }`}>
                    {emp.role}
                  </span>
                </td>
                <td className="p-4">
                  <button className="text-red-500 hover:text-red-700">
                    <Trash2 size={18} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {employees.length === 0 && !loading && (
          <div className="p-8 text-center text-gray-500">Chưa có nhân viên nào.</div>
        )}
      </div>

      {/* Modal Thêm mới (Popup) */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-lg w-full max-w-md p-6">
            <h2 className="text-xl font-bold mb-4">Thêm Nhân viên mới</h2>
            <form onSubmit={handleCreateEmployee} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Họ và tên</label>
                <input 
                  type="text" required
                  className="w-full p-2 border rounded-lg"
                  placeholder="Ví dụ: Nguyễn Văn A"
                  value={newEmp.employee_name}
                  onChange={e => setNewEmp({...newEmp, employee_name: e.target.value})}
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Tên đăng nhập</label>
                  <input 
                    type="text" required
                    className="w-full p-2 border rounded-lg"
                    placeholder="nv_banhang"
                    value={newEmp.username}
                    onChange={e => setNewEmp({...newEmp, username: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Mật khẩu</label>
                  <input 
                    type="password" required
                    className="w-full p-2 border rounded-lg"
                    placeholder="******"
                    value={newEmp.password}
                    onChange={e => setNewEmp({...newEmp, password: e.target.value})}
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Vai trò</label>
                <select 
                  className="w-full p-2 border rounded-lg"
                  value={newEmp.role}
                  onChange={e => setNewEmp({...newEmp, role: e.target.value})}
                >
                  <option value="SALES">Nhân viên Bán hàng</option>
                  <option value="INVENTORY">Nhân viên Kho</option>
                  <option value="ACCOUNTANT">Kế toán</option>
                </select>
              </div>

              <div className="flex justify-end gap-3 mt-6">
                <button 
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
                >
                  Hủy bỏ
                </button>
                <button 
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Lưu nhân viên
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}