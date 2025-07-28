# Advanced Comment Remover

A production-grade web application that removes comments from source code for 10+ programming languages. Built with FastAPI backend and modern HTML/CSS/JavaScript frontend.

## Features

- **10+ Language Support**: Python, JavaScript, TypeScript, Java, C++, C, Go, PHP, Rust, Ruby
- **High Performance**: Handles files with 2,000-10,000+ lines efficiently
- **Modular Architecture**: Clean separation of concerns with dedicated processors
- **Modern UI**: Dark/light mode, drag-and-drop upload, live preview
- **Production Ready**: Async processing, error handling, rate limiting

## Quick Start

### Backend Setup

```bash
cd backend
pip install -r ../requirements.txt
python main.py
```

### Frontend

Open `frontend/index.html` in your browser or serve via the FastAPI static files.

### API Endpoints

- `POST /api/v1/process` - Process code directly
- `POST /api/v1/process-file` - Upload and process files
- `GET /api/v1/languages` - Get supported languages

## Architecture

```
backend/
├── core/           # Language processors
├── routes/         # FastAPI routes
├── services/       # Business logic
├── schemas/        # Request/response models
├── utils/          # Helper functions
└── tests/          # Test suite
```

## Deployment

### Vercel
```bash
vercel deploy
```

### Local Development
```bash
uvicorn backend.main:app --reload
```

## Testing

```bash
cd backend
pytest tests/
```

## Supported Languages

- Python (with docstring handling)
- JavaScript/TypeScript
- Java
- C/C++
- Go
- PHP
- Rust
- Ruby

## Performance

- Async processing for large files
- Chunked processing for 50,000+ line files
- Memory-efficient streaming
- Production-grade error handling