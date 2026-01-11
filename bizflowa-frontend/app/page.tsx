import { DollarSign, ShoppingBag, Users, Activity } from "lucide-react";

export default function Home() {
  return (
    <div className="space-y-6">
      {/* Tiêu đề trang */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Tổng quan kinh doanh</h1>
        <span className="text-sm text-gray-500">Cập nhật lần cuối: Vừa xong</span>
      </div>

      {/* Các thẻ báo cáo nhanh (Stats Cards) */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {/* Thẻ 1: Doanh thu */}
        <div className="rounded-xl border bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between space-y-0 pb-2">
            <p className="text-sm font-medium text-gray-500">Tổng doanh thu</p>
            <DollarSign className="h-4 w-4 text-green-600" />
          </div>
          <div className="text-2xl font-bold">120.500.000 ₫</div>
          <p className="text-xs text-green-600">+20.1% so với tháng trước</p>
        </div>

        {/* Thẻ 2: Đơn hàng */}
        <div className="rounded-xl border bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between space-y-0 pb-2">
            <p className="text-sm font-medium text-gray-500">Đơn hàng mới</p>
            <ShoppingBag className="h-4 w-4 text-blue-600" />
          </div>
          <div className="text-2xl font-bold">+573</div>
          <p className="text-xs text-blue-600">+12% so với tuần trước</p>
        </div>

        {/* Thẻ 3: Khách hàng */}
        <div className="rounded-xl border bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between space-y-0 pb-2">
            <p className="text-sm font-medium text-gray-500">Khách hàng</p>
            <Users className="h-4 w-4 text-orange-600" />
          </div>
          <div className="text-2xl font-bold">2,350</div>
          <p className="text-xs text-gray-500">Đang hoạt động</p>
        </div>

        {/* Thẻ 4: Tồn kho */}
        <div className="rounded-xl border bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between space-y-0 pb-2">
            <p className="text-sm font-medium text-gray-500">Sản phẩm sắp hết</p>
            <Activity className="h-4 w-4 text-red-600" />
          </div>
          <div className="text-2xl font-bold">12</div>
          <p className="text-xs text-red-600">Cần nhập thêm ngay</p>
        </div>
      </div>

      {/* Khu vực biểu đồ (Để trống chờ làm sau) */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <div className="col-span-4 rounded-xl border bg-white p-6 shadow-sm h-[300px]">
          <h3 className="text-lg font-medium">Biểu đồ doanh thu</h3>
          <div className="flex h-full items-center justify-center text-gray-400">
            (Chỗ này sẽ vẽ biểu đồ sau)
          </div>
        </div>
        <div className="col-span-3 rounded-xl border bg-white p-6 shadow-sm h-[300px]">
          <h3 className="text-lg font-medium">Sản phẩm bán chạy</h3>
          <div className="flex h-full items-center justify-center text-gray-400">
            (Danh sách top sản phẩm)
          </div>
        </div>
      </div>
    </div>
  );
}