"""
Unit tests for the training pipeline
"""

import pytest
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Import training module
sys.path.insert(0, str(Path(__file__).parent.parent))
from training.train import HeartDiseaseTrainer


class TestTrainingPipeline:
    """Test cases for the training pipeline"""
    
    def test_trainer_initialization(self, data_dir):
        """Test if trainer can be initialized"""
        data_path = os.path.join(data_dir, 'train.csv')
        trainer = HeartDiseaseTrainer(data_path)
        assert trainer is not None
        assert trainer.data_path == data_path
    
    def test_data_loading(self, data_dir):
        """Test data loading functionality"""
        data_path = os.path.join(data_dir, 'train.csv')
        trainer = HeartDiseaseTrainer(data_path)
        
        df = trainer.load_data()
        assert df is not None
        assert len(df) > 0
        assert 'Heart Disease' in df.columns
    
    def test_data_loading_shape(self, data_dir):
        """Test data shape after loading"""
        data_path = os.path.join(data_dir, 'train.csv')
        trainer = HeartDiseaseTrainer(data_path)
        
        df = trainer.load_data()
        # After sampling, should have 50,000 rows
        assert df.shape[0] <= 50000
        assert df.shape[1] == 15  # 15 columns
    
    def test_data_preprocessing(self, data_dir):
        """Test data preprocessing"""
        data_path = os.path.join(data_dir, 'train.csv')
        trainer = HeartDiseaseTrainer(data_path)
        
        df = trainer.load_data()
        X, y = trainer.preprocess_data(df)
        
        assert X is not None
        assert y is not None
        assert len(X) == len(y)
        assert X.shape[1] == 13  # 13 features
    
    def test_feature_columns_stored(self, data_dir):
        """Test that feature columns are properly stored"""
        data_path = os.path.join(data_dir, 'train.csv')
        trainer = HeartDiseaseTrainer(data_path)
        
        df = trainer.load_data()
        X, y = trainer.preprocess_data(df)
        
        assert trainer.feature_columns is not None
        assert len(trainer.feature_columns) == 13
    
    def test_data_split(self, data_dir):
        """Test train/test split"""
        data_path = os.path.join(data_dir, 'train.csv')
        trainer = HeartDiseaseTrainer(data_path)
        
        df = trainer.load_data()
        X, y = trainer.preprocess_data(df)
        X_train, X_test, y_train, y_test = trainer.split_data(X, y)
        
        assert len(X_train) == len(y_train)
        assert len(X_test) == len(y_test)
        assert len(X_test) / len(X) == pytest.approx(0.2, abs=0.05)
    
    def test_scaler_creation(self, data_dir):
        """Test scaler creation"""
        data_path = os.path.join(data_dir, 'train.csv')
        trainer = HeartDiseaseTrainer(data_path)
        
        df = trainer.load_data()
        X, y = trainer.preprocess_data(df)
        X_train, X_test, y_train, y_test = trainer.split_data(X, y)
        X_train_scaled, X_test_scaled = trainer.scale_data(X_train, X_test)
        
        assert trainer.scaler is not None
        assert X_train_scaled.shape == X_train.shape
        assert X_test_scaled.shape == X_test.shape
    
    def test_model_training(self, data_dir):
        """Test model training"""
        data_path = os.path.join(data_dir, 'train.csv')
        trainer = HeartDiseaseTrainer(data_path)
        
        df = trainer.load_data()
        X, y = trainer.preprocess_data(df)
        X_train, X_test, y_train, y_test = trainer.split_data(X, y)
        X_train_scaled, X_test_scaled = trainer.scale_data(X_train, X_test)
        trainer.train_model(X_train_scaled, y_train)
        
        assert trainer.model is not None
        assert hasattr(trainer.model, 'predict')
    
    def test_model_prediction(self, data_dir):
        """Test model can make predictions"""
        data_path = os.path.join(data_dir, 'train.csv')
        trainer = HeartDiseaseTrainer(data_path)
        
        df = trainer.load_data()
        X, y = trainer.preprocess_data(df)
        X_train, X_test, y_train, y_test = trainer.split_data(X, y)
        X_train_scaled, X_test_scaled = trainer.scale_data(X_train, X_test)
        trainer.train_model(X_train_scaled, y_train)
        
        predictions = trainer.model.predict(X_test_scaled[:5])
        assert len(predictions) == 5
        assert all(pred in [0, 1] for pred in predictions)
    
    def test_label_encoder_creation(self, data_dir):
        """Test label encoder is created"""
        data_path = os.path.join(data_dir, 'train.csv')
        trainer = HeartDiseaseTrainer(data_path)
        
        df = trainer.load_data()
        X, y = trainer.preprocess_data(df)
        
        assert trainer.label_encoder is not None
        assert len(trainer.label_encoder.classes_) == 2


class TestTrainedModel:
    """Test cases for the trained model artifacts"""
    
    def test_model_exists(self, load_trained_model):
        """Test if model file exists"""
        assert load_trained_model is not None
    
    def test_scaler_exists(self, load_scaler):
        """Test if scaler file exists"""
        assert load_scaler is not None
    
    def test_label_encoder_exists(self, load_label_encoder):
        """Test if label encoder file exists"""
        assert load_label_encoder is not None
    
    def test_feature_columns_exist(self, load_feature_columns):
        """Test if feature columns file exists"""
        assert load_feature_columns is not None
        assert len(load_feature_columns) == 13
    
    def test_model_prediction_output(self, load_trained_model, load_scaler, 
                                     load_label_encoder, sample_patient_data):
        """Test model can make predictions with loaded artifacts"""
        if load_trained_model is None or load_scaler is None:
            pytest.skip("Model artifacts not found")
        
        # Prepare sample data
        input_data = np.array([[
            sample_patient_data['Age'],
            sample_patient_data['Sex'],
            sample_patient_data['Chest pain type'],
            sample_patient_data['BP'],
            sample_patient_data['Cholesterol'],
            sample_patient_data['FBS over 120'],
            sample_patient_data['EKG results'],
            sample_patient_data['Max HR'],
            sample_patient_data['Exercise angina'],
            sample_patient_data['ST depression'],
            sample_patient_data['Slope of ST'],
            sample_patient_data['Number of vessels fluro'],
            sample_patient_data['Thallium']
        ]])
        
        # Scale and predict
        input_scaled = load_scaler.transform(input_data)
        prediction = load_trained_model.predict(input_scaled)
        
        assert prediction is not None
        assert len(prediction) == 1
        assert prediction[0] in [0, 1]
