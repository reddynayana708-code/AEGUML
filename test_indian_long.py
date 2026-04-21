#!/usr/bin/env python3
"""
Test Indian languages with longer essays
"""

import requests
import json

def test_kannada_long():
    """Test Kannada with longer essay"""
    
    url = "http://localhost:8000/grade"
    
    kannada_essay = "ಕೊರೋನಾ ವೈರಸ್ ಚೀನಾದ ವುಹಾನ್ ನಗರದಲ್ಲಿ ಮೊದಲ ಬಾರಿಗೆ ಪತ್ತೆಯಾಯಿತು. ನಂತರ ಇದು ವಿಶ್ವದಾದ್ಯಂತ ವೇಗವಾಗಿ ಹರಡಿತು. ಮಾನವ ಇತಿಹಾಸದಲ್ಲಿ ದೊಡ್ಡ ಆರೋಗ್ಯ ಸಂಕಟವನ್ನು ಉಂಟುಮಾಡಿದ ಈ ವೈರಸ್ ಸಮಾಜ, ಆರ್ಥಿಕತೆ, ಶಿಕ್ಷಣ ಮತ್ತು ಮಾನವ ಜೀವನದ ಎಲ್ಲ ಕ್ಷೇತ್ರಗಳ ಮೇಲೂ ಆಳವಾದ ಪರಿಣಾಮ ಬೀರಿತು. ಲಕ್ಷಾಂತರ ಜನರು ಸೋಂಕಿಗೆ ಒಳಗಾದರು ಮತ್ತು ಅನೇಕರು ಜೀವ ಕಳೆದುಕೊಂಡರು. ಆಸ್ಪತ್ರೆಗಳು ತುಂಬಿ ಹೋಗಿ ವೈದ್ಯಕೀಯ ವ್ಯವಸ್ಥೆ ದೊಡ್ಡ ಸವಾಲನ್ನು ಎದುರಿಸಿತು. ಜನರು ಮಾಸ್ಕ್, ಸ್ಯಾನಿಟೈಸರ್, ಸಾಮಾಜಿಕ ಅಂತರ ಪಾಲನೆ ಮುಂತಾದ ನಿಯಮಗಳನ್ನು ಪಾಲಿಸಲು ಆರಂಭಿಸಿದರು. ಲಾಕ್‌ಡೌನ್‌ನಿಂದ ಕೈಗಾರಿಕೆಗಳು, ವ್ಯಾಪಾರ, ಪ್ರವಾಸೋದ್ಯಮ, ಹೋಟೆಲ್‌ಗಳು ಮುಂತಾದವುಗಳು ಕುಸಿದವು. ಅನೇಕರು ಉದ್ಯೋಗ ಕಳೆದುಕೊಂಡರು ಮತ್ತು ಬಡತನ ಹೆಚ್ಚಾಯಿತು. ಶಾಲೆಗಳು ಮತ್ತು ಕಾಲೇಜುಗಳು ಮುಚ್ಚಲ್ಪಟ್ಟವು. ಆನ್‌ಲೈನ್ ಶಿಕ್ಷಣಕ್ಕೆ ಹೆಚ್ಚಿನ ಒತ್ತು ನೀಡಲಾಯಿತು. ಜನರು ಮನೆಯೊಳಗೆ ಸೀಮಿತಗೊಂಡರು, ಸಾಮಾಜಿಕ ಸಂಪರ್ಕ ಕಡಿಮೆಯಾಯಿತು. ಒತ್ತಡ, ಆತಂಕ, ಮನೋವೈಕಲ್ಯ ಹೆಚ್ಚಾಯಿತು. ಲಾಕ್‌ಡೌನ್ ಸಮಯದಲ್ಲಿ ವಾಹನ ಸಂಚಾರ ಕಡಿಮೆಯಾದ ಕಾರಣ ವಾಯು ಮಾಲಿನ್ಯ ತಗ್ಗಿತು. ಪ್ರಕೃತಿ ತನ್ನ ಸ್ವಾಭಾವಿಕ ರೂಪವನ್ನು ಮರಳಿ ಪಡೆಯಿತು. ಕೊರೋನಾ ವೈರಸ್ ಮಾನವ ಜೀವನದ ಎಲ್ಲಾ ಕ್ಷೇತ್ರಗಳ ಮೇಲೆ ಆಳವಾದ ಪರಿಣಾಮ ಬೀರಿತು. ಇದು ನಮಗೆ ಆರೋಗ್ಯದ ಮಹತ್ವ, ತಂತ್ರಜ್ಞಾನ ಬಳಕೆ, ಪರಿಸರ ಸಂರಕ್ಷಣೆ ಮತ್ತು ಮಾನವೀಯ ಮೌಲ್ಯಗಳ ಅರಿವು ಮೂಡಿಸಿತು. ಸಂಕಷ್ಟದ ಸಮಯದಲ್ಲಿ ಸಹಕಾರ, ಸಹಾನುಭೂತಿ ಮತ್ತು ಶಿಸ್ತು ಪಾಲನೆಯೇ ಸಮಾಜವನ್ನು ಉಳಿಸುವ ಶಕ್ತಿ ಎಂಬುದನ್ನು ಈ ಮಹಾಮಾರಿ ನಮಗೆ ಕಲಿಸಿತು."
    
    payload = {
        "essay": kannada_essay,
        "selected_language": "kn"
    }
    
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    
    print("🧪 TESTING KANNADA (LONG ESSAY)")
    print("=" * 60)
    print(f"Essay length: {len(kannada_essay)} characters")
    print(f"Word count: {len(kannada_essay.split())} words")
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"Predicted score: {result.get('predicted_score', 'N/A')}")
            print(f"Detected language: {result.get('detected_language', 'N/A')}")
            print(f"Language compliance: {result.get('language_compliance', {}).get('is_compliant', 'N/A')}")
            print(f"Feedback preview: {result.get('strict_response', '')[:100]}...")
        else:
            print("❌ FAILED!")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")

if __name__ == "__main__":
    test_kannada_long()
