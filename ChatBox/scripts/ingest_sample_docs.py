#!/usr/bin/env python3
"""
Script để ingest tài liệu mẫu vào Intelligent Chatbot
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent / 'backend'))

from app.services.document_service import DocumentService
from app.core.database import SessionLocal

# Sample documents content
SAMPLE_DOCS = {
    "faq_general.md": """# FAQ Chung về Dịch vụ

## Câu hỏi thường gặp

### 1. Làm thế nào để đăng ký tài khoản?
Để đăng ký tài khoản, bạn cần:
- Truy cập trang web chính thức
- Nhấn nút "Đăng ký"
- Điền thông tin cá nhân
- Xác nhận email

### 2. Quên mật khẩu phải làm sao?
Nếu quên mật khẩu:
- Nhấn "Quên mật khẩu" trên trang đăng nhập
- Nhập email đã đăng ký
- Kiểm tra email và làm theo hướng dẫn""",

    "product_guide.md": """# Hướng dẫn Sản phẩm

## Tính năng chính

### Tính năng 1: Quản lý dự án
- Tạo dự án mới
- Phân công nhiệm vụ
- Theo dõi tiến độ
- Báo cáo kết quả

### Tính năng 2: Giao tiếp nhóm
- Chat nhóm real-time
- Chia sẻ file
- Lịch họp
- Thông báo""",

    "pricing_info.md": """# Thông tin Giá cả

## Gói cơ bản - 99,000đ/tháng
- Tối đa 5 người dùng
- Tính năng cơ bản
- Hỗ trợ email
- Dung lượng 10GB

## Gói chuyên nghiệp - 299,000đ/tháng
- Tối đa 20 người dùng
- Tất cả tính năng
- Hỗ trợ 24/7
- Dung lượng 100GB"""
}

async def ingest_sample_documents():
    """Ingest tài liệu mẫu vào hệ thống"""
    db = SessionLocal()
    
    try:
        doc_service = DocumentService(db)
        
        print("🚀 Bắt đầu ingest tài liệu mẫu...")
        
        for filename, content in SAMPLE_DOCS.items():
            print(f"📄 Đang xử lý: {filename}")
            
            # Tạo mock UploadFile object
            class MockUploadFile:
                def __init__(self, filename, content):
                    self.filename = filename
                    self._content = content.encode('utf-8')
                
                async def read(self):
                    return self._content
            
            mock_file = MockUploadFile(filename, content)
            
            # Ingest document
            result = await doc_service.ingest_document(mock_file)
            print(f"✅ Đã ingest: {filename} - {result['chunks_created']} chunks")
        
        print("\n🎉 Hoàn thành ingest tài liệu mẫu!")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(ingest_sample_documents())
