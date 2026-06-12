# AI Video Generator

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI app with Replicate integration
│   ├── requirements.txt      # Python dependencies
│   └── .env.example         # Environment template
└── frontend/
    ├── src/
    │   ├── App.js           # Main React component
    │   ├── App.css          # Styling
    │   └── index.js         # React entry point
    ├── public/
    │   └── index.html       # HTML template
    └── package.json         # NPM dependencies
```

## Setup Instructions

### 1. Get Replicate API Key
- Sign up at https://replicate.com
- Get your API token from https://replicate.com/account

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create and activate virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env and add your Replicate API key
```

### 3. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install
```

### 4. Run the Project

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn main:app --reload
# Backend runs on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
# Frontend runs on http://localhost:3000
```

### 5. Usage

1. Open http://localhost:3000 in your browser
2. Choose one of two options:
   - **Upload an image** and generate a video based on it
   - **Enter a text prompt** to generate a video from scratch
3. Click the generate button and wait for the AI to process
4. Download or view your generated video

## API Endpoints

### POST `/generate-video`
Upload an image file to generate a video
- **Request**: Multipart form data with image file
- **Response**: `{"status": "success", "video_url": "..."}`

### POST `/generate-video-from-prompt`
Generate a video from a text prompt
- **Query**: `prompt` (string)
- **Response**: `{"status": "success", "video_url": "..."}`

## Technologies Used
- **Backend**: FastAPI, Python 3.8+
- **Frontend**: React 18
- **AI/ML**: Replicate API
- **HTTP Client**: Axios

## Notes
- Videos are generated using Replicate's image-to-video models
- Generation time depends on the model and current API load
- API requires internet connection for Replicate integration

## License
MIT
