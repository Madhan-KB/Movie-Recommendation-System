// Configuration
const API_BASE_URL = 'http://localhost:5000'; // Change for production

// DOM Elements
const movieInput = document.getElementById('movieInput');
const searchBtn = document.getElementById('searchBtn');
const loadingIndicator = document.getElementById('loadingIndicator');
const errorMessage = document.getElementById('errorMessage');
const resultsSection = document.getElementById('resultsSection');
const searchedMovie = document.getElementById('searchedMovie');
const recommendationsList = document.getElementById('recommendationsList');
const searchSuggestions = document.getElementById('searchSuggestions');

// Event Listeners
searchBtn.addEventListener('click', handleSearch);
movieInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSearch();
    }
});

// Debounced search suggestions
let searchTimeout;
movieInput.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    const query = e.target.value.trim();
    
    if (query.length >= 2) {
        searchTimeout = setTimeout(() => {
            fetchSuggestions(query);
        }, 300);
    } else {
        searchSuggestions.innerHTML = '';
    }
});

// Main Search Handler
async function handleSearch() {
    const movieName = movieInput.value.trim();
    
    if (!movieName) {
        showError('Please enter a movie name');
        return;
    }
    
    // Hide previous results and errors
    hideElement(errorMessage);
    hideElement(resultsSection);
    searchSuggestions.innerHTML = '';
    
    // Show loading
    showElement(loadingIndicator);
    
    try {
        const recommendations = await getRecommendations(movieName);
        
        // Hide loading
        hideElement(loadingIndicator);
        
        // Display results
        displayRecommendations(movieName, recommendations);
        
    } catch (error) {
        hideElement(loadingIndicator);
        showError(error.message);
    }
}

// Fetch Recommendations from API
async function getRecommendations(movieName) {
    try {
        const response = await fetch(`${API_BASE_URL}/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                movie_name: movieName
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch recommendations');
        }
        
        if (!data.success) {
            throw new Error(data.error || 'No recommendations found');
        }
        
        return data.recommendations;
        
    } catch (error) {
        if (error.message.includes('fetch')) {
            throw new Error('Cannot connect to server. Please ensure the backend is running.');
        }
        throw error;
    }
}

// Fetch Search Suggestions
async function fetchSuggestions(query) {
    try {
        const response = await fetch(`${API_BASE_URL}/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data.success && data.movies.length > 0) {
            displaySuggestions(data.movies);
        } else {
            searchSuggestions.innerHTML = '';
        }
    } catch (error) {
        console.error('Error fetching suggestions:', error);
    }
}

// Display Search Suggestions
function displaySuggestions(movies) {
    searchSuggestions.innerHTML = movies.map(movie => `
        <div class="suggestion-item" onclick="selectSuggestion('${movie.replace(/'/g, "\\'")}')">
            ${movie}
        </div>
    `).join('');
}

// Select Suggestion
function selectSuggestion(movieName) {
    movieInput.value = movieName;
    searchSuggestions.innerHTML = '';
    handleSearch();
}

// Display Recommendations
function displayRecommendations(movieName, recommendations) {
    searchedMovie.textContent = movieName;
    
    recommendationsList.innerHTML = recommendations.map((movie, index) => `
        <div class="movie-card">
            <div class="movie-number">#${index + 1}</div>
            <div class="movie-title">${movie.title}</div>
            <div class="movie-score">
                Similarity: ${(movie.similarity_score * 100).toFixed(1)}%
            </div>
        </div>
    `).join('');
    
    showElement(resultsSection);
    
    // Smooth scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Show Error Message
function showError(message) {
    errorMessage.textContent = message;
    showElement(errorMessage);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideElement(errorMessage);
    }, 5000);
}

// Utility Functions
function showElement(element) {
    element.classList.remove('hidden');
}

function hideElement(element) {
    element.classList.add('hidden');
}

// Check Backend Connection on Page Load
async function checkBackendConnection() {
    try {
        // Frontend now checks the API health endpoint
        const response = await fetch(`${API_BASE_URL}/api`);
        const data = await response.json();
        console.log('Backend connected:', data.message);
    } catch (error) {
        console.warn('Backend not connected. Make sure to start the Flask server.');
    }
}

// Initialize
checkBackendConnection();