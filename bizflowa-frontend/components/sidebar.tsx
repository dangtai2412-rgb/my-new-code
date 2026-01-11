"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  Package, 
  ShoppingCart, 
  Users, 
  Settings, 
  LogOut,
  Truck,
  Bot 
} from "lucide-react";
import clsx from "clsx";

const menuItems = [
  { name: "Tổng quan", href: "/", icon: LayoutDashboard },
  { name: "Đơn hàng AI", href: "/ai_drafts", icon: Bot }, // Khớp với folder app/ai_drafts
  { name: "Sản phẩm", href: "/products", icon: Package },
  { name: "Đơn hàng", href: "/orders", icon: ShoppingCart },
  { name: "Khách hàng", href: "/customers", icon: Users },
  { name: "Nhà cung cấp", href: "/suppliers", icon: Truck },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="flex h-screen w-64 flex-col justify-between border-r bg-white px-3 py-4 shadow-sm">
      <div>
        <div className="mb-6 flex items-center gap-2 px-3">
          <div className="h-8 w-8 rounded-lg bg-blue-600 flex items-center justify-center">
            <span className="text-white font-bold text-lg">B</span>
          </div>
          <span className="text-xl font-bold text-gray-900 tracking-tight">BizFlowa</span>
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
                  "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-all duration-200",
                  isActive
                    ? "bg-blue-50 text-blue-600"
                    : "text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                )}
              >
                <LinkIcon className={clsx("h-5 w-5", isActive ? "text-blue-600" : "text-gray-500")} />
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
        <button
          className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-red-600 hover:bg-red-50 transition-colors"
        >
          <LogOut className="h-5 w-5" />
          Đăng xuất
        </button>
      </div>
    </div>
  );
}