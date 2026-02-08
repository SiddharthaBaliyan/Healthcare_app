"""
Heart Disease Prediction Model Training Pipeline
This script trains a machine learning model for heart disease prediction
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import pickle
import logging
from datetime import datetime

# Setup logging
log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f'training_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class HeartDiseaseTrainer:
    def __init__(self, data_path):
        self.data_path = data_path
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.feature_columns = None
        
    def load_data(self):
        """Load and explore data"""
        logger.info(f"Loading data from {self.data_path}")
        df = pd.read_csv(self.data_path)
        logger.info(f"Original data shape: {df.shape}")
        
        # Sample data if too large (over 50,000 rows)
        if len(df) > 50000:
            logger.info(f"Large dataset detected ({len(df)} rows). Sampling 50,000 rows for efficient training...")
            df = df.sample(n=50000, random_state=42)
            logger.info(f"Sampled data shape: {df.shape}")
        
        logger.info(f"Columns: {df.columns.tolist()}")
        return df
    
    def preprocess_data(self, df):
        """Preprocess and clean data"""
        logger.info("Preprocessing data...")
        
        # Handle missing values
        df = df.dropna()
        logger.info(f"Data shape after dropping NaN: {df.shape}")
        
        # Separate features and target
        X = df.drop(['id', 'Heart Disease'], axis=1)
        y = df['Heart Disease']
        
        self.feature_columns = X.columns.tolist()
        
        # Encode target variable
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        
        logger.info(f"Target classes: {self.label_encoder.classes_}")
        logger.info(f"Target distribution:\n{pd.Series(y).value_counts()}")
        
        # Encode categorical features if any
        for col in X.columns:
            if X[col].dtype == 'object':
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col])
        
        return X, y_encoded
    
    def split_data(self, X, y, test_size=0.2, random_state=42):
        """Split data into train and test sets"""
        logger.info(f"Splitting data with test_size={test_size}")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        logger.info(f"Training set size: {X_train.shape}")
        logger.info(f"Test set size: {X_test.shape}")
        return X_train, X_test, y_train, y_test
    
    def scale_data(self, X_train, X_test):
        """Scale features"""
        logger.info("Scaling features...")
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        return X_train_scaled, X_test_scaled
    
    def train_model(self, X_train, y_train):
        """Train Random Forest model"""
        logger.info("Training Random Forest model...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train, y_train)
        logger.info("Model training completed")
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate model performance"""
        logger.info("Evaluating model...")
        y_pred = self.model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        logger.info(f"\n{'='*50}")
        logger.info("Model Performance Metrics:")
        logger.info(f"{'='*50}")
        logger.info(f"Accuracy:  {accuracy:.4f}")
        logger.info(f"Precision: {precision:.4f}")
        logger.info(f"Recall:    {recall:.4f}")
        logger.info(f"F1-Score:  {f1:.4f}")
        logger.info(f"{'='*50}")
        
        logger.info("\nConfusion Matrix:")
        cm = confusion_matrix(y_test, y_pred)
        logger.info(f"\n{cm}")
        
        logger.info("\nClassification Report:")
        logger.info(f"\n{classification_report(y_test, y_pred, target_names=self.label_encoder.classes_)}")
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }
    
    def save_model(self, model_dir):
        """Save model and preprocessing objects"""
        logger.info(f"Saving model to {model_dir}")
        os.makedirs(model_dir, exist_ok=True)
        
        # Save model
        model_path = os.path.join(model_dir, 'heart_disease_model.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        logger.info(f"Model saved to {model_path}")
        
        # Save scaler
        scaler_path = os.path.join(model_dir, 'scaler.pkl')
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        logger.info(f"Scaler saved to {scaler_path}")
        
        # Save label encoder
        encoder_path = os.path.join(model_dir, 'label_encoder.pkl')
        with open(encoder_path, 'wb') as f:
            pickle.dump(self.label_encoder, f)
        logger.info(f"Label encoder saved to {encoder_path}")
        
        # Save feature columns
        features_path = os.path.join(model_dir, 'feature_columns.pkl')
        with open(features_path, 'wb') as f:
            pickle.dump(self.feature_columns, f)
        logger.info(f"Feature columns saved to {features_path}")
    
    def run_pipeline(self):
        """Run complete training pipeline"""
        logger.info("="*60)
        logger.info("HEART DISEASE PREDICTION MODEL TRAINING PIPELINE")
        logger.info("="*60)
        
        # Load data
        df = self.load_data()
        
        # Preprocess
        X, y = self.preprocess_data(df)
        
        # Split
        X_train, X_test, y_train, y_test = self.split_data(X, y)
        
        # Scale
        X_train_scaled, X_test_scaled = self.scale_data(X_train, X_test)
        
        # Train
        self.train_model(X_train_scaled, y_train)
        
        # Evaluate
        metrics = self.evaluate_model(X_test_scaled, y_test)
        
        # Save
        model_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        self.save_model(model_dir)
        
        logger.info("="*60)
        logger.info("TRAINING PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("="*60)
        
        return metrics


def main():
    # Path to training data
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'train.csv')
    
    # Initialize trainer
    trainer = HeartDiseaseTrainer(data_path)
    
    # Run pipeline
    metrics = trainer.run_pipeline()


if __name__ == "__main__":
    main()
