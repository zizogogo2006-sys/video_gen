# AI Social Video Generator

Enterprise-grade pipeline for generating short-form social media videos (TikTok/Reels/Shorts). Integrates OpenAI for scriptwriting and image generation, and MoviePy for compositing.

## Architecture
- **Language**: Python 3.11+
- **LLM / Generation**: OpenAI GPT-4o & DALL-E 3
- **Video Processing**: MoviePy & ImageMagick

## Infrastructure
This service is fully containerized and includes a CI/CD pipeline.

### Running Locally with Docker
```bash
docker-compose up --build
```

### Running Tests
We use Pytest for continuous integration.
```bash
pytest tests/
```
