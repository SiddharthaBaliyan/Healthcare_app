"""
Configuration file for Heart Disease Prediction Pipeline
"""

import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# Training configuration
TRAINING_CONFIG = {
    'train_data_path': os.path.join(DATA_DIR, 'train.csv'),
    'test_size': 0.2,
    'random_state': 42,
    'model_params': {
        'n_estimators': 100,
        'max_depth': 15,
        'random_state': 42,
        'n_jobs': -1
    }
}

# API configuration
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 8000,
    'reload': True,  # Set to False in production
    'title': 'Heart Disease Prediction API',
    'version': '1.0.0'
}

# Model paths
MODEL_PATHS = {
    'model': os.path.join(MODELS_DIR, 'heart_disease_model.pkl'),
    'scaler': os.path.join(MODELS_DIR, 'scaler.pkl'),
    'label_encoder': os.path.join(MODELS_DIR, 'label_encoder.pkl'),
    'feature_columns': os.path.join(MODELS_DIR, 'feature_columns.pkl')
}

# Feature columns (in order)
FEATURE_COLUMNS = [
    'Age', 'Sex', 'Chest pain type', 'BP', 'Cholesterol',
    'FBS over 120', 'EKG results', 'Max HR', 'Exercise angina',
    'ST depression', 'Slope of ST', 'Number of vessels fluro', 'Thallium'
]

# Logging configuration
LOG_CONFIG = {
    'log_dir': LOGS_DIR,
    'log_level': 'INFO',
    'log_format': '%(asctime)s - %(levelname)s - %(message)s'
}
