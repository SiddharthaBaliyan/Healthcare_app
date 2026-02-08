"""
Integration tests for the complete pipeline
"""

import pytest
import requests
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestIntegration:
    """Integration tests for the complete pipeline"""
    
    def test_api_and_frontend_connection(self):
        """Test connection between frontend and API"""
        try:
            # Try to connect to both services
            api_response = requests.get("http://127.0.0.1:8000/health", timeout=5)
            assert api_response.status_code == 200
            
            frontend_response = requests.get("http://127.0.0.1:5000/", timeout=5)
            assert frontend_response.status_code in [200, 302]  # 302 if redirected
        except requests.exceptions.ConnectionError:
            pytest.skip("Services not running locally")
    
    def test_end_to_end_prediction(self, sample_patient_data):
        """Test end-to-end prediction flow"""
        try:
            # Prepare payload
            payload = {
                "Age": sample_patient_data['Age'],
                "Sex": sample_patient_data['Sex'],
                "Chest pain type": sample_patient_data['Chest pain type'],
                "BP": sample_patient_data['BP'],
                "Cholesterol": sample_patient_data['Cholesterol'],
                "FBS over 120": sample_patient_data['FBS over 120'],
                "EKG results": sample_patient_data['EKG results'],
                "Max HR": sample_patient_data['Max HR'],
                "Exercise angina": sample_patient_data['Exercise angina'],
                "ST depression": sample_patient_data['ST depression'],
                "Slope of ST": sample_patient_data['Slope of ST'],
                "Number of vessels fluro": sample_patient_data['Number of vessels fluro'],
                "Thallium": sample_patient_data['Thallium']
            }
            
            # Test direct API call
            api_response = requests.post(
                "http://127.0.0.1:8000/predict",
                json=payload,
                timeout=10
            )
            assert api_response.status_code == 200
            data = api_response.json()
            assert "prediction" in data
            
            # Test through frontend
            frontend_response = requests.post(
                "http://127.0.0.1:5000/predict",
                json=payload,
                timeout=10
            )
            assert frontend_response.status_code == 200
        except requests.exceptions.ConnectionError:
            pytest.skip("Services not running locally")
    
    def test_concurrent_predictions(self, sample_patients):
        """Test multiple concurrent predictions"""
        try:
            for patient in sample_patients:
                payload = {
                    "Age": patient['Age'],
                    "Sex": patient['Sex'],
                    "Chest pain type": patient['Chest pain type'],
                    "BP": patient['BP'],
                    "Cholesterol": patient['Cholesterol'],
                    "FBS over 120": patient['FBS over 120'],
                    "EKG results": patient['EKG results'],
                    "Max HR": patient['Max HR'],
                    "Exercise angina": patient['Exercise angina'],
                    "ST depression": patient['ST depression'],
                    "Slope of ST": patient['Slope of ST'],
                    "Number of vessels fluro": patient['Number of vessels fluro'],
                    "Thallium": patient['Thallium']
                }
                
                response = requests.post(
                    "http://127.0.0.1:8000/predict",
                    json=payload,
                    timeout=10
                )
                assert response.status_code == 200
        except requests.exceptions.ConnectionError:
            pytest.skip("API not running locally")
    
    def test_frontend_api_communication(self):
        """Test frontend can communicate with API"""
        try:
            # Check if frontend can reach API
            response = requests.get("http://127.0.0.1:5000/", timeout=5)
            assert response.status_code in [200, 302]
            
            # Check if API is healthy
            api_response = requests.get("http://127.0.0.1:8000/health", timeout=5)
            assert api_response.status_code == 200
            health_data = api_response.json()
            assert health_data["model_loaded"] is True
        except requests.exceptions.ConnectionError:
            pytest.skip("Services not running locally")


class TestDataflow:
    """Test data flow through the pipeline"""
    
    def test_data_processing_consistency(self, sample_patient_data):
        """Test data is processed consistently"""
        try:
            payload = {
                "Age": sample_patient_data['Age'],
                "Sex": sample_patient_data['Sex'],
                "Chest pain type": sample_patient_data['Chest pain type'],
                "BP": sample_patient_data['BP'],
                "Cholesterol": sample_patient_data['Cholesterol'],
                "FBS over 120": sample_patient_data['FBS over 120'],
                "EKG results": sample_patient_data['EKG results'],
                "Max HR": sample_patient_data['Max HR'],
                "Exercise angina": sample_patient_data['Exercise angina'],
                "ST depression": sample_patient_data['ST depression'],
                "Slope of ST": sample_patient_data['Slope of ST'],
                "Number of vessels fluro": sample_patient_data['Number of vessels fluro'],
                "Thallium": sample_patient_data['Thallium']
            }
            
            # Make prediction twice with same data
            response1 = requests.post(
                "http://127.0.0.1:8000/predict",
                json=payload,
                timeout=10
            )
            
            response2 = requests.post(
                "http://127.0.0.1:8000/predict",
                json=payload,
                timeout=10
            )
            
            data1 = response1.json()
            data2 = response2.json()
            
            # Predictions should be identical for same input
            assert data1["prediction"] == data2["prediction"]
            assert data1["probability"] == data2["probability"]
        except requests.exceptions.ConnectionError:
            pytest.skip("API not running locally")
