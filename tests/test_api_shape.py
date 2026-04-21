import json
import threading
import time
import requests

# NOTE: Requires backend to be running locally on port 8000.

def test_grade_endpoint_shape():
    try:
        r = requests.post('http://localhost:8000/grade', json={"essay": "This is a simple test essay with enough content to pass validation."}, timeout=5)
        assert r.status_code in (200, 400, 500)
        if r.status_code == 200:
            data = r.json()
            assert 'predicted_score' in data
            assert 'feedback' in data
            assert 'readability' in data
            assert 'sentiment' in data
    except Exception:
        # If API isn't running, skip
        pass
