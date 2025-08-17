# Hướng Dẫn Sử Dụng Intelligent Chatbot

## Mục Lục
1. [Khởi Động Ứng Dụng](#khởi-động-ứng-dụng)
2. [Giao Diện Chat](#giao-diện-chat)
3. [Quản Lý Tài Liệu](#quản-lý-tài-liệu)
4. [Sử Dụng API](#sử-dụng-api)
5. [Troubleshooting](#troubleshooting)
6. [Tips & Best Practices](#tips--best-practices)

## Khởi Động Ứng Dụng

### Cách 1: Sử Dụng Docker (Khuyến Nghị)

```bash
# 1. Clone repository
git clone <your-repo-url>
cd ChatBox

# 2. Tạo file .env từ template
cp .env.example .env
# Chỉnh sửa .env với API key OpenAI và các thông tin cần thiết

# 3. Khởi động toàn bộ hệ thống
docker-compose up -d

# 4. Kiểm tra trạng thái
docker-compose ps
```

**Các service sẽ chạy tại:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Cách 2: Chạy Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt

# Chạy uvicorn (chọn 1 trong các cách sau)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
# HOẶC (nếu gặp lỗi trên Windows)
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend (terminal mới)
cd frontend
npm install
npm run dev
```

## Giao Diện Chat

### 1. Truy Cập Chat Interface

Mở trình duyệt và truy cập: **http://localhost:3000**

Bạn sẽ thấy 2 tab chính:
- **Chat**: Giao diện chat với bot
- **Documents**: Quản lý tài liệu

### 2. Bắt Đầu Chat

1. **Chọn tab "Chat"**
2. **Nhập câu hỏi** vào ô input ở cuối màn hình
3. **Nhấn Enter** hoặc click nút gửi (➤)
4. **Đợi bot trả lời** - bot sẽ:
   - Tìm kiếm tài liệu liên quan
   - Tạo câu trả lời dựa trên context
   - Hiển thị kết quả

### 3. Tính Năng Chat

- **Lịch sử chat**: Bot tự động lưu và hiển thị lịch sử
- **Context awareness**: Bot nhớ các câu hỏi trước đó trong session
- **RAG responses**: Bot trả lời dựa trên tài liệu đã được ingest
- **Fallback**: Nếu không tìm thấy thông tin, bot sẽ thông báo rõ ràng

### 4. Ví Dụ Câu Hỏi

```
✅ Câu hỏi tốt:
- "Làm thế nào để reset mật khẩu?"
- "Chính sách hoàn tiền như thế nào?"
- "Có thể thay đổi gói dịch vụ không?"

❌ Câu hỏi không phù hợp:
- "Thời tiết hôm nay thế nào?" (không liên quan domain)
- "1+1=?" (câu hỏi toán học đơn giản)
```

## Quản Lý Tài Liệu

### 1. Upload Tài Liệu

1. **Chọn tab "Documents"**
2. **Click "Choose File"** hoặc kéo thả file
3. **Chọn file** (hỗ trợ: PDF, TXT, MD)
4. **Click "Upload Document"**
5. **Đợi xử lý** - hệ thống sẽ:
   - Đọc nội dung file
   - Chia thành chunks nhỏ
   - Tạo embeddings
   - Lưu vào vector database

### 2. Xem Danh Sách Tài Liệu

- **Tên file**: Tên gốc của file upload
- **Loại**: PDF, TXT, hoặc MD
- **Kích thước**: Số chunks đã tạo
- **Ngày upload**: Thời gian file được xử lý

### 3. Xóa Tài Liệu

1. **Tìm file** cần xóa trong danh sách
2. **Click nút "Delete"** (🗑️)
3. **Xác nhận** việc xóa
4. **File sẽ bị xóa** khỏi cả database và vector store

### 4. Ingest Tài Liệu Mẫu

```bash
# Chạy script để ingest tài liệu mẫu
cd scripts
python ingest_sample_docs.py
```

Script này sẽ tạo:
- FAQ document với các câu hỏi thường gặp
- Tài liệu hướng dẫn cơ bản
- Dữ liệu test để demo RAG

## Sử Dụng API

### 1. Chat API

```bash
# Gửi tin nhắn
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "message": "Làm thế nào để reset mật khẩu?"
  }'
```

**Response:**
```json
{
  "answer": "Để reset mật khẩu, bạn có thể...",
  "source_documents": ["faq.md", "user_guide.pdf"],
  "conversation_id": "conv_123"
}
```

### 2. Document Management API

```bash
# Upload document
curl -X POST "http://localhost:8000/api/documents/ingest" \
  -F "file=@document.pdf"

# List documents
curl "http://localhost:8000/api/documents"

# Delete document
curl -X DELETE "http://localhost:8000/api/documents/doc_123"
```

### 3. Conversation API

```bash
# Get user conversations
curl "http://localhost:8000/api/conversations/user123"

# Get messages in conversation
curl "http://localhost:8000/api/conversations/conv_123/messages"

# Update conversation title
curl -X PUT "http://localhost:8000/api/conversations/conv_123/title" \
  -H "Content-Type: application/json" \
  -d '{"title": "Hỗ trợ kỹ thuật"}'
```

## Troubleshooting

### 1. Lỗi Thường Gặp

**Uvicorn không chạy được (Windows):**
```bash
# Giải pháp nhanh nhất
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Hoặc sử dụng Docker
docker-compose up backend
```

**Bot không trả lời:**
```bash
# Kiểm tra backend logs
docker-compose logs backend

# Kiểm tra OpenAI API key
echo $OPENAI_API_KEY
```

**Không thể upload file:**
```bash
# Kiểm tra quyền thư mục
ls -la backend/uploads/

# Kiểm tra disk space
df -h
```

**Database connection error:**
```bash
# Kiểm tra PostgreSQL
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

### 2. Debug Mode

```bash
# Backend với debug logging
cd backend
uvicorn main:app --reload --log-level debug

# Frontend với console logs
cd frontend
npm run dev
# Mở Developer Tools > Console
```

### 3. Lỗi Uvicorn trên Windows

**Lỗi: "uvicorn is not recognized"**

**Giải pháp 1: Sử dụng Python module**
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Giải pháp 2: Kiểm tra PATH và reinstall**
```bash
# Kiểm tra pip packages
pip list | findstr uvicorn

# Reinstall uvicorn
pip uninstall uvicorn
pip install uvicorn[standard]

# Hoặc install với --user flag
pip install --user uvicorn[standard]
```

**Giải pháp 3: Sử dụng virtual environment**
```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt (Windows)
venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Chạy uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Giải pháp 4: Sử dụng Docker (Khuyến nghị)**
```bash
# Nếu gặp vấn đề với local Python
docker-compose up backend
```

### 3. Reset Hệ Thống

```bash
# Xóa tất cả data
docker-compose down -v
docker-compose up -d

# Hoặc reset từng service
docker-compose restart backend
docker-compose restart frontend
```

## Tips & Best Practices

### 1. Tối Ưu Chat Experience

- **Câu hỏi rõ ràng**: Viết câu hỏi cụ thể, tránh câu hỏi mơ hồ
- **Context liên quan**: Hỏi các vấn đề liên quan đến tài liệu đã upload
- **Kiên nhẫn**: Bot cần thời gian để xử lý và tìm kiếm thông tin

### 2. Quản Lý Tài Liệu Hiệu Quả

- **Chia nhỏ**: Upload tài liệu theo chủ đề, tránh file quá lớn
- **Format chuẩn**: Sử dụng PDF hoặc Markdown để đảm bảo chất lượng
- **Metadata**: Đặt tên file có ý nghĩa để dễ quản lý

### 3. Monitoring & Analytics

```bash
# Xem logs real-time
docker-compose logs -f

# Kiểm tra performance
docker stats

# Backup database
docker exec postgres pg_dump -U postgres chatbot > backup.sql
```

### 4. Security Considerations

- **API Keys**: Không commit file .env vào git
- **File Upload**: Chỉ upload file từ nguồn đáng tin cậy
- **Rate Limiting**: Tránh spam API calls
- **Input Validation**: Bot có cơ chế chống prompt injection

### 5. Scaling Tips

- **Vector Database**: Sử dụng Pinecone thay vì Chroma cho production
- **Caching**: Redis cache để tăng tốc độ response
- **Load Balancing**: Sử dụng Nginx cho multiple backend instances
- **Monitoring**: Prometheus + Grafana cho metrics

## Hỗ Trợ

Nếu gặp vấn đề:

1. **Kiểm tra logs** trước khi báo cáo
2. **Tạo issue** với thông tin chi tiết
3. **Cung cấp** error message và steps to reproduce
4. **Kiểm tra** documentation và troubleshooting guide

---

**Lưu ý**: Hướng dẫn này dành cho phiên bản hiện tại. Kiểm tra README.md để cập nhật thông tin mới nhất.
