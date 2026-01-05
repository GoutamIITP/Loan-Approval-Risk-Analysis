"""
Test script for FinCrime Loan Risk System
"""

import requests
import json

API_URL = "http://localhost:5000/api"

# Test data
test_cases = [
    {
        "name": "Low Risk Application",
        "data": {
            "applicant_income": 8000,
            "coapplicant_income": 2000,
            "loan_amount": 150,
            "loan_amount_term": 360,
            "credit_history": 1,
            "property_area": "Urban",
            "self_employed": 0,
            "dependents": 1
        }
    },
    {
        "name": "High Risk Application",
        "data": {
            "applicant_income": 3000,
            "coapplicant_income": 0,
            "loan_amount": 250,
            "loan_amount_term": 360,
            "credit_history": 0,
            "property_area": "Rural",
            "self_employed": 1,
            "dependents": 3
        }
    },
    {
        "name": "Medium Risk Application",
        "data": {
            "applicant_income": 5000,
            "coapplicant_income": 1500,
            "loan_amount": 180,
            "loan_amount_term": 360,
            "credit_history": 1,
            "property_area": "Semiurban",
            "self_employed": 0,
            "dependents": 2
        }
    }
]

print("🧪 Testing FinCrime Loan Risk System")
print("=" * 50)

for i, test_case in enumerate(test_cases, 1):
    print(f"\nTest {i}: {test_case['name']}")
    print("-" * 50)
    
    try:
        response = requests.post(
            f"{API_URL}/assess-loan",
            json=test_case['data'],
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Decision: {result['decision']}")
            print(f"   Risk Level: {result['risk_level']}")
            print(f"   Risk Score: {result['risk_score']}/100")
            print(f"   Reason: {result['reason']}")
            print(f"   Processing Time: {result['processing_time_ms']}ms")
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "=" * 50)
print("✅ Testing complete!")
