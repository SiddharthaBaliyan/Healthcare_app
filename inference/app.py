"""
Heart Disease Prediction FastAPI Inference Server
Provides REST API endpoints for heart disease prediction
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pickle
import os
import logging
import numpy as np
from typing import List

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Heart Disease Prediction API",
    description="API for predicting heart disease presence",
    version="1.0.0"
)

# Get model directory path
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')

# Load model and preprocessing objects
def load_model_artifacts():
    """Load saved model and preprocessing artifacts"""
    try:
        model_path = os.path.join(MODEL_DIR, 'heart_disease_model.pkl')
        scaler_path = os.path.join(MODEL_DIR, 'scaler.pkl')
        encoder_path = os.path.join(MODEL_DIR, 'label_encoder.pkl')
        features_path = os.path.join(MODEL_DIR, 'feature_columns.pkl')
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        
        with open(encoder_path, 'rb') as f:
            label_encoder = pickle.load(f)
        
        with open(features_path, 'rb') as f:
            feature_columns = pickle.load(f)
        
        logger.info("Model artifacts loaded successfully")
        return model, scaler, label_encoder, feature_columns
    
    except FileNotFoundError as e:
        logger.error(f"Model artifacts not found: {e}")
        logger.error("Please run the training pipeline first")
        raise


# Load models on startup
try:
    model, scaler, label_encoder, feature_columns = load_model_artifacts()
    model_loaded = True
except Exception as e:
    model_loaded = False
    logger.error(f"Failed to load model: {e}")


# Define request/response models
class PatientData(BaseModel):
    """Patient data for prediction"""
    Age: int = Field(..., ge=1, le=150, description="Patient age")
    Sex: int = Field(..., ge=0, le=1, description="Sex (0=Female, 1=Male)")
    Chest_pain_type: int = Field(..., alias="Chest pain type", ge=1, le=4, description="Chest pain type (1-4)")
    BP: int = Field(..., ge=50, le=250, description="Blood pressure")
    Cholesterol: int = Field(..., ge=0, le=600, description="Cholesterol level")
    FBS_over_120: int = Field(..., alias="FBS over 120", ge=0, le=1, description="Fasting blood sugar > 120")
    EKG_results: int = Field(..., alias="EKG results", ge=0, le=2, description="EKG results (0-2)")
    Max_HR: int = Field(..., alias="Max HR", ge=30, le=250, description="Maximum heart rate achieved")
    Exercise_angina: int = Field(..., alias="Exercise angina", ge=0, le=1, description="Exercise induced angina")
    ST_depression: float = Field(..., alias="ST depression", ge=0, le=10, description="ST depression")
    Slope_of_ST: int = Field(..., alias="Slope of ST", ge=1, le=3, description="Slope of ST segment")
    Number_of_vessels_fluro: int = Field(..., alias="Number of vessels fluro", ge=0, le=3, description="Number of vessels")
    Thallium: int = Field(..., ge=3, le=7, description="Thallium value")
    
    class Config:
        schema_extra = {
            "example": {
                "Age": 58,
                "Sex": 1,
                "Chest pain type": 4,
                "BP": 152,
                "Cholesterol": 239,
                "FBS over 120": 0,
                "EKG results": 0,
                "Max HR": 158,
                "Exercise angina": 1,
                "ST depression": 3.6,
                "Slope of ST": 2,
                "Number of vessels fluro": 2,
                "Thallium": 7
            }
        }


class PredictionResponse(BaseModel):
    """Prediction response"""
    prediction: str = Field(..., description="Presence or Absence")
    probability: float = Field(..., description="Prediction probability")
    confidence: float = Field(..., description="Confidence score")
    message: str = Field(..., description="Prediction message")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    message: str


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if model_loaded else "unhealthy",
        model_loaded=model_loaded,
        message="Model is ready for predictions" if model_loaded else "Model artifacts not found"
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict(patient: PatientData):
    """
    Predict heart disease presence
    
    Returns:
        - prediction: "Presence" or "Absence"
        - probability: Probability of the prediction (0-1)
        - confidence: Confidence level (0-100%)
        - message: Human-readable prediction message
    """
    if not model_loaded:
        raise HTTPException(
            status_code=503,
            detail="Model is not loaded. Please ensure model artifacts exist in the models directory."
        )
    
    try:
        # Prepare input data in the correct order
        input_data = np.array([[
            patient.Age,
            patient.Sex,
            patient.Chest_pain_type,
            patient.BP,
            patient.Cholesterol,
            patient.FBS_over_120,
            patient.EKG_results,
            patient.Max_HR,
            patient.Exercise_angina,
            patient.ST_depression,
            patient.Slope_of_ST,
            patient.Number_of_vessels_fluro,
            patient.Thallium
        ]])
        
        # Scale input
        input_scaled = scaler.transform(input_data)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        prediction_proba = model.predict_proba(input_scaled)[0]
        
        # Get prediction label
        prediction_label = label_encoder.inverse_transform([prediction])[0]
        probability = float(max(prediction_proba))
        confidence = probability * 100
        
        # Generate message
        if prediction_label == "Presence":
            message = f"⚠️  Heart disease presence detected with {confidence:.2f}% confidence. Please consult a healthcare professional."
        else:
            message = f"✅ No heart disease detected with {confidence:.2f}% confidence. Continue healthy lifestyle."
        
        logger.info(f"Prediction made: {prediction_label} (confidence: {confidence:.2f}%)")
        
        return PredictionResponse(
            prediction=prediction_label,
            probability=probability,
            confidence=confidence,
            message=message
        )
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Error during prediction: {str(e)}"
        )


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "app": "Heart Disease Prediction API",
        "version": "1.0.0",
        "status": "healthy" if model_loaded else "unhealthy",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs",
            "openapi": "/openapi.json"
        },
        "documentation": "Visit /docs for interactive API documentation"
    }


@app.get("/info")
async def info():
    """Get API and model information"""
    return {
        "api_name": "Heart Disease Prediction API",
        "version": "1.0.0",
        "description": "ML-based API for predicting heart disease presence",
        "model_type": "Random Forest Classifier",
        "features_count": len(feature_columns) if model_loaded else 0,
        "features": feature_columns if model_loaded else [],
        "output_classes": list(label_encoder.classes_) if model_loaded else [],
        "model_status": "loaded" if model_loaded else "not_loaded"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
