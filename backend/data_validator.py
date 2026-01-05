"""
Data Validation Module
Validates incoming loan application data before processing
"""

class LoanDataValidator:
    
    REQUIRED_FIELDS = [
        'applicant_income',
        'loan_amount',
        'loan_amount_term',
        'credit_history',
        'property_area'
    ]
    
    VALID_PROPERTY_AREAS = ['Urban', 'Semiurban', 'Rural']
    
    @staticmethod
    def validate(data):
        """
        Validates loan application data
        Returns: (is_valid, errors, warnings)
        """
        errors = []
        warnings = []
        
        # 1. Check missing fields
        for field in LoanDataValidator.REQUIRED_FIELDS:
            if field not in data or data[field] is None or data[field] == '':
                errors.append(f"Missing required field: {field}")
        
        if errors:
            return False, errors, warnings
        
        # 2. Validate credit history
        if data['credit_history'] not in [0, 1, '0', '1']:
            errors.append("Credit history must be 0 or 1")
        elif int(data['credit_history']) == 0:
            warnings.append("No credit history - HIGH RISK indicator")
        
        # 3. Validate income
        try:
            income = float(data['applicant_income'])
            if income < 0:
                errors.append("Income cannot be negative")
            elif income < 1000:
                warnings.append("Very low income - potential risk")
            elif income > 1000000:
                warnings.append("Extremely high income - verify data accuracy")
        except ValueError:
            errors.append("Income must be a valid number")
        
        # 4. Validate loan amount
        try:
            loan_amount = float(data['loan_amount'])
            if loan_amount <= 0:
                errors.append("Loan amount must be positive")
            elif loan_amount > 10000:
                warnings.append("Very high loan amount - requires review")
        except ValueError:
            errors.append("Loan amount must be a valid number")
        
        # 5. Validate loan term
        try:
            term = float(data['loan_amount_term'])
            if term <= 0:
                errors.append("Loan term must be positive")
            elif term > 480:  # 40 years
                warnings.append("Unusually long loan term")
        except ValueError:
            errors.append("Loan term must be a valid number")
        
        # 6. Validate property area
        if data['property_area'] not in LoanDataValidator.VALID_PROPERTY_AREAS:
            errors.append(f"Property area must be one of: {LoanDataValidator.VALID_PROPERTY_AREAS}")
        
        # 7. Debt-to-Income ratio check
        try:
            income = float(data['applicant_income'])
            loan = float(data['loan_amount'])
            monthly_payment = loan / float(data['loan_amount_term'])
            dti_ratio = (monthly_payment / (income / 12)) * 100
            
            if dti_ratio > 43:
                warnings.append(f"High debt-to-income ratio: {dti_ratio:.1f}% (>43% threshold)")
        except:
            pass
        
        is_valid = len(errors) == 0
        return is_valid, errors, warnings


def test_validator():
    """Test the validator"""
    
    # Test case 1: Valid data
    valid_data = {
        'applicant_income': 5000,
        'loan_amount': 150,
        'loan_amount_term': 360,
        'credit_history': 1,
        'property_area': 'Urban'
    }
    print("Test 1 - Valid data:")
    print(LoanDataValidator.validate(valid_data))
    
    # Test case 2: Missing credit history
    invalid_data = {
        'applicant_income': 5000,
        'loan_amount': 150,
        'loan_amount_term': 360,
        'property_area': 'Urban'
    }
    print("\nTest 2 - Missing field:")
    print(LoanDataValidator.validate(invalid_data))
    
    # Test case 3: No credit history
    risky_data = {
        'applicant_income': 5000,
        'loan_amount': 150,
        'loan_amount_term': 360,
        'credit_history': 0,
        'property_area': 'Urban'
    }
    print("\nTest 3 - No credit history:")
    print(LoanDataValidator.validate(risky_data))


if __name__ == "__main__":
    test_validator()
