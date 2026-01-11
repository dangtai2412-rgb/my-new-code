"use client";

import { useEffect, useState } from "react";
import api from "@/lib/axios";
import { Plus, Trash2, Edit } from "lucide-react";

interface Unit {
  id: number;
  name: string;
}

export default function UnitsPage() {
  const [units, setUnits] = useState<Unit[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Giả lập gọi API lấy đơn vị tính
    const fetchUnits = async () => {
      try {
        // const res = await api.get("/units"); 
        // setUnits(res.data);
        
        // Dữ liệu giả để test trước khi có Backend
        setUnits([
          { id: 1, name: "Cái" },
          { id: 2, name: "Hộp" },
          { id: 3, name: "Thùng" },
          { id: 4, name: "Kg" },
        ]);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };
    fetchUnits();
  }, []);

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Đơn vị tính</h1>
        <button className="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
          <Plus className="h-4 w-4" /> Thêm mới
        </button>
      </div>

      <div className="rounded-xl border bg-white shadow-sm">
        <table className="w-full text-left text-sm">
          <thead className="bg-gray-50 text-gray-500">
            <tr>
              <th className="px-6 py-3">ID</th>
              <th className="px-6 py-3 w-full">Tên đơn vị</th>
              <th className="px-6 py-3 text-right">Thao tác</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {units.map((unit) => (
              <tr key={unit.id} className="hover:bg-gray-50">
                <td className="px-6 py-3 text-gray-500">#{unit.id}</td>
                <td className="px-6 py-3 font-medium">{unit.name}</td>
                <td className="px-6 py-3 text-right space-x-2">
                  <button className="text-blue-600"><Edit className="h-4 w-4" /></button>
                  <button className="text-red-600"><Trash2 className="h-4 w-4" /></button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}