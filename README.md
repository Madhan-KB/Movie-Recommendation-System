# 🎬 Movie Recommendation System - Complete Guide

A full-stack movie recommendation system using Machine Learning (TF-IDF & Cosine Similarity) with Flask backend and vanilla JavaScript frontend.

---

## 📋 Table of Contents
1. [Project Structure](#project-structure)
2. [Dataset Preparation](#dataset-preparation)
3. [Model Training](#model-training)
4. [Backend Setup](#backend-setup)
5. [Frontend Setup](#frontend-setup)
6. [Local Testing](#local-testing)
7. [Deployment](#deployment)

---

## 📁 Project Structure

```
movie-recommendation-system/
├── backend/
│   ├── app.py                 # Flask API
│   ├── train_model.py         # ML model training script
│   ├── model.pkl              # Trained model (generated)
│   ├── requirements.txt       # Python dependencies
│   └── tmdb_5000_movies.csv   # Dataset
│   └── tmdb_5000_credits.csv  # Dataset
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── README.md
```

---

## 📊 Dataset Preparation

### Step 1: Download Dataset

**Option A: TMDB 5000 Movie Dataset (Recommended)**
1. Visit: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata
2. Download `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv`
3. Place both files in the `backend/` directory

**Option B: MovieLens Dataset**
1. Visit: https://grouplens.org/datasets/movielens/
2. Download MovieLens 25M or 100K dataset
3. Modify `train_model.py` to work with MovieLens format

### Dataset Structure (TMDB)
- **tmdb_5000_movies.csv**: Contains movie details (title, overview, genres, keywords)
- **tmdb_5000_credits.csv**: Contains cast and crew information

---

## 🤖 Model Training

### Step 2: Install Python Dependencies

```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Train the Model

```bash
python train_model.py
```

**What happens during training:**

1. **Data Loading**: Reads CSV files and merges them
2. **Data Cleaning**: Removes null values and duplicates
3. **Feature Extraction**:
   - Extracts genres (e.g., Action, Comedy)
   - Extracts keywords (e.g., space, adventure)
   - Extracts top 3 cast members
   - Extracts director name
   - Combines overview text
4. **Feature Engineering**:
   - Combines all features into a single "tags" column
   - Converts to lowercase for consistency
   - Removes spaces from multi-word names
5. **TF-IDF Vectorization**:
   - Creates numerical vectors from text tags
   - Uses max 5000 features
   - Removes English stop words
6. **Similarity Calculation**:
   - Computes cosine similarity between all movie pairs
   - Creates similarity matrix
7. **Model Saving**:
   - Saves preprocessed data, similarity matrix, and vectorizer to `model.pkl`

**Expected Output:**
```
Loading and cleaning data...
Extracting features...
Creating TF-IDF vectors...
Calculating similarity matrix...
Saving model...
Model saved successfully as 'model.pkl'
```

**File Size:** `model.pkl` will be approximately 200-400 MB depending on dataset size.

---

## 🔧 Backend Setup

### Step 4: Configure Flask API

The `app.py` file contains the Flask REST API with the following endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API status and documentation |
| `/recommend` | POST | Get movie recommendations |
| `/movies` | GET | List all available movies |
| `/search` | GET | Search movies by partial name |

### Step 5: Run Backend Locally

```bash
python app.py
```

Server will start at: `http://localhost:5000`

**Test the API:**
```bash
# Test recommendation endpoint
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"movie_name": "Avatar"}'

# Test search endpoint
curl http://localhost:5000/search?q=avatar
```

---

## 🎨 Frontend Setup

### Step 6: Configure Frontend

The frontend consists of three files that work together:

**index.html** - Structure
- Search bar for movie input
- Button to trigger recommendations
- Loading indicator
- Results display section

**style.css** - Styling
- Modern gradient background
- Responsive card layout
- Smooth animations and transitions
- Mobile-friendly design

**script.js** - Functionality
- Sends POST request to `/recommend` endpoint
- Handles loading states and errors
- Displays recommendations dynamically
- Provides search suggestions

### Step 7: Update API URL

In `script.js`, update the API URL:

```javascript
// For local development
const API_BASE_URL = 'http://localhost:5000';

// For production (after deployment)
const API_BASE_URL = 'https://your-backend-url.onrender.com';
```

---

## 🧪 Local Testing

### Step 8: Test Complete System

**Terminal 1 - Run Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Run Frontend:**
```bash
cd frontend
python -m http.server 8000
# Or use any local server
```

**Access Application:**
- Frontend: `http://localhost:8000`
- Backend API: `http://localhost:5000`

**Test Flow:**
1. Open frontend in browser
2. Enter a movie name (e.g., "Avatar")
3. Click "Get Recommendations"
4. View top 10 similar movies

---

## 🚀 Deployment

### Option 1: Deploy Backend on Render

**Step 9: Prepare for Render**

Create `render.yaml`:
```yaml
services:
  - type: web
    name: movie-recommendation-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

**Deploy Steps:**
1. Push code to GitHub repository
2. Go to https://render.com and sign up
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Click "Create Web Service"
7. **Important**: Upload `model.pkl` via Render Dashboard (Files section) or include in repo

**Note:** model.pkl is large. Consider using:
- Render Disk storage
- External storage (AWS S3, Google Cloud Storage)
- Git LFS for version control

### Option 2: Deploy Backend on Railway

1. Visit https://railway.app
2. Create new project from GitHub repo
3. Railway auto-detects Python and installs dependencies
4. Set environment variables if needed
5. Deploy automatically

### Option 3: Deploy Frontend on Netlify

**Step 10: Deploy Frontend**

**Method 1: Drag & Drop**
1. Go to https://netlify.com
2. Drag the `frontend/` folder to Netlify
3. Site will be live instantly

**Method 2: GitHub Integration**
1. Push frontend code to GitHub
2. Connect repository to Netlify
3. Configure build settings:
   - **Build Command**: (leave empty)
   - **Publish Directory**: `frontend`
4. Deploy

**Update API URL:**
After backend deployment, update `script.js`:
```javascript
const API_BASE_URL = 'https://your-app.onrender.com';
```

### Option 4: Deploy Frontend on Vercel

1. Visit https://vercel.com
2. Import GitHub repository
3. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `frontend`
4. Deploy

---

## 🔒 CORS Configuration

Ensure CORS is enabled in `app.py`:

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # Allows all origins

# Or restrict to specific domain:
# CORS(app, origins=['https://your-frontend.netlify.app'])
```

---

## 🐛 Troubleshooting

### Common Issues

**1. "Movie not found" Error**
- Check movie name spelling
- Try partial search using `/search` endpoint
- Verify movie exists in dataset

**2. Backend Connection Failed**
- Ensure Flask server is running
- Check CORS configuration
- Verify API_BASE_URL in script.js

**3. Model Loading Error**
- Ensure model.pkl is in backend directory
- Check file size (should be 200-400 MB)
- Re-train model if corrupted

**4. Large File Deployment**
- Use Git LFS for model.pkl
- Consider cloud storage (S3, GCS)
- Split model into chunks if needed

---

## 📈 Model Performance

**Metrics:**
- **Dataset Size**: ~4,800 movies (TMDB)
- **Feature Dimensions**: 5,000 TF-IDF features
- **Similarity Algorithm**: Cosine Similarity
- **Recommendation Time**: ~50-100ms per query
- **Accuracy**: Based on content similarity (genres, keywords, cast)

**Improvements:**
- Add collaborative filtering
- Include user ratings
- Implement hybrid recommendation
- Add movie posters/images
- Include release year filtering

---

## 🎯 API Usage Examples

### JavaScript (Fetch)
```javascript
fetch('http://localhost:5000/recommend', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ movie_name: 'Inception' })
})
.then(res => res.json())
.then(data => console.log(data.recommendations));
```

### Python (Requests)
```python
import requests

response = requests.post(
    'http://localhost:5000/recommend',
    json={'movie_name': 'Inception'}
)
print(response.json())
```

### cURL
```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"movie_name": "The Dark Knight"}'
```

---

## 📝 License

This project is open-source and available under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new features
- Improve model accuracy
- Enhance UI/UX
- Fix bugs

---

## 📧 Support

For issues or questions:
- Create an issue on GitHub
- Check existing documentation
- Review API responses for error details

---

**Built with ❤️ using Flask, Scikit-learn, and Vanilla JavaScript**