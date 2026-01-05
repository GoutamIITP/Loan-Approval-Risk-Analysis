"""
Audit Logging System
Stores all loan decisions for compliance and auditing
"""

import sqlite3
import json
from datetime import datetime
import os

class AuditLogger:
    
    def __init__(self, db_path='logs/audit.db'):
        """Initialize audit logger with database path"""
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self):
        """Create audit table if it doesn't exist"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                applicant_data TEXT NOT NULL,
                validation_status TEXT,
                validation_errors TEXT,
                validation_warnings TEXT,
                rule_risk_level TEXT,
                rule_risk_score INTEGER,
                rule_flags TEXT,
                ml_probability REAL,
                ml_prediction TEXT,
                final_decision TEXT NOT NULL,
                final_risk_level TEXT NOT NULL,
                decision_reason TEXT,
                processing_time_ms INTEGER,
                user_agent TEXT,
                ip_address TEXT
            )
        ''')
        
        # Create index on application_id for fast lookups
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_application_id 
            ON audit_log(application_id)
        ''')
        
        # Create index on timestamp for time-based queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON audit_log(timestamp)
        ''')
        
        conn.commit()
        conn.close()
    
    def log_decision(self, decision_data):
        """
        Log a loan decision to the audit trail
        
        decision_data should contain:
        - application_id
        - applicant_data
        - validation_result
        - rule_result
        - ml_result
        - final_decision
        - processing_time_ms
        - metadata (optional)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Extract data
        validation = decision_data.get('validation_result', {})
        rule = decision_data.get('rule_result', {})
        ml = decision_data.get('ml_result', {})
        metadata = decision_data.get('metadata', {})
        
        cursor.execute('''
            INSERT INTO audit_log (
                application_id, timestamp, applicant_data,
                validation_status, validation_errors, validation_warnings,
                rule_risk_level, rule_risk_score, rule_flags,
                ml_probability, ml_prediction,
                final_decision, final_risk_level, decision_reason,
                processing_time_ms, user_agent, ip_address
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            decision_data.get('application_id', 'N/A'),
            datetime.utcnow().isoformat(),
            json.dumps(decision_data.get('applicant_data', {})),
            'VALID' if validation.get('is_valid') else 'INVALID',
            json.dumps(validation.get('errors', [])),
            json.dumps(validation.get('warnings', [])),
            rule.get('risk_level'),
            rule.get('risk_score'),
            json.dumps(rule.get('flags', [])),
            ml.get('probability'),
            ml.get('prediction'),
            decision_data.get('final_decision'),
            decision_data.get('final_risk_level'),
            decision_data.get('decision_reason'),
            decision_data.get('processing_time_ms'),
            metadata.get('user_agent'),
            metadata.get('ip_address')
        ))
        
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        
        return record_id
    
    def get_application_history(self, application_id):
        """Retrieve audit history for a specific application"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM audit_log 
            WHERE application_id = ? 
            ORDER BY timestamp DESC
        ''', (application_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return rows
    
    def get_recent_decisions(self, limit=100):
        """Get recent decisions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT application_id, timestamp, final_decision, final_risk_level
            FROM audit_log 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return rows
    
    def get_statistics(self):
        """Get decision statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                COUNT(*) as total_applications,
                SUM(CASE WHEN final_decision = 'APPROVED' THEN 1 ELSE 0 END) as approved,
                SUM(CASE WHEN final_decision = 'REJECTED' THEN 1 ELSE 0 END) as rejected,
                SUM(CASE WHEN final_decision = 'MANUAL_REVIEW' THEN 1 ELSE 0 END) as manual_review,
                AVG(processing_time_ms) as avg_processing_time,
                SUM(CASE WHEN final_risk_level = 'HIGH' THEN 1 ELSE 0 END) as high_risk_count,
                SUM(CASE WHEN final_risk_level = 'MEDIUM' THEN 1 ELSE 0 END) as medium_risk_count,
                SUM(CASE WHEN final_risk_level = 'LOW' THEN 1 ELSE 0 END) as low_risk_count
            FROM audit_log
        '''
        
        cursor.execute(query)
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'total_applications': row[0],
                'approved': row[1],
                'rejected': row[2],
                'manual_review': row[3],
                'avg_processing_time_ms': row[4],
                'high_risk': row[5],
                'medium_risk': row[6],
                'low_risk': row[7],
                'approval_rate': f"{(row[1]/row[0]*100) if row[0] > 0 else 0:.1f}%"
            }
        
        return None


def test_audit_logger():
    """Test audit logger"""
    
    # Create test database
    logger = AuditLogger('test_audit.db')
    
    # Test logging
    test_decision = {
        'application_id': 'APP123456',
        'applicant_data': {
            'name': 'John Doe',
            'income': 5000,
            'loan_amount': 150
        },
        'validation_result': {
            'is_valid': True,
            'errors': [],
            'warnings': ['Low income warning']
        },
        'rule_result': {
            'risk_level': 'MEDIUM',
            'risk_score': 35,
            'flags': []
        },
        'ml_result': {
            'probability': 0.72,
            'prediction': 'APPROVE'
        },
        'final_decision': 'MANUAL_REVIEW',
        'final_risk_level': 'MEDIUM',
        'decision_reason': 'Medium risk requires human review',
        'processing_time_ms': 145,
        'metadata': {
            'user_agent': 'Test Client',
            'ip_address': '127.0.0.1'
        }
    }
    
    record_id = logger.log_decision(test_decision)
    print(f"✅ Logged decision with ID: {record_id}")
    
    # Test retrieval
    history = logger.get_application_history('APP123456')
    print(f"\n✅ Retrieved {len(history)} record(s)")
    
    # Test statistics
    stats = logger.get_statistics()
    print(f"\n✅ Statistics:")
    print(json.dumps(stats, indent=2))
    
    # Cleanup
    os.remove('test_audit.db')
    print("\n✅ Test database cleaned up")


if __name__ == "__main__":
    test_audit_logger()
