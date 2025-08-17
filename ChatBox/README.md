# Intelligent Chatbot - Hướng dẫn thực hành

## Mục tiêu sản phẩm

Một **Intelligent Chatbot** có khả năng:
- Trả lời tự nhiên các câu hỏi về domain cho trước (FAQ / tài liệu nội bộ)
- Kết hợp **RAG** (retrieval-augmented generation) — lấy tài liệu liên quan + sinh trả lời
- Lưu lịch sử, phân loại intent, fallback chuyển human
- Có UI chat cơ bản, backend API, và deploy được

## Kiến trúc tổng quát

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   AI Layer      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (OpenAI +     │
│                 │    │                 │    │    Vector DB)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐
                       │   Database      │
                       │   (PostgreSQL)  │
                       └─────────────────┘
```

## Công nghệ sử dụng

- **Backend**: FastAPI (Python)
- **Frontend**: React + TypeScript
- **AI**: OpenAI GPT-4, OpenAI Embeddings
- **Vector DB**: Chroma (local)
- **Database**: PostgreSQL
- **Cache**: Redis
- **Orchestration**: LangChain
- **Deployment**: Docker + Docker Compose

## Cài đặt và chạy

### Yêu cầu hệ thống
- Python 3.8+
- Node.js 16+
- Docker & Docker Compose
- OpenAI API key

### Bước 1: Clone và setup
```bash
git clone <repository>
cd ChatBox
cp .env.example .env
# Cập nhật OPENAI_API_KEY trong .env
```

### Bước 2: Chạy với Docker
```bash
docker-compose up -d
```

### Bước 3: Chạy development
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Cấu trúc dự án

```
ChatBox/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Config, database
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   ├── requirements.txt
│   └── main.py
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom hooks
│   │   └── types/          # TypeScript types
│   ├── package.json
│   └── index.html
├── docs/                    # Sample documents
├── scripts/                 # Utility scripts
├── docker-compose.yml
└── README.md
```

## Lab roadmap

### Lab 1: API chat cơ bản
- Setup FastAPI + OpenAI integration
- Endpoint `/chat` cơ bản

### Lab 2: Lưu lịch sử & context
- Database models cho users và conversations
- Session management

### Lab 3: RAG với Vector Store
- Document ingestion
- Embeddings generation
- Vector search

### Lab 4: Prompt engineering
- System prompts
- Context injection
- Safety measures

### Lab 5: Intent classification
- Basic intent detection
- Fallback mechanisms

### Lab 6: Deploy & monitoring
- Docker containerization
- Basic metrics và logging

## API Endpoints

- `POST /api/chat` - Chat với bot
- `GET /api/conversations/{user_id}` - Lấy lịch sử chat
- `POST /api/documents/ingest` - Ingest tài liệu mới
- `GET /api/health` - Health check

## Evaluation Metrics

- **Accuracy**: % câu trả lời đúng
- **RAG Fidelity**: % câu trả lời có dẫn nguồn
- **Response Time**: Thời gian phản hồi trung bình
- **User Satisfaction**: Điểm đánh giá từ người dùng

## Contributing

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## License

MIT License
