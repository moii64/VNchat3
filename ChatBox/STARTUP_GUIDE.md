# 🚀 Hướng Dẫn Khởi Động Intelligent Chatbot

## 📋 Yêu Cầu Hệ Thống

### 🔧 Phần Mềm Cần Thiết

- **Python 3.11+** hoặc **Node.js 18+**
- **Docker Desktop** (khuyến nghị)
- **Git** để clone repository
- **Code Editor** (VS Code, PyCharm, etc.)

### 💻 Hệ Điều Hành

- ✅ **Windows 10/11** (PowerShell hoặc Command Prompt)
- ✅ **macOS 10.15+** (Terminal)
- ✅ **Ubuntu 20.04+** (Terminal)

### 🌐 Kết Nối Internet

- **Bắt buộc**: Để download packages và Docker images
- **Khuyến nghị**: Kết nối ổn định để tránh timeout

## 🎯 Cách 1: Khởi Động Với Docker (Khuyến Nghị)

### Bước 1: Chuẩn Bị Môi Trường

```bash
# 1. Mở terminal/command prompt
# Windows: PowerShell hoặc Command Prompt
# macOS/Linux: Terminal

# 2. Kiểm tra Docker
docker --version
docker-compose --version

# Nếu chưa có Docker, tải từ: https://www.docker.com/products/docker-desktop/
```

### Bước 2: Clone Repository

```bash
# Clone project về máy
git clone <your-repo-url>
cd ChatBox

# Kiểm tra cấu trúc thư mục
dir  # Windows
ls   # macOS/Linux
```

**Cấu trúc thư mục mong đợi:**
```
ChatBox/
├── backend/
├── frontend/
├── scripts/
├── docs/
├── docker-compose.yml
├── .env.example
└── README.md
```

### Bước 3: Cấu Hình Environment

```bash
# 1. Tạo file .env từ template
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# 2. Mở file .env và chỉnh sửa
# Sử dụng code editor hoặc notepad
code .env  # VS Code
notepad .env  # Windows Notepad
```

**Nội dung file .env cần chỉnh sửa:**
```env
# OpenAI API Key (BẮT BUỘC)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Database (có thể để mặc định)
DATABASE_URL=postgresql://postgres:password@postgres:5432/chatbot

# Redis (có thể để mặc định)
REDIS_URL=redis://redis:6379

# Chroma Vector Store (có thể để mặc định)
CHROMA_DIR=./chroma_db

# Security (có thể để mặc định)
SECRET_KEY=your-secret-key-here
```

**🔑 Lấy OpenAI API Key:**
1. Truy cập: https://platform.openai.com/api-keys
2. Đăng nhập/đăng ký tài khoản
3. Click "Create new secret key"
4. Copy key và paste vào file .env

### Bước 4: Khởi Động Hệ Thống

```bash
# 1. Khởi động tất cả services
docker-compose up -d

# 2. Kiểm tra trạng thái
docker-compose ps

# 3. Xem logs nếu cần
docker-compose logs -f
```

**Kết quả mong đợi:**
```
      Name                     Command               State           Ports         
--------------------------------------------------------------------------------
chatbox-backend-1   uvicorn main:app --host 0.0.0.0 --port 8000   Up      0.0.0.0:8000->8000/tcp
chatbox-frontend-1  npm run dev                                   Up      0.0.0.0:3000->3000/tcp
chatbox-postgres-1  docker-entrypoint.sh postgres                 Up      0.0.0.0:5432->5432/tcp
chatbox-redis-1     docker-entrypoint.sh redis-server            Up      0.0.0.0:6379->6379/tcp
```

### Bước 5: Kiểm Tra Hoạt Động

```bash
# 1. Kiểm tra Backend API
curl http://localhost:8000/api/health
# Hoặc mở browser: http://localhost:8000/api/health

# 2. Kiểm tra Frontend
# Mở browser: http://localhost:3000

# 3. Kiểm tra Database
docker exec chatbox-postgres-1 psql -U postgres -d chatbot -c "\dt"
```

## 🖥️ Cách 2: Khởi Động Local Development

### Bước 1: Chuẩn Bị Python Environment

```bash
# 1. Kiểm tra Python version
python --version  # Phải >= 3.11

# 2. Tạo virtual environment
python -m venv venv

# 3. Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Kiểm tra pip
pip --version
```

### Bước 2: Cài Đặt Backend Dependencies

```bash
# 1. Di chuyển vào thư mục backend
cd backend

# 2. Cài đặt packages
pip install -r requirements.txt

# 3. Kiểm tra cài đặt
pip list | findstr fastapi  # Windows
pip list | grep fastapi     # macOS/Linux
```

