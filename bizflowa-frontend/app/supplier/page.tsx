"use client";
import { useState, useEffect } from 'react';

export default function SuppliersPage() {
  const [suppliers, setSuppliers] = useState([]);
  const [newSupplier, setNewSupplier] = useState({ supplier_name: '', phone_number: '', tax_code: '' });

  useEffect(() => {
    fetchSuppliers();
  }, []);

  const fetchSuppliers = async () => {
    const res = await fetch('http://localhost:5000/supplier', {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
    });
    if (res.ok) setSuppliers(await res.json());
  };

  const handleAdd = async () => {
    const res = await fetch('http://localhost:5000/supplier', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + localStorage.getItem('token')
      },
      body: JSON.stringify(newSupplier)
    });
    if (res.ok) {
        fetchSuppliers();
        setNewSupplier({ supplier_name: '', phone_number: '', tax_code: '' });
    }
  };

  const handleDelete = async (id: number) => {
    if(!confirm("Bạn chắc chắn muốn xóa?")) return;
    const res = await fetch(`http://localhost:5000/supplier/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
    });
    if (res.ok) fetchSuppliers();
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Nhà cung cấp</h1>
      
      {/* Form thêm nhanh */}
      <div className="bg-gray-50 p-4 rounded mb-6 flex gap-4 items-end">
        <div>
            <label className="text-sm">Tên nhà cung cấp</label>
            <input 
                value={newSupplier.supplier_name}
                onChange={e => setNewSupplier({...newSupplier, supplier_name: e.target.value})}
                className="border p-2 rounded w-full" 
            />
        </div>
        <div>
            <label className="text-sm">Số điện thoại</label>
            <input 
                value={newSupplier.phone_number}
                onChange={e => setNewSupplier({...newSupplier, phone_number: e.target.value})}
                className="border p-2 rounded w-full" 
            />
        </div>
        <button onClick={handleAdd} className="bg-green-600 text-white px-4 py-2 rounded h-10">Thêm</button>
      </div>

      {/* Danh sách */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {suppliers.map((s: any) => (
            <div key={s.id} className="border p-4 rounded bg-white shadow flex justify-between items-center">
                <div>
                    <h3 className="font-bold">{s.name}</h3>
                    <p className="text-sm text-gray-500">{s.phone_number}</p>
                </div>
                <button 
                    onClick={() => handleDelete(s.id)}
                    className="text-red-500 hover:text-red-700 text-sm"
                >
                    Xóa
                </button>
            </div>
        ))}
      </div>
    </div>
  );
}