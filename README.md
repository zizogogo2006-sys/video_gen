# Social Video Generator

Generates short-form social videos. Uses OpenAI to write scripts and create images, and MoviePy to put them together.

## Architecture
- Language: Python 3.11+
- LLM / Generation: OpenAI GPT-4o & DALL-E 3
- Video Processing: MoviePy & ImageMagick

## Setup

Run locally with Docker:
```bash
docker-compose up --build
```

Run tests:
```bash
pytest tests/
```
