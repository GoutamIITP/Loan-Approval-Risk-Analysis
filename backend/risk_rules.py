"""
Rule-Based Risk Engine
Implements compliance and business rules for loan assessment
"""

class RiskRuleEngine:
    
    # Risk thresholds
    HIGH_LOAN_THRESHOLD = 5000
    LOW_INCOME_THRESHOLD = 2500
    HIGH_DTI_THRESHOLD = 43  # Debt-to-income %
    
    @staticmethod
    def evaluate(data):
        """
        Evaluate loan application against business rules
        Returns: (risk_level, flags, score)
        """
        flags = []
        risk_score = 0  # 0-100 scale
        
        # Rule 1: Credit History Check (Most Important)
        if int(data.get('credit_history', 1)) == 0:
            flags.append({
                'rule': 'R1: No Credit History',
                'severity': 'HIGH',
                'impact': +40,
                'description': 'Applicant has no credit history'
            })
            risk_score += 40
        
        # Rule 2: Income vs Loan Amount
        income = float(data.get('applicant_income', 0))
        coapplicant_income = float(data.get('coapplicant_income', 0))
        total_income = income + coapplicant_income
        loan_amount = float(data.get('loan_amount', 0))
        
        if loan_amount > total_income * 3:
            flags.append({
                'rule': 'R2: High Loan-to-Income Ratio',
                'severity': 'HIGH',
                'impact': +25,
                'description': f'Loan amount ({loan_amount}) exceeds 3x total income ({total_income})'
            })
            risk_score += 25
        elif loan_amount > total_income * 2:
            flags.append({
                'rule': 'R2: Moderate Loan-to-Income Ratio',
                'severity': 'MEDIUM',
                'impact': +15,
                'description': f'Loan amount is 2-3x total income'
            })
            risk_score += 15
        
        # Rule 3: Debt-to-Income Ratio
        loan_term = float(data.get('loan_amount_term', 360))
        monthly_payment = (loan_amount * 1000) / loan_term  # Convert to monthly
        monthly_income = total_income / 12
        
        if monthly_income > 0:
            dti_ratio = (monthly_payment / monthly_income) * 100
            
            if dti_ratio > 50:
                flags.append({
                    'rule': 'R3: Very High DTI Ratio',
                    'severity': 'HIGH',
                    'impact': +20,
                    'description': f'DTI ratio is {dti_ratio:.1f}% (>50% critical threshold)'
                })
                risk_score += 20
            elif dti_ratio > 43:
                flags.append({
                    'rule': 'R3: High DTI Ratio',
                    'severity': 'MEDIUM',
                    'impact': +10,
                    'description': f'DTI ratio is {dti_ratio:.1f}% (>43% threshold)'
                })
                risk_score += 10
        
        # Rule 4: Low Income Check
        if total_income < RiskRuleEngine.LOW_INCOME_THRESHOLD:
            flags.append({
                'rule': 'R4: Low Income',
                'severity': 'MEDIUM',
                'impact': +15,
                'description': f'Total income ({total_income}) below threshold ({RiskRuleEngine.LOW_INCOME_THRESHOLD})'
            })
            risk_score += 15
        
        # Rule 5: Property Area Risk
        property_area = data.get('property_area', 'Urban')
        if property_area == 'Rural':
            flags.append({
                'rule': 'R5: Rural Property',
                'severity': 'LOW',
                'impact': +5,
                'description': 'Rural properties have slightly higher risk'
            })
            risk_score += 5
        
        # Rule 6: Self-Employed Risk
        if int(data.get('self_employed', 0)) == 1:
            flags.append({
                'rule': 'R6: Self-Employed',
                'severity': 'LOW',
                'impact': +5,
                'description': 'Self-employed applicants require additional verification'
            })
            risk_score += 5
        
        # Rule 7: Dependents Risk
        dependents = int(data.get('dependents', 0))
        if dependents > 3:
            flags.append({
                'rule': 'R7: High Dependents',
                'severity': 'LOW',
                'impact': +5,
                'description': f'{dependents} dependents may impact repayment capacity'
            })
            risk_score += 5
        
        # Determine overall risk level
        if risk_score >= 50:
            risk_level = 'HIGH'
        elif risk_score >= 25:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        return {
            'risk_level': risk_level,
            'risk_score': min(risk_score, 100),  # Cap at 100
            'flags': flags,
            'total_flags': len(flags),
            'recommendation': RiskRuleEngine._get_recommendation(risk_level, risk_score)
        }
    
    @staticmethod
    def _get_recommendation(risk_level, risk_score):
        """Generate recommendation based on risk assessment"""
        if risk_level == 'HIGH':
            return 'REJECT' if risk_score > 65 else 'MANUAL_REVIEW'
        elif risk_level == 'MEDIUM':
            return 'MANUAL_REVIEW'
        else:
            return 'PROCEED_TO_ML'


def test_risk_engine():
    """Test risk engine"""
    
    # Test case 1: High risk - no credit history
    test_data_1 = {
        'applicant_income': 3000,
        'coapplicant_income': 0,
        'loan_amount': 200,
        'loan_amount_term': 360,
        'credit_history': 0,
        'property_area': 'Rural',
        'self_employed': 1,
        'dependents': 2
    }
    
    print("Test Case 1: High Risk Application")
    print("="*50)
    result = RiskRuleEngine.evaluate(test_data_1)
    print(f"Risk Level: {result['risk_level']}")
    print(f"Risk Score: {result['risk_score']}/100")
    print(f"Recommendation: {result['recommendation']}")
    print(f"\nFlags ({result['total_flags']}):")
    for flag in result['flags']:
        print(f"  [{flag['severity']}] {flag['rule']}: {flag['description']}")
    
    print("\n" + "="*50 + "\n")
    
    # Test case 2: Low risk application
    test_data_2 = {
        'applicant_income': 8000,
        'coapplicant_income': 2000,
        'loan_amount': 150,
        'loan_amount_term': 360,
        'credit_history': 1,
        'property_area': 'Urban',
        'self_employed': 0,
        'dependents': 1
    }
    
    print("Test Case 2: Low Risk Application")
    print("="*50)
    result = RiskRuleEngine.evaluate(test_data_2)
    print(f"Risk Level: {result['risk_level']}")
    print(f"Risk Score: {result['risk_score']}/100")
    print(f"Recommendation: {result['recommendation']}")
    print(f"\nFlags ({result['total_flags']}):")
    for flag in result['flags']:
        print(f"  [{flag['severity']}] {flag['rule']}: {flag['description']}")


if __name__ == "__main__":
    test_risk_engine()
