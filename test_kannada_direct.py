#!/usr/bin/env python3
"""
Direct test of Kannada character detection
"""

import sys
sys.path.append('backend')
from validations import EssayValidator

def test_kannada_direct():
    """Test Kannada detection directly"""
    
    validator = EssayValidator()
    
    # Test the exact same text
    kannada_essay = "ಕೊರೋನಾ ವೈರಸ್ ಚೀನಾದ ವುಹಾನ್ ನಗರದಲ್ಲಿ ಮೊದಲ ಬಾರಿಗೆ ಪತ್ತೆಯಾಯಿತು. ನಂತರ ಇದು ವಿಶ್ವದಾದ್ಯಂತ ವೇಗವಾಗಿ ಹರಡಿತು. ಮಾನವ ಇತಿಹಾಸದಲ್ಲಿ ದೊಡ್ಡ ಆರೋಗ್ಯ ಸಂಕಟವನ್ನು ಉಂಟುಮಾಡಿದ ಈ ವೈರಸ್ ಸಮಾಜ, ಆರ್ಥಿಕತೆ, ಶಿಕ್ಷಣ ಮತ್ತು ಮಾನವ ಜೀವನದ ಎಲ್ಲ ಕ್ಷೇತ್ರಗಳ ಮೇಲೂ ಆಳವಾದ ಪರಿಣಾಮ ಬೀರಿತು. ಆರೋಗ್ಯದ ಮೇಲೆ ಪರಿಣಾಮ, ಆರ್ಥಿಕ ಪರಿಣಾಮ, ಶಿಕ್ಷಣದ ಮೇಲೆ ಪರಿಣಾಮ, ಸಾಮಾಜಿಕ ಮತ್ತು ಮಾನಸಿಕ ಪರಿಣಾಮ, ಪರಿಸರದ ಮೇಲೆ ಪರಿಣಾಮ. ಕೊರೋನಾ ವೈರಸ್ ಮಾನವ ಜೀವನದ ಎಲ್ಲಾ ಕ್ಷೇತ್ರಗಳ ಮೇಲೆ ಆಳವಾದ ಪರಿಣಾಮ ಬೀರಿತು. ಇದು ನಮಗೆ ಆರೋಗ್ಯದ ಮಹತ್ವ, ತಂತ್ರಜ್ಞಾನ ಬಳಕೆ, ಪರಿಸರ ಸಂರಕ್ಷಣೆ ಮತ್ತು ಮಾನವೀಯ ಮೌಲ್ಯಗಳ ಅರಿವು ಮೂಡಿಸಿತು. ಸಂಕಷ್ಟದ ಸಮಯದಲ್ಲಿ ಸಹಕಾರ, ಸಹಾನುಭೂತಿ ಮತ್ತು ಶಿಸ್ತು ಪಾಲನೆಯೇ ಸಮಾಜವನ್ನು ಉಳಿಸುವ ಶಕ್ತಿ ಎಂಬುದನ್ನು ಈ ಮಹಾಮಾರಿ ನಮಗೆ ಕಲಿಸಿತು."
    
    print("=" * 60)
    print("DIRECT KANNADA TEST")
    print("=" * 60)
    print(f"Essay text: {kannada_essay}")
    print(f"Essay length: {len(kannada_essay)} characters")
    
    # Test character detection
    detected_lang = validator._detect_language_by_characters(kannada_essay)
    print(f"Detected language: {detected_lang}")
    
    # Test validation
    validation_result = validator.validate_language_requirement(kannada_essay, 'kn')
    print(f"Validation result: {validation_result}")
    
    if validation_result['is_valid']:
        print("✅ SUCCESS: Kannada language detected correctly!")
    else:
        print("❌ FAILED: Language detection issue")
    
    print("=" * 60)

if __name__ == "__main__":
    test_kannada_direct()
