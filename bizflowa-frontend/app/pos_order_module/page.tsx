"use client";

import React, { useState, useEffect } from "react";
import axios from "axios";
import { Search, ShoppingCart, Trash2, Plus, Minus } from "lucide-react";

// --- Types (Định nghĩa kiểu dữ liệu) ---
interface Product {
  id: number;
  name: string;
  price: number;
  image: string; // URL hình ảnh
  category: string;
}

interface CartItem extends Product {
  quantity: number;
}

// --- Mock Data (Dữ liệu giả lập để test giao diện trước khi có API thật) ---
const MOCK_PRODUCTS: Product[] = [
  { id: 1, name: "Cà phê sữa đá", price: 25000, image: "https://via.placeholder.com/150", category: "Drink" },
  { id: 2, name: "Bạc xỉu", price: 29000, image: "https://via.placeholder.com/150", category: "Drink" },
  { id: 3, name: "Trà đào cam sả", price: 35000, image: "https://via.placeholder.com/150", category: "Drink" },
  { id: 4, name: "Bánh Croissant", price: 20000, image: "https://via.placeholder.com/150", category: "Food" },
  { id: 5, name: "Trà sữa trân châu", price: 32000, image: "https://via.placeholder.com/150", category: "Drink" },
  { id: 6, name: "Bánh Tiramisu", price: 40000, image: "https://via.placeholder.com/150", category: "Food" },
];

export default function POSPage() {
  // --- State ---
  const [products, setProducts] = useState<Product[]>(MOCK_PRODUCTS); // Sau này sẽ fetch từ API product
  const [cart, setCart] = useState<CartItem[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(false);

  // --- Logic Giỏ hàng ---
  
  // 1. Thêm vào giỏ (Click product)
  const addToCart = (product: Product) => {
    setCart((prev) => {
      const existing = prev.find((item) => item.id === product.id);
      if (existing) {
        return prev.map((item) =>
          item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
        );
      }
      return [...prev, { ...product, quantity: 1 }];
    });
  };

  // 2. Tăng giảm số lượng
  const updateQuantity = (id: number, delta: number) => {
    setCart((prev) =>
      prev.map((item) => {
        if (item.id === id) {
          return { ...item, quantity: Math.max(1, item.quantity + delta) };
        }
        return item;
      })
    );
  };

  // 3. Xóa khỏi giỏ
  const removeFromCart = (id: number) => {
    setCart((prev) => prev.filter((item) => item.id !== id));
  };

  // 4. Tính tổng tiền
  const totalAmount = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  // --- Logic Tìm kiếm ---
  const filteredProducts = products.filter((p) =>
    p.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // --- Logic Thanh toán (Gọi API /order) ---
  const handlePayment = async (method: "CASH" | "DEBT") => {
    if (cart.length === 0) return alert("Giỏ hàng đang trống!");

    setLoading(true);
    try {
      // Payload gửi xuống Backend (order_controller)
      const payload = {
        payment_method: method, // "Tiền mặt" hoặc "Ghi nợ"
        items: cart.map((item) => ({
          product_id: item.id,
          quantity: item.quantity,
          price: item.price,
        })),
        total_amount: totalAmount,
      };

      // GỌI API BACKEND
      // URL này trỏ đến Flask server của bạn (VD: http://localhost:5000/api/order)
      const response = await axios.post("http://localhost:5000/api/order", payload);

      if (response.status === 200 || response.status === 201) {
        alert(`Thanh toán thành công qua ${method === 'CASH' ? 'Tiền mặt' : 'Ghi nợ'}!`);
        setCart([]); // Reset giỏ hàng
      }
    } catch (error) {
      console.error("Lỗi thanh toán:", error);
      alert("Có lỗi xảy ra khi tạo đơn hàng.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-100 overflow-hidden font-sans">
      
      {/* --- CỘT TRÁI: DANH SÁCH SẢN PHẨM (65-70%) --- */}
      <div className="flex-1 flex flex-col p-4 overflow-hidden">
        {/* Thanh tìm kiếm */}
        <div className="mb-4 relative">
          <Search className="absolute left-3 top-3 text-gray-400 w-5 h-5" />
          <input
            type="text"
            placeholder="Tìm kiếm sản phẩm..."
            className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        {/* Lưới sản phẩm */}
        <div className="flex-1 overflow-y-auto grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 pb-20">
          {filteredProducts.map((product) => (
            <div
              key={product.id}
              onClick={() => addToCart(product)}
              className="bg-white rounded-xl shadow-sm hover:shadow-md cursor-pointer transition-all border border-transparent hover:border-blue-300 flex flex-col overflow-hidden"
            >
              {/* Hình ảnh */}
              <div className="h-32 bg-gray-200 w-full relative">
                 <img src={product.image} alt={product.name} className="object-cover w-full h-full" />
              </div>
              {/* Thông tin */}
              <div className="p-3">
                <h3 className="font-semibold text-gray-800 text-sm truncate">{product.name}</h3>
                <p className="text-blue-600 font-bold mt-1">
                  {product.price.toLocaleString("vi-VN")} đ
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* --- CỘT PHẢI: GIỎ HÀNG (30-35%) --- */}
      <div className="w-96 bg-white shadow-xl flex flex-col h-full border-l border-gray-200">
        <div className="p-4 border-b border-gray-100 bg-gray-50">
          <h2 className="text-lg font-bold flex items-center gap-2 text-gray-700">
            <ShoppingCart className="w-5 h-5" /> Giỏ hàng
          </h2>
        </div>

        {/* Danh sách item trong giỏ */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {cart.length === 0 ? (
            <div className="text-center text-gray-400 mt-10">Chưa có sản phẩm nào</div>
          ) : (
            cart.map((item) => (
              <div key={item.id} className="flex justify-between items-center group">
                <div className="flex-1">
                  <h4 className="font-medium text-gray-800">{item.name}</h4>
                  <div className="text-sm text-gray-500">
                    {item.price.toLocaleString("vi-VN")} đ
                  </div>
                </div>
                
                {/* Điều chỉnh số lượng */}
                <div className="flex items-center gap-2 bg-gray-100 rounded-lg p-1">
                  <button onClick={() => updateQuantity(item.id, -1)} className="p-1 hover:bg-white rounded shadow-sm">
                    <Minus className="w-3 h-3" />
                  </button>
                  <span className="text-sm font-semibold w-6 text-center">{item.quantity}</span>
                  <button onClick={() => updateQuantity(item.id, 1)} className="p-1 hover:bg-white rounded shadow-sm">
                    <Plus className="w-3 h-3" />
                  </button>
                </div>

                <button onClick={() => removeFromCart(item.id)} className="ml-3 text-red-400 hover:text-red-600">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))
          )}
        </div>

        {/* Khu vực Thanh toán */}
        <div className="p-4 border-t border-gray-100 bg-gray-50">
          <div className="flex justify-between items-center mb-4">
            <span className="text-gray-600">Tổng cộng:</span>
            <span className="text-2xl font-bold text-blue-700">
              {totalAmount.toLocaleString("vi-VN")} đ
            </span>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <button
              disabled={loading}
              onClick={() => handlePayment("CASH")}
              className="bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-semibold shadow transition-colors disabled:opacity-50"
            >
              Tiền mặt
            </button>
            <button
              disabled={loading}
              onClick={() => handlePayment("DEBT")}
              className="bg-orange-500 hover:bg-orange-600 text-white py-3 rounded-lg font-semibold shadow transition-colors disabled:opacity-50"
            >
              Ghi nợ
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}