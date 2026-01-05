"""
Model Explainability Module
Provides human-readable explanations for ML predictions
"""

import pandas as pd
import numpy as np

class LoanExplainer:
    
    def __init__(self, feature_importance):
        """
        Initialize explainer with feature importance
        feature_importance: DataFrame with 'feature' and 'importance' columns
        """
        self.feature_importance = feature_importance.set_index('feature')['importance'].to_dict()
    
    def explain_prediction(self, input_data, ml_probability, model):
        """
        Generate human-readable explanation for a prediction
        """
        explanations = []
        
        # Calculate feature contributions
        feature_values = []
        for feature in input_data.keys():
            if feature in self.feature_importance:
                importance = self.feature_importance[feature]
                value = input_data[feature]
                feature_values.append({
                    'feature': feature,
                    'value': value,
                    'importance': importance,
                    'contribution': importance * 100  # Simplified contribution
                })
        
        # Sort by importance
        feature_values.sort(key=lambda x: x['importance'], reverse=True)
        
        # Generate explanations for top features
        top_features = feature_values[:5]
        
        for fv in top_features:
            feature = fv['feature']
            value = fv['value']
            importance = fv['importance']
            
            explanation = self._generate_feature_explanation(feature, value, importance)
            if explanation:
                explanations.append(explanation)
        
        # Overall assessment
        if ml_probability >= 0.7:
            overall = "✅ Strong indicators for approval"
        elif ml_probability >= 0.5:
            overall = "⚠️ Moderate indicators, requires review"
        else:
            overall = "❌ Weak indicators for approval"
        
        return {
            'overall_assessment': overall,
            'ml_confidence': f"{ml_probability:.1%}",
            'key_factors': explanations,
            'top_features': top_features[:3]
        }
    
    def _generate_feature_explanation(self, feature, value, importance):
        """Generate explanation for specific feature"""
        
        if feature == 'Credit_History':
            if value == 1:
                return {
                    'factor': 'Credit History',
                    'impact': 'POSITIVE',
                    'weight': f"{importance:.1%}",
                    'explanation': 'Applicant has good credit history (strong positive factor)'
                }
            else:
                return {
                    'factor': 'Credit History',
                    'impact': 'NEGATIVE',
                    'weight': f"{importance:.1%}",
                    'explanation': 'No credit history (major risk factor)'
                }
        
        elif feature == 'Total_Income':
            if value >= 8000:
                impact = 'POSITIVE'
                explanation = f'High total income (₹{value:,.0f}) supports repayment capacity'
            elif value >= 4000:
                impact = 'NEUTRAL'
                explanation = f'Moderate income (₹{value:,.0f})'
            else:
                impact = 'NEGATIVE'
                explanation = f'Low income (₹{value:,.0f}) may impact repayment'
            
            return {
                'factor': 'Total Income',
                'impact': impact,
                'weight': f"{importance:.1%}",
                'explanation': explanation
            }
        
        elif feature == 'Loan_to_Income':
            if value > 0.3:
                impact = 'NEGATIVE'
                explanation = f'High loan-to-income ratio ({value:.1%}) indicates potential stress'
            elif value > 0.2:
                impact = 'NEUTRAL'
                explanation = f'Moderate loan-to-income ratio ({value:.1%})'
            else:
                impact = 'POSITIVE'
                explanation = f'Low loan-to-income ratio ({value:.1%}) is favorable'
            
            return {
                'factor': 'Loan-to-Income Ratio',
                'impact': impact,
                'weight': f"{importance:.1%}",
                'explanation': explanation
            }
        
        elif feature == 'DTI_Ratio':
            if value > 43:
                impact = 'NEGATIVE'
                explanation = f'DTI ratio ({value:.1f}%) exceeds standard threshold (43%)'
            elif value > 36:
                impact = 'NEUTRAL'
                explanation = f'DTI ratio ({value:.1f}%) is moderate'
            else:
                impact = 'POSITIVE'
                explanation = f'Low DTI ratio ({value:.1f}%) indicates good debt management'
            
            return {
                'factor': 'Debt-to-Income Ratio',
                'impact': impact,
                'weight': f"{importance:.1%}",
                'explanation': explanation
            }
        
        elif feature == 'LoanAmount':
            if value > 300:
                impact = 'NEGATIVE'
                explanation = f'High loan amount (₹{value:,.0f}K) requires strong financials'
            elif value > 150:
                impact = 'NEUTRAL'
                explanation = f'Moderate loan amount (₹{value:,.0f}K)'
            else:
                impact = 'POSITIVE'
                explanation = f'Manageable loan amount (₹{value:,.0f}K)'
            
            return {
                'factor': 'Loan Amount',
                'impact': impact,
                'weight': f"{importance:.1%}",
                'explanation': explanation
            }
        
        return None


def test_explainer():
    """Test explainer"""
    
    # Mock feature importance
    importance_df = pd.DataFrame({
        'feature': ['Credit_History', 'Total_Income', 'Loan_to_Income', 'DTI_Ratio', 'LoanAmount'],
        'importance': [0.35, 0.25, 0.15, 0.15, 0.10]
    })
    
    explainer = LoanExplainer(importance_df)
    
    # Test data
    test_input = {
        'Credit_History': 1,
        'Total_Income': 7500,
        'Loan_to_Income': 0.2,
        'DTI_Ratio': 35.0,
        'LoanAmount': 150
    }
    
    explanation = explainer.explain_prediction(test_input, 0.75, None)
    
    print("Explanation Test:")
    print("="*50)
    print(f"Overall: {explanation['overall_assessment']}")
    print(f"ML Confidence: {explanation['ml_confidence']}")
    print("\nKey Factors:")
    for factor in explanation['key_factors']:
        print(f"  [{factor['impact']}] {factor['factor']} (Weight: {factor['weight']})")
        print(f"      {factor['explanation']}")


if __name__ == "__main__":
    test_explainer()
