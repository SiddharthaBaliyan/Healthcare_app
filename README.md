# Heart Disease Prediction Pipeline

A complete end-to-end machine learning pipeline for heart disease prediction with training and FastAPI inference capabilities.

## Project Structure

```
CLASSIFIER1/
├── data/
│   ├── train.csv           # Training data (labeled)
│   ├── test.csv            # Test data
│   └── top_rated_movies.csv
├── training/
│   └── train.py            # Training pipeline script
├── inference/
│   └── app.py              # FastAPI inference server
├── models/
│   ├── heart_disease_model.pkl    # Trained model
│   ├── scaler.pkl                 # Feature scaler
│   ├── label_encoder.pkl          # Label encoder
│   └── feature_columns.pkl        # Feature columns list
├── logs/
│   └── training_*.log      # Training logs
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Setup Instructions

### 1. Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

## Usage

### Train the Model

```powershell
python training/train.py
```

This will:
- Load the training data from `data/train.csv`
- Preprocess and clean the data
- Split into train/test sets (80/20)
- Train a Random Forest classifier
- Evaluate model performance
- Save model artifacts to `models/` directory
- Log all activities to `logs/` directory

### Run Inference Server

```powershell
# Option 1: Using uvicorn directly
uvicorn inference.app:app --host 0.0.0.0 --port 8000 --reload

# Option 2: Using Python
python -m uvicorn inference.app:app --host 0.0.0.0 --port 8000

# Option 3: Production with gunicorn (Unix/Linux only)
gunicorn -w 4 -k uvicorn.workers.UvicornWorker inference.app:app
```

The API will be available at: `http://localhost:8000`

### API Endpoints

#### 1. Health Check
```
GET /health
```
Returns model status and health information.

#### 2. Make Prediction
```
POST /predict
Content-Type: application/json

{
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
```

Returns:
```json
{
  "prediction": "Presence",
  "probability": 0.85,
  "confidence": 85.0,
  "message": "⚠️ Heart disease presence detected with 85.00% confidence. Please consult a healthcare professional."
}
```

#### 3. API Information
```
GET /
GET /info
```

#### 4. Interactive Documentation
```
GET /docs        # Swagger UI
GET /redoc       # ReDoc
GET /openapi.json # OpenAPI schema
```

## Model Features

The model uses 13 medical features:

1. **Age** (int): Patient age
2. **Sex** (int): 0=Female, 1=Male
3. **Chest pain type** (int): 1=Typical angina, 2=Atypical angina, 3=Non-anginal pain, 4=Asymptomatic
4. **BP** (int): Resting blood pressure (mmHg)
5. **Cholesterol** (int): Serum cholesterol (mg/dl)
6. **FBS over 120** (int): Fasting blood sugar > 120 mg/dl (0=No, 1=Yes)
7. **EKG results** (int): 0=Normal, 1=ST-T abnormality, 2=LV hypertrophy
8. **Max HR** (int): Maximum heart rate achieved
9. **Exercise angina** (int): Exercise induced angina (0=No, 1=Yes)
10. **ST depression** (float): ST depression induced by exercise
11. **Slope of ST** (int): 1=Upsloping, 2=Flat, 3=Downsloping
12. **Number of vessels fluro** (int): Number of major vessels (0-3)
13. **Thallium** (int): Thallium test result (3-7)

## Model Performance

After training, check the logs in `logs/` directory for:
- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix
- Classification Report

## Testing with curl

```bash
# Health check
curl http://localhost:8000/health

# Make prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

## Troubleshooting

### Model Not Found Error
- Ensure you've run `python training/train.py` first
- Check that model files exist in the `models/` directory

### Port Already in Use
```powershell
# Change port in the command
uvicorn inference.app:app --port 8001
```

### Virtual Environment Issues
```powershell
# Deactivate current environment
deactivate

# Remove and recreate
rmdir /s /q venv
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Dependencies

- **scikit-learn**: ML algorithms and preprocessing
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **fastapi**: Web framework for building APIs
- **uvicorn**: ASGI server for FastAPI
- **pydantic**: Data validation

## License

This project is provided as-is for educational purposes.
