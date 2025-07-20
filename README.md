# Pic-to-Caption: AI Image Captioning API

Pic-to-Caption is an AI-powered API that generates descriptive alt text for images using FastAPI and the BLIP model from Hugging Face Transformers. Easily upload images and receive automatic captions for improved accessibility and SEO.

## Features
- Generate alt text for images using state-of-the-art AI
- FastAPI backend for high performance
- Secure API key authentication
- Docker support for easy deployment
- Static file serving for web integration

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.10+

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pic-to-caption.git
   cd pic-to-caption
   ```
2. Create a `.env` file in the root directory and add your API key:
   ```env
   API_KEY=your_api_key_here
   ```
3. Build and run the Docker container:
   ```bash
   docker-compose up --build
   ```
4. Access the API at `http://localhost:8000`

## API Usage
### Generate Alt Text
- **Endpoint:** `/generate-alt`
- **Method:** `POST`
- **Headers:** `X-API-Key: your_api_key_here`
- **Body:** Multipart form with image file

#### Example Request (using `curl`):
```bash
curl -X POST "http://localhost:8000/generate-alt" \
     -H "X-API-Key: your_api_key_here" \
     -F "file=@example.jpeg"
```

#### Example Response
```json
{
  "alt_text": "A group of people standing in a park."
}
```

## License
MIT
