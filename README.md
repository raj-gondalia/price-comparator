# Price Comparator API

A FastAPI-based application that compares product prices using Google Shopping data and filters results using OpenAI models.

## Features
- Search for product prices across countries using Google Shopping (via Oxylabs API)
- Filter and rank results for relevance using OpenAI's GPT models
- **Optimized LRU caching** with O(1) operations and configurable expiration (default: 2 days)
- Service-oriented architecture with clear separation of concerns
- Comprehensive logging and monitoring endpoints

## Architecture

### Service Layer
- **SearchService**: Handles product search operations with caching
- **FilterService**: Manages result filtering using OpenAI
- **CacheManager**: Optimized LRU cache with O(1) operations using OrderedDict

### Utils Layer
- **Config**: Pydantic-based configuration management
- **Logging**: Centralized logging with file rotation
- **Middleware**: Request logging

---

## Requirements
- Python 3.10+
- [Oxylabs Real-Time Crawler API](https://oxylabs.io/products/real-time-crawler) credentials
- [OpenAI API key](https://platform.openai.com/account/api-keys)

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd price_comparator
```

### 2. Create and configure your environment variables
Create a `.env` file in the project root with the following content:

```ini
# .env.example
OXYLABS_USERNAME=your_oxylabs_username
OXYLABS_PASSWORD=your_oxylabs_password
OPENAI_API_KEY=your_openai_api_key

# Optional configuration
LOG_LEVEL=INFO
CACHE_EXPIRY_DAYS=1
MAX_CACHE_SIZE=1000
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.7
```

### 3. Install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Run the application locally
```bash
uvicorn main:app --reload
```

The API docs will be available at [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Docker

You can also run the application using Docker:

```bash
docker build -t price-comparator .
docker run --env-file .env -p 8000:8000 price-comparator
```

---

## API Endpoints

#### POST `/search`
Search for products and return filtered results.

Request body (JSON):
```json
{
  "country": "United States",
  "query": "iPhone 15",
  "use_cache": true
}
```

Response (JSON):
```json
{
  "results": [
    {
      "title": "Apple iPhone 15 (128GB, Blue)",
      "price": "$799",
      "link": "https://store.example.com/iphone-15",
      "currency": "USD",
      "rating": "4.8",
      "reviews_count": 1200
    }
  ]
}
```

---

## cURL Examples

```bash
# Search for products
curl --location 'http://localhost:8000/search' \
--header 'Content-Type: application/json' \
--data '{
  "country": "India",
  "query": "Samsung s24",
  "use_cache": true
}'
```

---

## Demo

Watch the search functionality in action:

![Search Demo](static/search_example.mov)

---

## Development
- Code formatting: [black](https://github.com/psf/black)
- Imports: [isort](https://github.com/PyCQA/isort)
- Pre-commit hooks: see `.pre-commit-config.yaml`
