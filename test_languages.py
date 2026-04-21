#!/usr/bin/env python3
"""
Test script to verify language detection for all supported languages
"""

import sys
sys.path.append('backend')
from validations import EssayValidator

def test_all_languages():
    """Test language detection for all supported languages"""
    
    validator = EssayValidator()
    
    # Test essays for each language
    test_essays = {
        'en': "This is an English essay. It contains proper English sentences with good grammar and structure. English language is widely spoken around the world.",
        'kn': "ಇದು ಕನ್ನಡ ಭಾಷೆಯಲ್ಲಿ ಬರೆದ ಪ್ರಬಂಧ. ಕನ್ನಡ ಒಂದು ಸುಂದರವಾದ ಭಾಷೆ. ಕನ್ನಡ ಸಾಹಿತ್ಯ ಬಹಳ ಶ್ರೀಮಂತವಾಗಿದೆ.",
        'ta': "இது தமிழ் மொழியில் எழுதப்பட்ட கட்டுரை. தமிழ் ஒரு செம்மொழி. தமிழ் இலக்கியம் சிறப்பானது.",
        'te': "ఇది తెలుగు భాషలో రాసిన వ్యాసం. తెలుగు ఒక అందమైన భాష. తెలుగు సాహిత్యం గొప్పది."
    }
    
    print("=" * 60)
    print("LANGUAGE DETECTION TEST RESULTS")
    print("=" * 60)
    
    for expected_lang, essay in test_essays.items():
        print(f"\nTesting {expected_lang.upper()}:")
        print(f"Essay: {essay}")
        
        # Test character detection
        detected_char = validator._detect_language_by_characters(essay)
        print(f"Character Detection: {detected_char}")
        
        # Test full validation
        validation_result = validator.validate_language_requirement(essay, expected_lang)
        print(f"Validation Result: {validation_result}")
        
        # Check if passed
        if validation_result['is_valid'] and validation_result['detected_language'] == expected_lang:
            print("✅ PASSED")
        else:
            print("❌ FAILED")
        
        print("-" * 40)
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    test_all_languages()
