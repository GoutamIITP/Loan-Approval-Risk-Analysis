"""
Main Flask Application
Integrates all components: validation, rules, ML, explainability, audit
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import time
import uuid
from datetime import datetime
import os

# Import our modules
from data_validator import LoanDataValidator
from risk_rules import RiskRuleEngine
from explainer import LoanExplainer
from audit_logger import AuditLogger

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Load ML model and components
print("Loading ML model...")
try:
    model = joblib.load('models/loan_model.pkl')
    label_encoder = joblib.load('models/label_encoder.pkl')
    feature_importance = pd.read_csv('models/feature_importance.csv')
    
    # Initialize components
    explainer = LoanExplainer(feature_importance)
    ml_available = True
    print("✅ ML model loaded successfully!")
except Exception as e:
    print(f"⚠️  ML model not found: {e}")
    print("⚠️  System will run in rule-based mode only")
    explainer = None
    ml_available = False

audit_logger = AuditLogger('logs/audit.db')

print("✅ Application initialized successfully!")


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'ml_available': ml_available
    })


@app.route('/api/assess-loan', methods=['POST'])
def assess_loan():
    """
    Main endpoint for loan risk assessment
    Integrates: Validation → Rules → ML → Explainability → Audit
    """
    start_time = time.time()
    
    try:
        # Get request data
        data = request.json
        application_id = data.get('application_id', f"APP-{uuid.uuid4().hex[:8].upper()}")
        
        # STEP 1: Data Validation
        is_valid, errors, warnings = LoanDataValidator.validate(data)
        
        if not is_valid:
            # Log failed validation
            audit_logger.log_decision({
                'application_id': application_id,
                'applicant_data': data,
                'validation_result': {
                    'is_valid': False,
                    'errors': errors,
                    'warnings': warnings
                },
                'final_decision': 'REJECTED',
                'final_risk_level': 'HIGH',
                'decision_reason': 'Failed data validation',
                'processing_time_ms': int((time.time() - start_time) * 1000),
                'metadata': {
                    'user_agent': request.headers.get('User-Agent'),
                    'ip_address': request.remote_addr
                }
            })
            
            return jsonify({
                'success': False,
                'application_id': application_id,
                'decision': 'REJECTED',
                'reason': 'Data validation failed',
                'errors': errors,
                'warnings': warnings
            }), 400
        
        # STEP 2: Rule-Based Risk Assessment
        rule_result = RiskRuleEngine.evaluate(data)
        
        # If rules suggest rejection, stop here
        if rule_result['recommendation'] == 'REJECT':
            processing_time = int((time.time() - start_time) * 1000)
            
            audit_logger.log_decision({
                'application_id': application_id,
                'applicant_data': data,
                'validation_result': {
                    'is_valid': True,
                    'errors': [],
                    'warnings': warnings
                },
                'rule_result': rule_result,
                'final_decision': 'REJECTED',
                'final_risk_level': rule_result['risk_level'],
                'decision_reason': f"Rule-based rejection: {rule_result['risk_score']} risk score",
                'processing_time_ms': processing_time
            })
            
            return jsonify({
                'success': True,
                'application_id': application_id,
                'decision': 'REJECTED',
                'risk_level': rule_result['risk_level'],
                'risk_score': rule_result['risk_score'],
                'reason': 'High risk based on business rules',
                'flags': rule_result['flags'],
                'warnings': warnings,
                'processing_time_ms': processing_time
            })
        
        # STEP 3: ML Model Prediction (if available)
        if ml_available:
            ml_features = prepare_features_for_ml(data)
            ml_probability = model.predict_proba(ml_features)[0][1]
            ml_prediction = 'APPROVE' if ml_probability >= 0.5 else 'REJECT'
            
            ml_result = {
                'probability': float(ml_probability),
                'prediction': ml_prediction
            }
            
            # STEP 4: Generate Explanation
            explanation = explainer.explain_prediction(
                prepare_feature_dict(data),
                ml_probability,
                model
            )
        else:
            # No ML available - use rule-based only
            ml_result = {'probability': None, 'prediction': None}
            explanation = {
                'overall_assessment': 'Rule-based assessment only (ML not available)',
                'ml_confidence': 'N/A',
                'key_factors': [],
                'top_features': []
            }
        
        # STEP 5: Make Final Decision
        final_decision, final_risk_level, decision_reason = make_final_decision(
            rule_result,
            ml_result,
            warnings
        )
        
        # STEP 6: Log to Audit Trail
        processing_time = int((time.time() - start_time) * 1000)
        
        audit_logger.log_decision({
            'application_id': application_id,
            'applicant_data': data,
            'validation_result': {
                'is_valid': True,
                'errors': [],
                'warnings': warnings
            },
            'rule_result': rule_result,
            'ml_result': ml_result,
            'final_decision': final_decision,
            'final_risk_level': final_risk_level,
            'decision_reason': decision_reason,
            'processing_time_ms': processing_time,
            'metadata': {
                'user_agent': request.headers.get('User-Agent'),
                'ip_address': request.remote_addr
            }
        })
        
        # STEP 7: Return Response
        return jsonify({
            'success': True,
            'application_id': application_id,
            'decision': final_decision,
            'risk_level': final_risk_level,
            'risk_score': rule_result['risk_score'],
            'reason': decision_reason,
            'ml_confidence': f"{ml_result['probability']:.1%}" if ml_result['probability'] else 'N/A',
            'explanation': explanation,
            'rule_flags': rule_result['flags'],
            'warnings': warnings,
            'processing_time_ms': processing_time,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def prepare_features_for_ml(data):
    """Prepare features for ML model"""
    # Calculate derived features
    total_income = float(data.get('applicant_income', 0)) + float(data.get('coapplicant_income', 0))
    loan_amount = float(data.get('loan_amount', 0))
    loan_term = float(data.get('loan_amount_term', 360))
    
    features = {
        'ApplicantIncome': float(data.get('applicant_income', 0)),
        'CoapplicantIncome': float(data.get('coapplicant_income', 0)),
        'LoanAmount': loan_amount,
        'Loan_Amount_Term': loan_term,
        'Credit_History': int(data.get('credit_history', 0)),
        'Self_Employed': int(data.get('self_employed', 0)),
        'Dependents': int(data.get('dependents', 0)),
        'Total_Income': total_income,
        'Loan_to_Income': loan_amount / total_income if total_income > 0 else 0,
        'Monthly_Payment': (loan_amount * 1000) / loan_term if loan_term > 0 else 0
    }
    
    # DTI Ratio
    monthly_income = total_income / 12 if total_income > 0 else 0
    features['DTI_Ratio'] = (features['Monthly_Payment'] / monthly_income * 100) if monthly_income > 0 else 0
    
    # Encode property area
    property_area_map = {'Urban': 2, 'Semiurban': 1, 'Rural': 0}
    features['Property_Area'] = property_area_map.get(data.get('property_area', 'Urban'), 2)
    
    # Create DataFrame
    feature_order = [
        'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
        'Loan_Amount_Term', 'Credit_History', 'Self_Employed',
        'Dependents', 'Total_Income', 'Loan_to_Income', 'DTI_Ratio',
        'Property_Area'
    ]
    
    return pd.DataFrame([features])[feature_order]


def prepare_feature_dict(data):
    """Prepare feature dictionary for explainer"""
    total_income = float(data.get('applicant_income', 0)) + float(data.get('coapplicant_income', 0))
    loan_amount = float(data.get('loan_amount', 0))
    
    return {
        'Credit_History': int(data.get('credit_history', 0)),
        'Total_Income': total_income,
        'Loan_to_Income': loan_amount / total_income if total_income > 0 else 0,
        'DTI_Ratio': calculate_dti(data),
        'LoanAmount': loan_amount
    }


def calculate_dti(data):
    """Calculate DTI ratio"""
    total_income = float(data.get('applicant_income', 0)) + float(data.get('coapplicant_income', 0))
    loan_amount = float(data.get('loan_amount', 0))
    loan_term = float(data.get('loan_amount_term', 360))
    
    monthly_payment = (loan_amount * 1000) / loan_term
    monthly_income = total_income / 12
    
    return (monthly_payment / monthly_income * 100) if monthly_income > 0 else 0


def make_final_decision(rule_result, ml_result, warnings):
    """
    Make final decision combining rules and ML
    Priority: Rules > ML (rules can override ML)
    """
    rule_recommendation = rule_result['recommendation']
    ml_prediction = ml_result.get('prediction')
    ml_probability = ml_result.get('probability')
    
    # High confidence scenarios
    if rule_recommendation == 'REJECT':
        return 'REJECTED', 'HIGH', 'Rule-based rejection due to critical risk factors'
    
    if rule_recommendation == 'MANUAL_REVIEW':
        return 'MANUAL_REVIEW', rule_result['risk_level'], 'Medium/High risk requires human review'
    
    # Proceed to ML (if available)
    if rule_recommendation == 'PROCEED_TO_ML':
        if ml_prediction and ml_probability:
            if ml_prediction == 'APPROVE' and ml_probability >= 0.7:
                return 'APPROVED', 'LOW', f'Strong approval indicators (ML confidence: {ml_probability:.1%})'
            elif ml_prediction == 'APPROVE' and ml_probability >= 0.5:
                return 'MANUAL_REVIEW', 'MEDIUM', f'Moderate approval indicators (ML confidence: {ml_probability:.1%})'
            else:
                return 'REJECTED', 'MEDIUM', f'Insufficient approval indicators (ML confidence: {ml_probability:.1%})'
        else:
            # No ML available - approve low risk cases
            return 'APPROVED', 'LOW', 'Low risk based on business rules'
    
    # Default
    return 'MANUAL_REVIEW', 'MEDIUM', 'Unable to make automated decision'


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get audit statistics"""
    stats = audit_logger.get_statistics()
    return jsonify(stats)


@app.route('/api/recent-decisions', methods=['GET'])
def get_recent_decisions():
    """Get recent decisions"""
    limit = request.args.get('limit', 100, type=int)
    decisions = audit_logger.get_recent_decisions(limit)
    
    return jsonify({
        'count': len(decisions),
        'decisions': [
            {
                'application_id': d[0],
                'timestamp': d[1],
                'decision': d[2],
                'risk_level': d[3]
            }
            for d in decisions
        ]
    })


if __name__ == '__main__':
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    print("\n" + "="*50)
    print("🏦 FinCrime Loan Risk Assessment API")
    print("="*50)
    print("Starting server on http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
