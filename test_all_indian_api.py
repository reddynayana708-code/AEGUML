#!/usr/bin/env python3
"""
Test all Indian languages via API
"""

import requests
import json

def test_language_api(language_code, essay_text, language_name):
    """Test specific language via API"""
    
    url = "http://localhost:8000/grade"
    
    payload = {
        "essay": essay_text,
        "selected_language": language_code
    }
    
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    
    print(f"\n{'='*60}")
    print(f"Testing {language_name} ({language_code})")
    print(f"{'='*60}")
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"Predicted score: {result.get('predicted_score', 'N/A')}")
            print(f"Detected language: {result.get('detected_language', 'N/A')}")
            print(f"Language compliance: {result.get('language_compliance', {}).get('is_compliant', 'N/A')}")
            print(f"Feedback length: {len(result.get('strict_response', ''))} characters")
        else:
            print("❌ FAILED!")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")

def main():
    """Test all Indian languages"""
    
    # Test essays
    essays = {
        'kn': (
            "ಇದು ಕನ್ನಡ ಭಾಷೆಯಲ್ಲಿ ಬರೆದ ಪ್ರಬಂಧ. ಕನ್ನಡ ಒಂದು ಸುಂದರವಾದ ಭಾಷೆ. "
            "ಕನ್ನಡ ಸಾಹಿತ್ಯ ಬಹಳ ಶ್ರೀಮಂತವಾಗಿದೆ. ನಾವು ಕನ್ನಡವನ್ನು ಪ್ರೀತಿಸಬೇಕು. "
            "ಕನ್ನಡ ಭಾಷೆ ನಮ್ಮ ಗೌರವಕ್ಕೆ ಪಾತ್ರವಾಗಿದೆ.",
            "Kannada"
        ),
        'ta': (
            "இது தமிழ் மொழியில் எழுதப்பட்ட கட்டுரை. தமிழ் ஒரு செம்மொழி. "
            "தமிழ் இலக்கியம் சிறப்பானது. தமிழ் மொழி அழகான மொழி. "
            "தமிழ் இலக்கியங்கள் பல உள்ளன.",
            "Tamil"
        ),
        'te': (
            "ఇది తెలుగు భాషలో రాసిన వ్యాసం. తెలుగు ఒక అందమైన భాష. "
            "తెలుగు సాహిత్యం గొప్పది. తెలుగు భాష చాలా అందంగా ఉంటుంది. "
            "తెలుగు సాహిత్యం చాలా సంపన్నంగా ఉంది.",
            "Telugu"
        )
    }
    
    print("🧪 TESTING ALL INDIAN LANGUAGES")
    print("=" * 60)
    
    for lang_code, (essay_text, lang_name) in essays.items():
        test_language_api(lang_code, essay_text, lang_name)
    
    print(f"\n{'='*60}")
    print("TESTING COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    main()