### Bước 3: Cài Đặt Frontend Dependencies

```bash
# 1. Mở terminal mới (giữ terminal backend)
# 2. Di chuyển vào thư mục frontend
cd frontend

# 3. Cài đặt Node.js packages
npm install

# 4. Kiểm tra cài đặt
npm list --depth=0
```

### Bước 4: Khởi Động Services

**Terminal 1 - Backend:**
```bash
cd backend
# Kích hoạt virtual environment nếu chưa
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Chạy FastAPI server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - Database (nếu cần):**
```bash
# Sử dụng Docker chỉ cho database
docker-compose up postgres redis -d
```

## 🔍 Kiểm Tra Và Troubleshooting

### ✅ Kiểm Tra Backend

```bash
# 1. Health check
curl http://localhost:8000/api/health

# 2. API documentation
# Mở browser: http://localhost:8000/docs

# 3. Kiểm tra logs
# Nếu dùng Docker:
docker-compose logs backend

# Nếu chạy local:
# Xem terminal đang chạy uvicorn
```

**Kết quả mong đợi:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### ✅ Kiểm Tra Frontend

```bash
# 1. Mở browser: http://localhost:3000
# 2. Kiểm tra console (F12 > Console)
# 3. Kiểm tra Network tab
```

**Giao diện mong đợi:**
- 2 tabs: "Chat" và "Documents"
- Input box để nhập câu hỏi
- Không có lỗi JavaScript trong console

### ✅ Kiểm Tra Database

```bash
# Nếu dùng Docker:
docker exec chatbox-postgres-1 psql -U postgres -d chatbot -c "\dt"

# Nếu chạy local PostgreSQL:
psql -h localhost -U postgres -d chatbot -c "\dt"
```

**Kết quả mong đợi:**
```
            List of relations
 Schema |     Name      | Type  |  Owner   
--------+---------------+-------+----------
 public | conversations | table | postgres
 public | documents     | table | postgres
 public | messages      | table | postgres
 public | users         | table | postgres
```

## 🚨 Xử Lý Lỗi Thường Gặp

### ❌ Lỗi Docker

**"docker command not found"**
```bash
# Cài đặt Docker Desktop
# Windows/macOS: https://www.docker.com/products/docker-desktop/
# Ubuntu: sudo apt install docker.io docker-compose
```

**"Port already in use"**
```bash
# Kiểm tra port đang sử dụng
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # macOS/Linux

# Dừng service đang sử dụng port hoặc thay đổi port
```

### ❌ Lỗi Python

**"uvicorn is not recognized"**
```bash
# Giải pháp nhanh nhất
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Hoặc reinstall
pip uninstall uvicorn
pip install uvicorn[standard]
```

**"Module not found"**
```bash
# Kiểm tra virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Reinstall packages
pip install -r requirements.txt
```

### ❌ Lỗi Node.js

**"npm command not found"**
```bash
# Cài đặt Node.js từ: https://nodejs.org/
# Chọn LTS version (18.x hoặc 20.x)
```

**"Port 3000 already in use"**
```bash
# Thay đổi port trong frontend/vite.config.ts
export default defineConfig({
  server: {
    port: 3001  # Thay đổi từ 3000 sang 3001
  }
})
```

### ❌ Lỗi Database

**"Connection refused"**
```bash
# Kiểm tra PostgreSQL service
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

**"Authentication failed"**
```bash
# Kiểm tra file .env
# Đảm bảo DATABASE_URL đúng format:
DATABASE_URL=postgresql://postgres:password@localhost:5432/chatbot
```

## 🎉 Khởi Động Thành Công!

### ✅ Checklist Hoàn Thành

- [ ] Backend API chạy tại http://localhost:8000
- [ ] Frontend UI chạy tại http://localhost:3000
- [ ] Database kết nối thành công
- [ ] Health check trả về "healthy"
- [ ] Không có lỗi trong logs

### 🚀 Bước Tiếp Theo

1. **Upload tài liệu mẫu:**
   ```bash
   cd scripts
   python ingest_sample_docs.py
   ```

2. **Test chat:**
   - Mở http://localhost:3000
   - Chọn tab "Chat"
   - Nhập câu hỏi: "Làm thế nào để reset mật khẩu?"

3. **Kiểm tra API:**
   - Mở http://localhost:8000/docs
   - Test các endpoints

### 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. **Kiểm tra logs** trước tiên
2. **Đọc USAGE_GUIDE.md** để troubleshooting
3. **Tạo issue** với thông tin chi tiết
4. **Cung cấp** error message và steps to reproduce

---

**🎯 Mục tiêu**: Hoàn thành setup trong 15-30 phút với Docker, hoặc 30-60 phút với local development.

