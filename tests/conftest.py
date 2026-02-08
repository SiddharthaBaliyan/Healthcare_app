"""
Test configuration and fixtures for the Heart Disease Predictor
"""

import pytest
import os
import sys
import pandas as pd
import pickle
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture(scope="session")
def model_dir():
    """Get model directory path"""
    return os.path.join(PROJECT_ROOT, 'models')


@pytest.fixture(scope="session")
def data_dir():
    """Get data directory path"""
    return os.path.join(PROJECT_ROOT, 'data')


@pytest.fixture(scope="session")
def training_dir():
    """Get training directory path"""
    return os.path.join(PROJECT_ROOT, 'training')


@pytest.fixture(scope="session")
def load_trained_model(model_dir):
    """Load the trained model"""
    model_path = os.path.join(model_dir, 'heart_disease_model.pkl')
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    return None


@pytest.fixture(scope="session")
def load_scaler(model_dir):
    """Load the scaler"""
    scaler_path = os.path.join(model_dir, 'scaler.pkl')
    if os.path.exists(scaler_path):
        with open(scaler_path, 'rb') as f:
            return pickle.load(f)
    return None


@pytest.fixture(scope="session")
def load_label_encoder(model_dir):
    """Load the label encoder"""
    encoder_path = os.path.join(model_dir, 'label_encoder.pkl')
    if os.path.exists(encoder_path):
        with open(encoder_path, 'rb') as f:
            return pickle.load(f)
    return None


@pytest.fixture(scope="session")
def load_feature_columns(model_dir):
    """Load feature columns"""
    features_path = os.path.join(model_dir, 'feature_columns.pkl')
    if os.path.exists(features_path):
        with open(features_path, 'rb') as f:
            return pickle.load(f)
    return None


@pytest.fixture(scope="session")
def sample_patient_data():
    """Sample patient data for testing"""
    return {
        'Age': 58,
        'Sex': 1,
        'Chest pain type': 4,
        'BP': 152,
        'Cholesterol': 239,
        'FBS over 120': 0,
        'EKG results': 0,
        'Max HR': 158,
        'Exercise angina': 1,
        'ST depression': 3.6,
        'Slope of ST': 2,
        'Number of vessels fluro': 2,
        'Thallium': 7
    }


@pytest.fixture(scope="session")
def sample_patients():
    """Multiple sample patients for batch testing"""
    return [
        {
            'Age': 58, 'Sex': 1, 'Chest pain type': 4, 'BP': 152,
            'Cholesterol': 239, 'FBS over 120': 0, 'EKG results': 0,
            'Max HR': 158, 'Exercise angina': 1, 'ST depression': 3.6,
            'Slope of ST': 2, 'Number of vessels fluro': 2, 'Thallium': 7
        },
        {
            'Age': 40, 'Sex': 0, 'Chest pain type': 1, 'BP': 120,
            'Cholesterol': 200, 'FBS over 120': 0, 'EKG results': 0,
            'Max HR': 130, 'Exercise angina': 0, 'ST depression': 0.0,
            'Slope of ST': 1, 'Number of vessels fluro': 0, 'Thallium': 3
        },
        {
            'Age': 75, 'Sex': 1, 'Chest pain type': 3, 'BP': 180,
            'Cholesterol': 300, 'FBS over 120': 1, 'EKG results': 2,
            'Max HR': 120, 'Exercise angina': 1, 'ST depression': 2.5,
            'Slope of ST': 2, 'Number of vessels fluro': 2, 'Thallium': 7
        }
    ]
