"""
ML Model Training Script
Trains a Random Forest classifier for loan approval prediction
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib
import json
import os

# For demonstration, we'll create synthetic data
# In production, use real historical loan data
def create_sample_dataset(n_samples=1000):
    """Create synthetic loan dataset"""
    np.random.seed(42)
    
    data = {
        'ApplicantIncome': np.random.randint(2000, 15000, n_samples),
        'CoapplicantIncome': np.random.randint(0, 8000, n_samples),
        'LoanAmount': np.random.randint(50, 500, n_samples),
        'Loan_Amount_Term': np.random.choice([180, 240, 360, 480], n_samples),
        'Credit_History': np.random.choice([0, 1], n_samples, p=[0.15, 0.85]),
        'Property_Area': np.random.choice(['Urban', 'Semiurban', 'Rural'], n_samples),
        'Self_Employed': np.random.choice([0, 1], n_samples, p=[0.85, 0.15]),
        'Dependents': np.random.choice([0, 1, 2, 3], n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Create target variable based on logical rules
    # Good credit history and reasonable loan amount increase approval chances
    df['Loan_Status'] = 0
    
    conditions = (
        (df['Credit_History'] == 1) &
        (df['LoanAmount'] < (df['ApplicantIncome'] + df['CoapplicantIncome']) * 0.3) &
        (df['ApplicantIncome'] > 3000)
    )
    
    df.loc[conditions, 'Loan_Status'] = 1
    
    # Add some noise
    noise_indices = np.random.choice(df.index, size=int(0.1 * n_samples), replace=False)
    df.loc[noise_indices, 'Loan_Status'] = 1 - df.loc[noise_indices, 'Loan_Status']
    
    return df


def train_model():
    """Train and save the ML model"""
    
    print("Creating dataset...")
    df = create_sample_dataset(1000)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Approval rate: {df['Loan_Status'].mean():.2%}")
    
    # Feature engineering
    df['Total_Income'] = df['ApplicantIncome'] + df['CoapplicantIncome']
    df['Loan_to_Income'] = df['LoanAmount'] / df['Total_Income']
    df['Monthly_Payment'] = df['LoanAmount'] / (df['Loan_Amount_Term'] / 12)
    df['DTI_Ratio'] = (df['Monthly_Payment'] / (df['Total_Income'] / 12)) * 100
    
    # Prepare features
    feature_cols = [
        'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
        'Loan_Amount_Term', 'Credit_History', 'Self_Employed',
        'Dependents', 'Total_Income', 'Loan_to_Income', 'DTI_Ratio'
    ]
    
    X = df[feature_cols].copy()
    
    # Encode Property_Area
    le = LabelEncoder()
    df['Property_Area_Encoded'] = le.fit_transform(df['Property_Area'])
    X['Property_Area'] = df['Property_Area_Encoded']
    
    y = df['Loan_Status']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("\nTraining Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"\nTrain Accuracy: {train_score:.3f}")
    print(f"Test Accuracy: {test_score:.3f}")
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    print(f"Cross-validation scores: {cv_scores}")
    print(f"Mean CV score: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
    
    # Predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Reject', 'Approve']))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    print(f"\nROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.3f}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 5 Feature Importances:")
    print(feature_importance.head())
    
    # Save model and metadata
    print("\nSaving model...")
    os.makedirs('../backend/models', exist_ok=True)
    joblib.dump(model, '../backend/models/loan_model.pkl')
    joblib.dump(le, '../backend/models/label_encoder.pkl')
    
    # Save feature importance
    feature_importance.to_csv('../backend/models/feature_importance.csv', index=False)
    
    # Save model metadata
    metadata = {
        'model_type': 'RandomForestClassifier',
        'n_estimators': 100,
        'train_accuracy': float(train_score),
        'test_accuracy': float(test_score),
        'cv_mean': float(cv_scores.mean()),
        'cv_std': float(cv_scores.std()),
        'roc_auc': float(roc_auc_score(y_test, y_pred_proba)),
        'features': list(X.columns),
        'training_date': pd.Timestamp.now().isoformat()
    }
    
    with open('../backend/models/model_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n✅ Model training complete!")
    print("Saved files:")
    print("  - backend/models/loan_model.pkl")
    print("  - backend/models/label_encoder.pkl")
    print("  - backend/models/feature_importance.csv")
    print("  - backend/models/model_metadata.json")
    
    return model, X.columns, feature_importance


if __name__ == "__main__":
    model, features, importance = train_model()
