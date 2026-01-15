import axios from 'axios';

// 1. Tạo bản sao của Axios với cấu hình cơ bản
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL, // Lấy link từ .env.local
  headers: {
    'Content-Type': 'application/json',
    'ngrok-skip-browser-warning': 'true',
  },
});

// 2. Tự động thêm Token vào mỗi lần gọi API (nếu có)
api.interceptors.request.use(
  (config) => {
    // Kiểm tra xem đang chạy ở trình duyệt hay không
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('accessToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;