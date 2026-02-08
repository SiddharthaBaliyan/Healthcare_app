"""
Unit tests for the FastAPI inference server
"""

import pytest
import json
import sys
from pathlib import Path

# Import the FastAPI app
sys.path.insert(0, str(Path(__file__).parent.parent))
from inference.app import app
from fastapi.testclient import TestClient

client = TestClient(app)


class TestAPIHealth:
    """Test API health check endpoints"""
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "model_loaded" in data
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "app" in data
        assert "endpoints" in data
    
    def test_info_endpoint(self):
        """Test info endpoint"""
        response = client.get("/info")
        assert response.status_code == 200
        data = response.json()
        assert "api_name" in data
        assert "model_type" in data


class TestPredictionEndpoint:
    """Test prediction endpoints"""
    
    def test_prediction_success(self, sample_patient_data):
        """Test successful prediction"""
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
        
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert "probability" in data
        assert "confidence" in data
        assert data["prediction"] in ["Presence", "Absence"]
    
    def test_prediction_probability_range(self, sample_patient_data):
        """Test prediction probability is in valid range"""
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
        
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert 0 <= data["probability"] <= 1
        assert 0 <= data["confidence"] <= 100
    
    def test_prediction_missing_field(self, sample_patient_data):
        """Test prediction with missing required field"""
        payload = sample_patient_data.copy()
        del payload['Age']
        
        response = client.post("/predict", json=payload)
        assert response.status_code == 400
    
    def test_prediction_invalid_age(self, sample_patient_data):
        """Test prediction with invalid age"""
        payload = sample_patient_data.copy()
        payload['Age'] = 200  # Invalid age
        
        response = client.post("/predict", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_prediction_invalid_sex(self, sample_patient_data):
        """Test prediction with invalid sex value"""
        payload = sample_patient_data.copy()
        payload['Sex'] = 5  # Invalid sex (should be 0 or 1)
        
        response = client.post("/predict", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_prediction_batch_multiple(self, sample_patients):
        """Test predictions for multiple patients"""
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
            
            response = client.post("/predict", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert "prediction" in data
            assert data["prediction"] in ["Presence", "Absence"]


class TestResponseStructure:
    """Test response structure and format"""
    
    def test_prediction_response_structure(self, sample_patient_data):
        """Test prediction response has correct structure"""
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
        
        response = client.post("/predict", json=payload)
        data = response.json()
        
        required_fields = ["prediction", "probability", "confidence", "message"]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
    
    def test_prediction_message_present(self, sample_patient_data):
        """Test prediction message is meaningful"""
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
        
        response = client.post("/predict", json=payload)
        data = response.json()
        
        assert len(data["message"]) > 0
        assert "confidence" in data["message"].lower() or data["prediction"].lower() in data["message"].lower()


class TestAPIErrorHandling:
    """Test API error handling"""
    
    def test_invalid_json_payload(self):
        """Test invalid JSON payload"""
        response = client.post(
            "/predict",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code in [400, 422]
    
    def test_prediction_with_negative_age(self, sample_patient_data):
        """Test prediction with negative age"""
        payload = sample_patient_data.copy()
        payload['Age'] = -5
        
        response = client.post("/predict", json=payload)
        assert response.status_code == 422
    
    def test_prediction_with_negative_bp(self, sample_patient_data):
        """Test prediction with negative blood pressure"""
        payload = sample_patient_data.copy()
        payload['BP'] = -100
        
        response = client.post("/predict", json=payload)
        assert response.status_code == 422


class TestDocumentation:
    """Test API documentation endpoints"""
    
    def test_swagger_ui_available(self):
        """Test Swagger UI is available"""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_available(self):
        """Test ReDoc is available"""
        response = client.get("/redoc")
        assert response.status_code == 200
    
    def test_openapi_schema_available(self):
        """Test OpenAPI schema is available"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "paths" in data
