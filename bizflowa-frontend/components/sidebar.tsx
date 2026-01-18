"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  Package, 
  ShoppingCart, 
  Users, 
  Settings, 
  Truck, 
  Bot,
  Tag,     // Icon Danh mục
  Wallet,  // Icon Chi phí (Mới thêm)
  Ruler    // Icon Đơn vị (Nếu cần)
} from "lucide-react";
import clsx from "clsx";
import { ClipboardCheck } from "lucide-react";
const menuItems = [
  { name: "Tổng quan", href: "/", icon: LayoutDashboard },
  { name: "Bán hàng (POS)", href: "/pos_order_module", icon: ShoppingCart }, // Đổi tên cho đúng chức năng
  { name: "Sản phẩm", href: "/products", icon: Package },
  { name: 'Danh mục', href: '/categories', icon: Tag }, // Đã sửa 'path' -> 'href'
  { name: "Đơn vị tính", href: "/units", icon: Ruler }, // Thêm cho đủ bộ
  { name: 'Sổ quỹ (Chi phí)', href: '/expenses', icon: Wallet }, // Mới thêm
  { name: "Khách hàng", href: "/customers", icon: Users },
  { name: "Nhà cung cấp", href: "/supplier", icon: Truck }, // Lưu ý: folder của bạn là 'supplier' (số ít)
  { name: "Đơn hàng AI", href: "/ai_drafts", icon: Bot },
  { name: 'Kiểm kho', href: '/inventory_check', icon: ClipboardCheck },
  { name: 'Sổ quỹ (Chi phí)', href: '/expenses', icon: Wallet },
  
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="flex h-screen w-64 flex-col justify-between border-r bg-white px-3 py-4 shadow-sm sticky top-0">
      <div>
        <div className="mb-8 flex items-center gap-2 px-3 pt-2">
          <div className="h-8 w-8 rounded-lg bg-blue-600 flex items-center justify-center">
            <span className="text-white font-bold text-xl">B</span>
          </div>
          <span className="text-xl font-bold text-gray-800">BizFlow</span>
        </div>

        <nav className="space-y-1">
          {menuItems.map((item) => {
            const LinkIcon = item.icon;
            const isActive = pathname === item.href;
            
            return (
              <Link
                key={item.href}
                href={item.href}
                className={clsx(
                  "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-200",
                  isActive
                    ? "bg-blue-50 text-blue-600 shadow-sm"
                    : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"
                )}
              >
                <LinkIcon className={clsx("h-5 w-5", isActive ? "text-blue-600" : "text-gray-400")} />
                {item.name}
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="border-t pt-4 space-y-1">
        <Link
          href="/settings"
          className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900"
        >
          <Settings className="h-5 w-5 text-gray-500" />
          Cài đặt
        </Link>
        {/* Nút đăng xuất có thể thêm logic sau */}
      </div>
    </div>
  );
}