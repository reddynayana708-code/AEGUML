#!/usr/bin/env python3
"""
Test Kannada essay via API with proper Unicode handling
"""

import requests
import json

def test_kannada_api():
    """Test Kannada essay via API"""
    
    url = "http://localhost:8000/grade"
    
    # The same essay you tried
    kannada_essay = "ಕೊರೋನಾ ವೈರಸ್ ಚೀನಾದ ವುಹಾನ್ ನಗರದಲ್ಲಿ ಮೊದಲ ಬಾರಿಗೆ ಪತ್ತೆಯಾಯಿತು. ನಂತರ ಇದು ವಿಶ್ವದಾದ್ಯಂತ ವೇಗವಾಗಿ ಹರಡಿತು. ಮಾನವ ಇತಿಹಾಸದಲ್ಲಿ ದೊಡ್ಡ ಆರೋಗ್ಯ ಸಂಕಟವನ್ನು ಉಂಟುಮಾಡಿದ ಈ ವೈರಸ್ ಸಮಾಜ, ಆರ್ಥಿಕತೆ, ಶಿಕ್ಷಣ ಮತ್ತು ಮಾನವ ಜೀವನದ ಎಲ್ಲ ಕ್ಷೇತ್ರಗಳ ಮೇಲೂ ಆಳವಾದ ಪರಿಣಾಮ ಬೀರಿತು. ಆರೋಗ್ಯದ ಮೇಲೆ ಪರಿಣಾಮ, ಆರ್ಥಿಕ ಪರಿಣಾಮ, ಶಿಕ್ಷಣದ ಮೇಲೆ ಪರಿಣಾಮ, ಸಾಮಾಜಿಕ ಮತ್ತು ಮಾನಸಿಕ ಪರಿಣಾಮ, ಪರಿಸರದ ಮೇಲೆ ಪರಿಣಾಮ. ಕೊರೋನಾ ವೈರಸ್ ಮಾನವ ಜೀವನದ ಎಲ್ಲಾ ಕ್ಷೇತ್ರಗಳ ಮೇಲೆ ಆಳವಾದ ಪರಿಣಾಮ ಬೀರಿತು. ಇದು ನಮಗೆ ಆರೋಗ್ಯದ ಮಹತ್ವ, ತಂತ್ರಜ್ಞಾನ ಬಳಕೆ, ಪರಿಸರ ಸಂರಕ್ಷಣೆ ಮತ್ತು ಮಾನವೀಯ ಮೌಲ್ಯಗಳ ಅರಿವು ಮೂಡಿಸಿತು. ಸಂಕಷ್ಟದ ಸಮಯದಲ್ಲಿ ಸಹಕಾರ, ಸಹಾನುಭೂತಿ ಮತ್ತು ಶಿಸ್ತು ಪಾಲನೆಯೇ ಸಮಾಜವನ್ನು ಉಳಿಸುವ ಶಕ್ತಿ ಎಂಬುದನ್ನು ಈ ಮಹಾಮಾರಿ ನಮಗೆ ಕಲಿಸಿತು."
    
    payload = {
        "essay": kannada_essay,
        "selected_language": "kn"
    }
    
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    
    print("=" * 60)
    print("KANNADA API TEST")
    print("=" * 60)
    print(f"Sending request to: {url}")
    print(f"Essay length: {len(kannada_essay)} characters")
    print(f"Selected language: kn")
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"Predicted score: {result.get('predicted_score', 'N/A')}")
            print(f"Detected language: {result.get('detected_language', 'N/A')}")
            print(f"Feedback language compliance: {result.get('language_compliance', {}).get('is_compliant', 'N/A')}")
        else:
            print("❌ FAILED!")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
    
    print("=" * 60)

if __name__ == "__main__":
    test_kannada_api()
