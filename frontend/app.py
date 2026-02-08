"""
Heart Disease Predictor Frontend - Flask Application
Beautiful web interface for heart disease prediction
"""

from flask import Flask, render_template, request, jsonify
import requests
import logging
from datetime import datetime
import os

# Configuration
API_BASE_URL = "http://127.0.0.1:8000"
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def index():
    """Home page"""
    try:
        # Check API health
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        api_status = response.json()
    except:
        api_status = {"status": "unhealthy", "model_loaded": False}
    
    return render_template('index.html', api_status=api_status)


@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for making predictions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'Age', 'Sex', 'Chest_pain_type', 'BP', 'Cholesterol',
            'FBS_over_120', 'EKG_results', 'Max_HR', 'Exercise_angina',
            'ST_depression', 'Slope_of_ST', 'Number_of_vessels_fluro', 'Thallium'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing field: {field}'
                }), 400
        
        # Prepare data for API
        payload = {
            "Age": int(data['Age']),
            "Sex": int(data['Sex']),
            "Chest pain type": int(data['Chest_pain_type']),
            "BP": int(data['BP']),
            "Cholesterol": int(data['Cholesterol']),
            "FBS over 120": int(data['FBS_over_120']),
            "EKG results": int(data['EKG_results']),
            "Max HR": int(data['Max_HR']),
            "Exercise angina": int(data['Exercise_angina']),
            "ST depression": float(data['ST_depression']),
            "Slope of ST": int(data['Slope_of_ST']),
            "Number of vessels fluro": int(data['Number_of_vessels_fluro']),
            "Thallium": int(data['Thallium'])
        }
        
        # Call FastAPI backend
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Prediction successful: {result['prediction']}")
            return jsonify({
                'success': True,
                'data': result
            }), 200
        else:
            error_msg = response.json().get('detail', 'Unknown error')
            logger.error(f"Prediction failed: {error_msg}")
            return jsonify({
                'success': False,
                'error': error_msg
            }), response.status_code
    
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to API server")
        return jsonify({
            'success': False,
            'error': 'Cannot connect to prediction API. Please ensure the API server is running on port 8000.'
        }), 503
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/info', methods=['GET'])
def api_info():
    """Get API information"""
    try:
        response = requests.get(f"{API_BASE_URL}/info", timeout=5)
        if response.status_code == 200:
            return jsonify(response.json()), 200
    except:
        pass
    
    return jsonify({
        'error': 'Cannot retrieve API information'
    }), 503


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            return jsonify({
                'frontend_status': 'healthy',
                'api': response.json()
            }), 200
    except:
        pass
    
    return jsonify({
        'frontend_status': 'healthy',
        'api': {'status': 'unhealthy', 'message': 'API server not responding'}
    }), 503


@app.route('/history', methods=['GET'])
def get_history():
    """Get prediction history (placeholder)"""
    return jsonify({
        'message': 'History feature coming soon'
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Page not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"Server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    logger.info("Starting Heart Disease Predictor Frontend...")
    logger.info(f"Frontend running on http://127.0.0.1:5000")
    logger.info(f"API Server: {API_BASE_URL}")
    app.run(debug=True, host='127.0.0.1', port=5000)
