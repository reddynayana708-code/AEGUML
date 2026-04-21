# tests/test_validations.py
import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from validations import EssayValidator

class TestEssayValidator:
    """Test cases for the strict validation system."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.validator = EssayValidator()
    
    def test_language_validation_english_success(self):
        """Test successful English language validation."""
        essay = "This is a test essay written in English. It contains proper sentences and grammar."
        result = self.validator.validate_language_requirement(essay, 'en')
        
        assert result['is_valid'] == True
        assert result['detected_language'] == 'en'
        assert result['selected_language'] == 'en'
        assert result['language_violation'] == False
    
    def test_language_validation_violation(self):
        """Test language validation failure."""
        # Spanish essay but expecting English
        spanish_essay = "Este es un ensayo de prueba escrito en español. Contiene oraciones adecuadas."
        result = self.validator.validate_language_requirement(spanish_essay, 'en')
        
        assert result['is_valid'] == False
        assert result['language_violation'] == True
        assert 'LANGUAGE VIOLATION' in result['error_message']
    
    def test_content_validation_minimum_requirements(self):
        """Test content validation for minimum requirements."""
        # Test too short essay
        short_essay = "Too short."
        result = self.validator.validate_essay_content(short_essay)
        
        assert result['is_valid'] == False
        assert any('too short' in issue.lower() for issue in result['issues'])
        assert result['word_count'] < 50
    
    def test_content_validation_valid_essay(self):
        """Test content validation for valid essay."""
        valid_essay = """
        This is a valid test essay that meets the minimum requirements. 
        It contains enough words to pass the validation check. 
        The essay has multiple sentences and proper structure. 
        This should be considered a valid submission for testing purposes.
        """
        result = self.validator.validate_essay_content(valid_essay)
        
        assert result['is_valid'] == True
        assert result['word_count'] >= 50
        assert result['sentence_count'] >= 3
    
    def test_content_validation_empty_essay(self):
        """Test content validation for empty essay."""
        result = self.validator.validate_essay_content("")
        
        assert result['is_valid'] == False
        assert any('empty' in issue.lower() for issue in result['issues'])
    
    def test_strict_response_generation_english(self):
        """Test strict response generation in English."""
        essay = "This is a test essay in English."
        score = 8.5
        strengths = ["Good structure", "Clear arguments"]
        weaknesses = ["Some grammar issues"]
        suggestions = ["Review grammar rules"]
        
        result = self.validator.generate_strict_language_response(
            essay, 'en', score, strengths, weaknesses, suggestions
        )
        
        assert result['error'] == False
        assert 'Score: 8.5/10' in result['response']
        assert 'Strengths:' in result['response']
        assert 'Weaknesses:' in result['response']
        assert 'Suggestions for improvement:' in result['response']
        assert result['language_compliance']['is_compliant'] == True
    
    def test_response_language_compliance_check(self):
        """Test response language compliance validation."""
        # Test English response with English words (should be compliant)
        english_response = "This is a response in English with proper words."
        result = self.validator.validate_response_language_compliance(english_response, 'en')
        
        assert result['is_compliant'] == True
        assert result['english_violation'] == False
        assert result['mixed_language_detected'] == False
    
    def test_multilingual_support(self):
        """Test multilingual language support."""
        supported_langs = self.validator.supported_languages
        
        assert 'en' in supported_langs
        assert 'kn' in supported_langs  # Kannada
        assert 'ta' in supported_langs  # Tamil
        assert 'te' in supported_langs  # Telugu
        
        assert supported_langs['en'] == 'English'
        assert supported_langs['kn'] == 'Kannada'

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
