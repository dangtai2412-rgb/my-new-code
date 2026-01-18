"use client"
import { useEffect, useState } from 'react';
import { 
  DollarSign, ShoppingBag, Users, AlertTriangle, 
  ArrowUpRight, Package, Calendar, Loader2 
} from "lucide-react";
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer 
} from 'recharts';
import api from '@/lib/axios'; // Đảm bảo bạn đã có file này

export default function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    revenue_today: 0,
    orders_today: 0,
    low_stock_count: 0,
    expenses_month: 0
  });
  const [revenueData, setRevenueData] = useState([]);
  const [topProducts, setTopProducts] = useState([]);

  // Hàm gọi API lấy dữ liệu
  const fetchData = async () => {
    try {
      const [statsRes, chartRes, topRes] = await Promise.all([
        api.get('/reports/dashboard'),
        api.get('/reports/chart'),
        api.get('/reports/top-products')
      ]);

      setStats(statsRes.data);
      setRevenueData(chartRes.data);
      setTopProducts(topRes.data);
    } catch (error) {
      console.error("Lỗi tải dữ liệu Dashboard:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
        <span className="ml-2 text-gray-500">Đang tải số liệu...</span>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-500 pb-10">
      
      {/* 1. Header */}
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Tổng quan kinh doanh</h1>
          <p className="text-gray-500 mt-1">Số liệu cập nhật theo thời gian thực hôm nay.</p>
        </div>
        <button 
          onClick={fetchData} 
          className="px-4 py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors text-sm font-medium"
        >
          Làm mới
        </button>
      </div>

      {/* 2. Các thẻ chỉ số (KPI Cards) */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Doanh thu hôm nay */}
        <div className="bg-gradient-to-br from-blue-600 to-blue-700 p-6 rounded-2xl text-white shadow-lg shadow-blue-200">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-blue-100 text-sm font-medium mb-1">Doanh thu hôm nay</p>
              <h3 className="text-2xl font-bold">
                {stats.revenue_today.toLocaleString('vi-VN')} ₫
              </h3>
            </div>
            <div className="bg-white/20 p-2 rounded-lg backdrop-blur-sm">
              <DollarSign className="text-white" size={20} />
            </div>
          </div>
        </div>

        {/* Đơn hàng hôm nay */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-gray-500 text-sm font-medium mb-1">Đơn hàng mới</p>
              <h3 className="text-2xl font-bold text-gray-800">{stats.orders_today}</h3>
            </div>
            <div className="bg-purple-100 p-2 rounded-lg">
              <ShoppingBag className="text-purple-600" size={20} />
            </div>
          </div>
        </div>

        {/* Chi phí tháng này (Mới thêm) */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-gray-500 text-sm font-medium mb-1">Chi phí tháng này</p>
              <h3 className="text-2xl font-bold text-orange-600">
                {stats.expenses_month.toLocaleString('vi-VN')} ₫
              </h3>
            </div>
            <div className="bg-orange-100 p-2 rounded-lg">
              <Users className="text-orange-600" size={20} />
            </div>
          </div>
        </div>

        {/* Cảnh báo kho */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-red-100 relative overflow-hidden">
          <div className="absolute right-0 top-0 w-16 h-16 bg-red-50 rounded-bl-full -mr-4 -mt-4"></div>
          <div className="flex justify-between items-start relative z-10">
            <div>
              <p className="text-gray-500 text-sm font-medium mb-1">Sắp hết hàng</p>
              <h3 className="text-2xl font-bold text-red-600">{stats.low_stock_count}</h3>
            </div>
            <div className="bg-red-100 p-2 rounded-lg">
              <AlertTriangle className="text-red-600" size={20} />
            </div>
          </div>
          {stats.low_stock_count > 0 && (
            <div className="mt-2 text-xs text-red-500 font-medium">
              Cần nhập thêm hàng ngay!
            </div>
          )}
        </div>
      </div>

      {/* 3. Biểu đồ & Top sản phẩm */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Biểu đồ */}
        <div className="lg:col-span-2 bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
          <h3 className="text-lg font-bold text-gray-800 mb-6 flex items-center gap-2">
            <Calendar size={20} className="text-blue-600"/> 
            Doanh thu 7 ngày qua
          </h3>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={revenueData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="date" axisLine={false} tickLine={false} />
                <YAxis 
                  axisLine={false} 
                  tickLine={false} 
                  tickFormatter={(value) => `${value / 1000}k`} 
                />
                <Tooltip 
                  formatter={(value: any) => [`${Number(value).toLocaleString()} ₫`, 'Doanh thu']}
                  contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                />
                <Bar dataKey="revenue" fill="#3B82F6" radius={[4, 4, 0, 0]} barSize={40} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Top sản phẩm */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
          <h3 className="text-lg font-bold text-gray-800 mb-6 flex items-center gap-2">
            <Package size={20} className="text-purple-600"/> 
            Top bán chạy
          </h3>
          <div className="space-y-4">
            {topProducts.length === 0 ? (
              <p className="text-gray-400 text-sm text-center py-4">Chưa có dữ liệu bán hàng</p>
            ) : (
              topProducts.map((item: any, index) => (
                <div key={index} className="flex justify-between items-center border-b border-gray-50 last:border-0 pb-3 last:pb-0">
                  <div className="flex items-center gap-3">
                    <span className="w-6 h-6 flex items-center justify-center bg-gray-100 text-gray-600 text-xs font-bold rounded-full">
                      {index + 1}
                    </span>
                    <span className="text-sm font-medium text-gray-700">{item.name}</span>
                  </div>
                  <span className="text-sm text-blue-600 font-bold">{item.sold}</span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}