# backend/validations.py
import re
from typing import Dict, Any, List, Tuple
from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator

class EssayValidator:
    """Handles strict validation rules for essay grading."""
    
    def __init__(self):
        self.supported_languages = {
            'en': 'English',
            'kn': 'Kannada',
            'ta': 'Tamil', 
            'te': 'Telugu'
        }
    
    def validate_language_requirement(self, essay_text: str, selected_language: str) -> Dict[str, Any]:
        """
        STRICT SYSTEM RULE: Validate that essay language matches user-selected language.
        This is a MANDATORY validation.
        """
        validation_result = {
            'is_valid': True,
            'detected_language': selected_language,
            'selected_language': selected_language,
            'language_violation': False,
            'error_message': None
        }
        
        # Debug info
        print(f"DEBUG: Essay length: {len(essay_text)} characters")
        print(f"DEBUG: Selected language: {selected_language}")
        
        # For Indian languages, always use character-based detection
        if selected_language in ['kn', 'ta', 'te']:
            detected_lang = self._detect_language_by_characters(essay_text)
            validation_result['detected_language'] = detected_lang
            
            print(f"DEBUG: Detected language: {detected_lang}")
            
            if detected_lang != selected_language:
                validation_result.update({
                    'is_valid': False,
                    'language_violation': True,
                    'error_message': f"LANGUAGE VIOLATION: Essay appears to be written in {self.supported_languages.get(detected_lang, detected_lang)} but you selected {self.supported_languages.get(selected_language, selected_language)}. This violates the strict system rule."
                })
        else:
            # For English, use langdetect
            try:
                detected_lang = detect(essay_text)
                validation_result['detected_language'] = detected_lang
                
                if detected_lang != selected_language:
                    validation_result.update({
                        'is_valid': False,
                        'language_violation': True,
                        'error_message': f"LANGUAGE VIOLATION: Essay is written in {self.supported_languages.get(detected_lang, detected_lang)} but you selected {self.supported_languages.get(selected_language, selected_language)}. This violates the strict system rule."
                    })
                    
            except LangDetectException:
                validation_result.update({
                    'is_valid': False,
                    'error_message': "LANGUAGE DETECTION ERROR: Unable to detect essay language. Please ensure the essay text is valid."
                })
            
        return validation_result
    
    def _detect_language_by_characters(self, text: str) -> str:
        """
        Fallback language detection using character patterns for Indian languages.
        """
        # Count characters from each language script
        kannada_chars = len(re.findall(r'[\u0C80-\u0CFF]', text))
        tamil_chars = len(re.findall(r'[\u0B80-\u0BFF]', text))
        telugu_chars = len(re.findall(r'[\u0C00-\u0C7F]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        
        # Debug info
        print(f"DEBUG: Kannada chars: {kannada_chars}")
        print(f"DEBUG: Tamil chars: {tamil_chars}")
        print(f"DEBUG: Telugu chars: {telugu_chars}")
        print(f"DEBUG: English chars: {english_chars}")
        print(f"DEBUG: Text sample: {text[:50]}...")
        
        # Determine dominant language
        char_counts = {
            'kn': kannada_chars,
            'ta': tamil_chars,
            'te': telugu_chars,
            'en': english_chars
        }
        
        # Return the language with most characters
        dominant_lang = max(char_counts, key=char_counts.get)
        
        # If no clear winner, default to English
        if char_counts[dominant_lang] == 0:
            return 'en'
            
        return dominant_lang
    
    def validate_response_language_compliance(self, response_text: str, target_language: str) -> Dict[str, Any]:
        """
        STRICT SYSTEM RULE: Validate that response is ONLY in the target language.
        No mixing languages allowed.
        """
        validation_result = {
            'is_compliant': True,
            'violations': [],
            'mixed_language_detected': False,
            'english_violation': False
        }
        
        # Check for English words when target is not English
        if target_language != 'en':
            # Only count actual English words (3+ characters), exclude numbers and single letters
            english_words = re.findall(r'\b[A-Za-z]{3,}\b', response_text)
            # Filter out common technical terms and numbers
            filtered_words = [word for word in english_words if not word.isdigit() and word.lower() not in ['score', 'feedback', 'analysis', 'grammar', 'readability']]
            if filtered_words:
                validation_result.update({
                    'is_compliant': False,
                    'english_violation': True,
                    'violations': [f"English words detected: {', '.join(filtered_words[:5])}"]
                })
        
        # Detect language of response
        if target_language in ['kn', 'ta', 'te']:
            # Use character-based detection for Indian languages
            detected_response_lang = self._detect_language_by_characters(response_text)
        else:
            # Use langdetect for English
            try:
                detected_response_lang = detect(response_text)
            except LangDetectException:
                detected_response_lang = 'en'  # Default fallback
        
        if detected_response_lang != target_language:
            validation_result.update({
                'is_compliant': False,
                'mixed_language_detected': True,
                'violations': [f"Response language ({detected_response_lang}) doesn't match target ({target_language})"]
            })
            
        return validation_result
    
    def generate_strict_language_response(self, essay_text: str, selected_language: str, 
                                         score: float, strengths: List[str], 
                                         weaknesses: List[str], suggestions: List[str]) -> Dict[str, Any]:
        """
        Generate response that STRICTLY follows the language rules.
        """
        # First validate the essay language
        lang_validation = self.validate_language_requirement(essay_text, selected_language)
        
        if not lang_validation['is_valid']:
            return {
                'error': True,
                'message': lang_validation['error_message'],
                'language_violation': True
            }
        
        # Build response components in the target language
        # Translate score text
        score_translations = {
            'en': f"Score: {score}/10",
            'kn': f"ಸ್ಕೋರ್: {score}/10",
            'ta': f"மதிப்பெண்: {score}/10",
            'te': f"స్కోరు: {score}/10"
        }
        
        response_components = {
            'score_out_of_10': score_translations.get(selected_language, f"Score: {score}/10"),
            'strengths': self._format_list("Strengths:", strengths, selected_language),
            'weaknesses': self._format_list("Weaknesses:", weaknesses, selected_language),
            'suggestions': self._format_list("Suggestions for improvement:", suggestions, selected_language)
        }
        
        # Combine into final response
        final_response = "\n\n".join([
            response_components['score_out_of_10'],
            response_components['strengths'],
            response_components['weaknesses'],
            response_components['suggestions']
        ])
        
        # Validate the generated response complies with language rules
        compliance_check = self.validate_response_language_compliance(final_response, selected_language)
        
        return {
            'error': False,
            'response': final_response,
            'language_compliance': compliance_check,
            'selected_language': selected_language
        }
    
    def _format_list(self, title: str, items: List[str], language: str) -> str:
        """Format a list of items in the target language."""
        if not items:
            # Simple translation for "None identified"
            none_translations = {
                'en': "None identified",
                'kn': "ಯಾವುದೂ ಗುರುತಿಸಲಾಗಿಲ್ಲ",
                'ta': "எதுவும் அடையாளம் காணப்படவில்லை",
                'te': "ఏమీ గుర్తించబడలేదు"
            }
            none_text = none_translations.get(language, "None identified")
            return f"{title} {none_text}."
        
        # Translate title if needed (basic implementation)
        title_translations = {
            'en': {
                'Strengths:': 'Strengths:',
                'Weaknesses:': 'Weaknesses:', 
                'Suggestions for improvement:': 'Suggestions for improvement:'
            },
            'kn': {
                'Strengths:': 'ಬಲಗಳು:',
                'Weaknesses:': 'ದೌರ್ಬಲ್ಯಗಳು:',
                'Suggestions for improvement:': 'ಸುಧಾರಣೆಗಾಗಿ ಸಲಹೆಗಳು:'
            },
            'ta': {
                'Strengths:': 'பலங்கள்:',
                'Weaknesses:': 'பலவடைவுகள்:',
                'Suggestions for improvement:': 'மேம்படுத்துவதற்கான பரிந்துரைகள்:'
            },
            'te': {
                'Strengths:': 'బలాలు:',
                'Weaknesses:': 'బలహీనతలు:',
                'Suggestions for improvement:': 'మెరుగుదల కోసం సూచనలు:'
            }
        }
        
        translated_title = title_translations.get(language, {}).get(title, title)
        formatted_items = "\n".join([f"• {item}" for item in items])
        
        return f"{translated_title}\n{formatted_items}"
    
    def validate_essay_content(self, essay_text: str) -> Dict[str, Any]:
        """Validate essay content quality and completeness."""
        validation = {
            'is_valid': True,
            'issues': [],
            'word_count': len(essay_text.split()),
            'character_count': len(essay_text),
            'sentence_count': len(re.split(r'[.!?]+', essay_text)) if essay_text else 0
        }
        
        # Check minimum length requirements
        if validation['word_count'] < 50:
            validation['is_valid'] = False
            validation['issues'].append("Essay too short - minimum 50 words required")
        
        if validation['sentence_count'] < 3:
            validation['is_valid'] = False
            validation['issues'].append("Essay too brief - minimum 3 sentences required")
        
        # Check for empty or whitespace-only content
        if not essay_text or essay_text.isspace():
            validation['is_valid'] = False
            validation['issues'].append("Essay content is empty")
            
        return validation
