# Price Comparator API

A FastAPI-based application that compares product prices using Google Shopping data and filters results using OpenAI models.

## Features
- Search for product prices across countries using Google Shopping (via Oxylabs API)
- Filter and rank results for relevance using OpenAI's GPT models

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

## API Usage

### POST `/search`
Request body (JSON):
```json
{
  "country": "US",
  "query": "iPhone 15"
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
    },
    ...
  ]
}
```

---

## Development
- Code formatting: [black](https://github.com/psf/black)
- Imports: [isort](https://github.com/PyCQA/isort)
- Pre-commit hooks: see `.pre-commit-config.yaml`
