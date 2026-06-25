# 🤖 AI News Intelligence Platform

A distributed microservice system for AI-powered news ingestion, LLM-based summarization, and real-time sentiment analysis.

## ✨ Features

- **📰 Multi-source News Ingestion** - Integrate with NewsAPI, Guardian, NY Times, RSS feeds
- **🧠 LLM-powered Summarization** - Generate concise summaries using OpenAI GPT-4
- **😊 Sentiment Analysis** - Real-time sentiment classification (positive/negative/neutral)
- **🏷️ Topic Clustering** - Automatic topic extraction and grouping
- **⚡ Async Processing** - Non-blocking job processing with Celery
- **📊 REST API** - Comprehensive API for querying articles and analytics
- **🗄️ PostgreSQL** - Production-grade data storage
- **🔍 Full-text Search** - Search articles by title and content
- **📈 Sentiment Trends** - Track sentiment evolution over time

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL 13+
- Redis 6+ (for caching and task queue)
- Docker & Docker Compose (optional)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/vikasmlv/AI-news-intelligence.git
cd AI-news-intelligence
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
# OR using Poetry
poetry install
```

4. **Setup environment variables**

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/news_intelligence

# News APIs
NEWSAPI_KEY=your_key_here
GUARDIAN_API_KEY=your_key_here

# LLM
OPENAI_API_KEY=your_key_here
```

5. **Initialize database**

```bash
python -c "from src.core.database import init_db; init_db()"
```

6. **Run the API server**

```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### Health Check

```bash
GET /api/v1/health
```

### Articles

```bash
# List articles
GET /api/v1/articles?page=1&limit=10&source=NewsAPI&sentiment=positive

# Get single article
GET /api/v1/articles/{article_id}

# Search articles
POST /api/v1/articles/search?query=AI&page=1&limit=10
```

### Sentiment Analysis

```bash
# Get sentiment analysis
GET /api/v1/sentiment?limit=100

# Get sentiment statistics
GET /api/v1/sentiment/stats
```

### Topics

```bash
# Get topics
GET /api/v1/topics?limit=20

# Get articles for topic
GET /api/v1/topics/{topic_id}/articles?limit=50
```

## 🏗️ Project Structure

```
.
├── src/
│   ├── api/
│   │   ├── main.py              # FastAPI app initialization
│   │   └── routes/              # API endpoints
│   │       ├── articles.py
│   │       ├── health.py
│   │       ├── sentiment.py
│   │       └── topics.py
│   ├── models/
│   │   ├── base.py              # Base SQLAlchemy model
│   │   ├── article.py           # Pydantic models
│   │   ├── article_db.py        # SQLAlchemy model
│   │   ├── source.py            # News source model
│   │   └── processing_job.py    # Job tracking model
│   ├── services/
│   │   ├── article_service.py   # Article business logic
│   │   ├── sentiment_service.py # Sentiment analysis
│   │   ├── ingestion_service.py # Article ingestion
│   │   └── news_sources/        # News connectors
│   ├── core/
│   │   ├── config.py            # Settings management
│   │   ├── database.py          # DB session management
│   │   └── logging.py           # Logging setup
│   └── __init__.py
├── tests/                        # Unit & integration tests
├── docker-compose.yml            # Docker services
├── Dockerfile                    # API container
├── pyproject.toml               # Poetry config
├── requirements.txt             # Pip dependencies
├── .env.example                 # Example env file
└── README.md                    # This file
```

## 🐳 Docker Setup

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_articles.py

# Run with coverage
pytest --cov=src tests/
```

## 📝 Examples

### Python Client

```python
import requests

# Get articles
response = requests.get(
    "http://localhost:8000/api/v1/articles",
    params={"page": 1, "limit": 10}
)
articles = response.json()

# Search articles
response = requests.post(
    "http://localhost:8000/api/v1/articles/search",
    params={"query": "AI", "limit": 5}
)
results = response.json()

# Get sentiment analysis
response = requests.get(
    "http://localhost:8000/api/v1/sentiment"
)
sentiment_data = response.json()
```

### cURL

```bash
# List articles
curl "http://localhost:8000/api/v1/articles?page=1&limit=10"

# Search articles
curl -X POST "http://localhost:8000/api/v1/articles/search?query=AI"

# Get sentiment stats
curl "http://localhost:8000/api/v1/sentiment/stats"
```

## 🔧 Configuration

Edit `.env` to customize:

| Variable | Description | Default |
|----------|-------------|----------|
| `APP_ENV` | Environment (development/production) | development |
| `DATABASE_URL` | PostgreSQL connection string | - |
| `NEWSAPI_KEY` | NewsAPI.org API key | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `API_PORT` | Server port | 8000 |
| `LOG_LEVEL` | Logging level | INFO |

## 📦 Dependencies

### Core
- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database
- **Pydantic** - Data validation
- **PostgreSQL** - Database

### AI/ML
- **Transformers** - Sentiment analysis models
- **OpenAI** - GPT-4 for summarization
- **Numpy/Pandas** - Data processing

### Async/Jobs
- **Celery** - Task queue
- **Redis** - Message broker & cache
- **aiohttp** - Async HTTP client

### Development
- **Pytest** - Testing framework
- **Black** - Code formatting
- **Mypy** - Type checking
- **Pylint** - Linting

## 📊 Database Schema

### Articles Table

```sql
CREATE TABLE articles (
    id UUID PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    summary TEXT,
    source VARCHAR(200) NOT NULL,
    source_url VARCHAR(1000) UNIQUE NOT NULL,
    sentiment VARCHAR(20),
    sentiment_score FLOAT,
    keywords TEXT[],
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## 🛠️ Development

### Code Style

```bash
# Format code with Black
black src/ tests/

# Sort imports with isort
isort src/ tests/

# Lint with Flake8
flake8 src/ tests/

# Type check with Mypy
mypy src/
```

### Pre-commit Hooks

```bash
# Install pre-commit
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

## 🚢 Deployment

### Using Docker

```bash
# Build image
docker build -t ai-news-intelligence .

# Run container
docker run -p 8000:8000 --env-file .env ai-news-intelligence
```

### Using Gunicorn

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 src.api.main:app
```

## 📋 Roadmap

- [ ] LLM-based article summarization
- [ ] Multi-language support
- [ ] Advanced topic modeling (LDA, BERTopic)
- [ ] Vector embeddings for semantic search
- [ ] Real-time streaming with WebSockets
- [ ] ML model versioning and monitoring
- [ ] Dashboard UI with React
- [ ] Kubernetes deployment manifests

## 🤝 Contributing

Contributions are welcome! Please follow the steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

**Author:** Vikas Kumar  
**Email:** [your-email@example.com](mailto:your-email@example.com)  
**GitHub:** [@vikasmlv](https://github.com/vikasmlv)

## 🙏 Acknowledgments

- NewsAPI.org for news data
- OpenAI for GPT models
- Hugging Face for transformers
- FastAPI community

---

**Made with ❤️ by Vikas Kumar**
