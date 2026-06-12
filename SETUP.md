# AI Video Generator

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI app with Hugging Face integration
│   ├── requirements.txt      # Python dependencies
│   └── .env.example         # Environment template
├── frontend/
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   ├── App.css          # Styling
│   │   └── index.js         # React entry point
│   ├── public/
│   │   └── index.html       # HTML template
│   └── package.json         # NPM dependencies
└── generated_videos/        # Output directory for generated videos
```

## Features

✅ **100% FREE** - Uses Hugging Face free inference API
✅ **Image-to-Video** - Convert images into videos
✅ **Text-to-Video** - Generate videos from text prompts
✅ **Open Source** - Uses DAMO-VILAB models
✅ **Beautiful UI** - Modern React interface with gradient design

## Setup Instructions

### 1. Get Hugging Face API Token (FREE!)
- Sign up at https://huggingface.co (completely free)
- Go to https://huggingface.co/settings/tokens
- Create a new "User Access Token"
- Copy the token

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
# Edit .env and add your Hugging Face API token
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
- **Response**: `{"status": "success", "video_path": "..."}`

### POST `/generate-video-from-prompt`
Generate a video from a text prompt
- **Query**: `prompt` (string)
- **Response**: `{"status": "success", "video_path": "..."}`

### GET `/video/{file_path}`
Retrieve a generated video file

## Technologies Used
- **Backend**: FastAPI, Python 3.8+
- **Frontend**: React 18
- **AI/ML**: Hugging Face Inference API (FREE)
- **Models**: DAMO-VILAB (Open Source)
- **HTTP Client**: Axios

## Cost
**COMPLETELY FREE!** 🎉
- No credit card required for Hugging Face
- Unlimited free API calls
- Open-source models

## Notes
- Videos are generated using Hugging Face's free inference API
- Generation time depends on model complexity and current API load
- Internet connection required for API calls
- Videos are saved locally in `generated_videos/` directory

## Troubleshooting

**"Model is loading" error:**
- First-time model loads take longer (1-2 minutes)
- Wait a bit and try again

**"Unauthorized" error:**
- Check your HF_API_TOKEN in `.env`
- Make sure token has proper permissions

**Generation takes too long:**
- Hugging Face free API sometimes has queues
- Models are loaded on-demand, first request takes longer

## License
MIT
