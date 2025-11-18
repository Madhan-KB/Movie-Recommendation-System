from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import pandas as pd
from pathlib import Path

CORS_HEADER = 'Content-Type'

# Serve frontend static files from the sibling `frontend/` folder
FRONTEND_DIR = Path(__file__).resolve().parent.parent / 'frontend'
app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path='')
CORS(app)  # Enable CORS for frontend communication

# Load the trained model on startup
print("Loading model...")
with open('model.pkl', 'rb') as f:
    model_data = pickle.load(f)

data = model_data['data']
similarity = model_data['similarity']
print("Model loaded successfully!")

def recommend_movies(movie_name, top_n=10):
    """
    Recommend top N similar movies based on input
    """
    # Case-insensitive search
    movie_matches = data[data['title'].str.lower() == movie_name.lower()]
    
    if movie_matches.empty:
        # Try partial match
        movie_matches = data[data['title'].str.lower().str.contains(movie_name.lower(), na=False)]
        if movie_matches.empty:
            return None
        # Use first match
        movie_index = movie_matches.index[0]
    else:
        movie_index = movie_matches.index[0]
    
    # Get similarity scores
    distances = similarity[movie_index]
    
    # Sort and get top N similar movies
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:top_n+1]
    
    recommendations = []
    for i in movies_list:
        recommendations.append({
            'title': data.iloc[i[0]].title,
            'similarity_score': round(float(i[1]), 4)
        })
    
    return recommendations

@app.route('/')
def home():
    """Serve the frontend index.html"""
    return app.send_static_file('index.html')


@app.route('/api', methods=['GET'])
def api_info():
    """API health/info endpoint (used by the frontend to check backend availability)"""
    return jsonify({
        'message': 'Movie Recommendation API',
        'status': 'running',
        'endpoints': {
            '/recommend': 'POST - Get movie recommendations',
            '/movies': 'GET - Get all available movies',
            '/search': 'GET - Search movies by name'
        }
    })

@app.route('/recommend', methods=['POST'])
def recommend():
    """
    Endpoint to get movie recommendations
    Request body: {"movie_name": "Avatar"}
    """
    try:
        data_input = request.get_json()
        movie_name = data_input.get('movie_name', '')
        
        if not movie_name:
            return jsonify({
                'success': False,
                'error': 'Movie name is required'
            }), 400
        
        recommendations = recommend_movies(movie_name)
        
        if recommendations is None:
            return jsonify({
                'success': False,
                'error': f'Movie "{movie_name}" not found in database'
            }), 404
        
        return jsonify({
            'success': True,
            'movie': movie_name,
            'recommendations': recommendations
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/movies', methods=['GET'])
def get_all_movies():
    """
    Get all available movies in the database
    """
    try:
        movies_list = data['title'].tolist()
        return jsonify({
            'success': True,
            'count': len(movies_list),
            'movies': movies_list[:100]  # Return first 100 for performance
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/search', methods=['GET'])
def search_movies():
    """
    Search movies by partial name
    Query parameter: ?q=avatar
    """
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query is required'
            }), 400
        
        # Case-insensitive partial match
        matches = data[data['title'].str.lower().str.contains(query.lower(), na=False)]
        movies_list = matches['title'].tolist()
        
        return jsonify({
            'success': True,
            'query': query,
            'count': len(movies_list),
            'movies': movies_list[:20]  # Return top 20 matches
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)