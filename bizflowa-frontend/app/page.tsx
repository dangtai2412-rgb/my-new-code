"use client"
import { useEffect, useState } from 'react';
import { DollarSign, ShoppingBag, Users, AlertTriangle, TrendingUp } from "lucide-react";
import api from '@/lib/axios';

// Định nghĩa kiểu dữ liệu cho đơn hàng hiển thị
interface RecentOrder {
  id: number;
  customer_name: string;
  total_amount: number;
  status: string;
  created_at: string;
}

export default function Dashboard() {
  const [stats, setStats] = useState({
    revenue: 0,
    orders_count: 0,
    customers_count: 0,
    low_stock_count: 0
  });
  const [recentOrders, setRecentOrders] = useState<RecentOrder[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // 1. Gọi API lấy số liệu thống kê (Nếu chưa có endpoint này, BE sẽ trả lỗi và ta dùng số giả)
        // const statsRes = await api.get('/reports/dashboard-stats'); 
        // setStats(statsRes.data);

        // 2. Gọi API lấy đơn hàng mới nhất
        // const ordersRes = await api.get('/orders?limit=5');
        // setRecentOrders(ordersRes.data);

        // --- MOCK DATA (DỮ LIỆU GIẢ ĐỂ TEST GIAO DIỆN KHI CHƯA CÓ API DASHBOARD) ---
        // Khi nào Backend viết xong API thống kê thì xóa đoạn này đi
        setStats({
          revenue: 15400000,
          orders_count: 42,
          customers_count: 128,
          low_stock_count: 5
        });
        setRecentOrders([
          { id: 101, customer_name: "Nguyễn Văn A", total_amount: 500000, status: "COMPLETED", created_at: "2024-01-20" },
          { id: 102, customer_name: "Trần Thị B", total_amount: 1200000, status: "PENDING", created_at: "2024-01-20" },
          { id: 103, customer_name: "Lê Văn C", total_amount: 250000, status: "CANCELLED", created_at: "2024-01-19" },
        ]);
        // --------------------------------------------------------------------------

      } catch (error) {
        console.error("Lỗi tải dashboard:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">Tổng quan kinh doanh</h1>

      {/* 4 Thẻ Thống kê (Cards) */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Thẻ 1: Doanh thu */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
          <div className="p-3 bg-green-100 text-green-600 rounded-full">
            <DollarSign size={24} />
          </div>
          <div>
            <p className="text-sm text-gray-500">Doanh thu hôm nay</p>
            <h3 className="text-2xl font-bold text-gray-800">{stats.revenue.toLocaleString('vi-VN')} ₫</h3>
          </div>
        </div>

        {/* Thẻ 2: Đơn hàng */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
          <div className="p-3 bg-blue-100 text-blue-600 rounded-full">
            <ShoppingBag size={24} />
          </div>
          <div>
            <p className="text-sm text-gray-500">Đơn hàng mới</p>
            <h3 className="text-2xl font-bold text-gray-800">{stats.orders_count}</h3>
          </div>
        </div>

        {/* Thẻ 3: Khách hàng */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
          <div className="p-3 bg-purple-100 text-purple-600 rounded-full">
            <Users size={24} />
          </div>
          <div>
            <p className="text-sm text-gray-500">Tổng khách hàng</p>
            <h3 className="text-2xl font-bold text-gray-800">{stats.customers_count}</h3>
          </div>
        </div>

        {/* Thẻ 4: Cảnh báo kho */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
          <div className="p-3 bg-red-100 text-red-600 rounded-full">
            <AlertTriangle size={24} />
          </div>
          <div>
            <p className="text-sm text-gray-500">Sắp hết hàng</p>
            <h3 className="text-2xl font-bold text-gray-800">{stats.low_stock_count} SP</h3>
          </div>
        </div>
      </div>

      {/* Bảng đơn hàng gần đây */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-bold text-gray-800 flex items-center gap-2">
            <TrendingUp size={20} className="text-blue-600"/> Đơn hàng gần đây
          </h2>
          <button className="text-sm text-blue-600 hover:underline">Xem tất cả</button>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="p-3 text-sm font-semibold text-gray-600">Mã đơn</th>
                <th className="p-3 text-sm font-semibold text-gray-600">Khách hàng</th>
                <th className="p-3 text-sm font-semibold text-gray-600">Tổng tiền</th>
                <th className="p-3 text-sm font-semibold text-gray-600">Trạng thái</th>
                <th className="p-3 text-sm font-semibold text-gray-600">Ngày tạo</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan={5} className="p-4 text-center">Đang tải...</td></tr>
              ) : recentOrders.map((order) => (
                <tr key={order.id} className="border-b hover:bg-gray-50">
                  <td className="p-3 text-sm">#{order.id}</td>
                  <td className="p-3 text-sm font-medium">{order.customer_name}</td>
                  <td className="p-3 text-sm">{order.total_amount.toLocaleString('vi-VN')} ₫</td>
                  <td className="p-3 text-sm">
                    <span className={`px-2 py-1 rounded text-xs font-bold ${
                      order.status === 'COMPLETED' ? 'bg-green-100 text-green-700' :
                      order.status === 'PENDING' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {order.status}
                    </span>
                  </td>
                  <td className="p-3 text-sm text-gray-500">{order.created_at}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}