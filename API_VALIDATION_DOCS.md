# API Documentation - Enhanced Essay Grading with Strict Validations

## Overview
The essay grading API now includes strict validation rules to ensure language compliance and content quality.

## New Features

### 1. Strict Language Validation
- **MANDATORY**: Essay language must match user-selected language
- **NO LANGUAGE MIXING**: Response generated exclusively in target language
- **AUTOMATIC DETECTION**: System detects and rejects language mismatches

### 2. Content Quality Validation
- **Minimum 50 words** required
- **Minimum 3 sentences** required
- **Empty content** detection

### 3. Language Compliance Enforcement
- **Response validation** to ensure target language compliance
- **English word detection** when target is non-English
- **Mixed language prevention**

## API Endpoints

### POST /grade
Enhanced grading endpoint with strict validations.

#### Request Format
```json
{
  "essay": "Your essay text here...",
  "selected_language": "en|kn|ta|te"
}
```

#### Parameters
- `essay` (string, required): Essay text to be graded
- `selected_language` (string, required): Target language code
  - `en`: English
  - `kn`: Kannada (ಕನ್ನಡ)
  - `ta`: Tamil (தமிழ்)
  - `te`: Telugu (తెలుగు)

#### Success Response (200)
```json
{
  "error": false,
  "predicted_score": 8.5,
  "strict_response": "Score: 8.5/10\n\nStrengths:\n• Good organization and structure\n• Clear thesis statement\n\nWeaknesses:\n• Some grammatical errors present\n• Limited vocabulary variety\n\nSuggestions for improvement:\n• Review grammar rules\n• Expand vocabulary",
  "selected_language": "en",
  "language_compliance": {
    "is_compliant": true,
    "violations": [],
    "mixed_language_detected": false,
    "english_violation": false
  },
  "validation_passed": true,
  "language_rules_followed": true,
  "strengths": ["Good organization and structure", "Clear thesis statement"],
  "weaknesses": ["Some grammatical errors present", "Limited vocabulary variety"],
  "suggestions": ["Review grammar rules", "Expand vocabulary"],
  "grammar": {"score": 0.8, "issues": []},
  "readability": {
    "word_count": 150,
    "sentence_count": 10,
    "avg_word_length": 5.2,
    "avg_sentence_length": 15.0
  },
  "sentiment": {"positive": 0.6, "neutral": 0.3, "negative": 0.1, "compound": 0.8},
  "bias_analysis": {"bias_score": 0.2, "bias_categories": {}},
  "plagiarism": {"is_plagiarized": false, "similarity_score": 0.05}
}
```

#### Error Responses

##### Language Violation (400)
```json
{
  "error": true,
  "message": "LANGUAGE VIOLATION: Essay is written in Spanish but you selected English. This violates the strict system rule.",
  "language_violation": true,
  "detected_language": "es",
  "selected_language": "en"
}
```

##### Content Validation Failed (400)
```json
{
  "error": true,
  "message": "Essay validation failed",
  "content_issues": ["Essay too short - minimum 50 words required"],
  "word_count": 25,
  "sentence_count": 2
}
```

##### Language Compliance Violation (400)
```json
{
  "error": true,
  "message": "Language compliance violation detected",
  "violations": ["English words detected: the, and, is"]
}
```

## STRICT SYSTEM RULES

### Mandatory Rules
1. **Essay Language Validation**: The system validates that the essay is written in the selected language
2. **Exclusive Language Response**: The entire response is generated ONLY in the selected language
3. **No English Mixing**: No English words unless the selected language is English
4. **No Language Mixing**: No mixing of languages under any circumstance
5. **Invalid Output**: Any response with words outside the selected language is considered INVALID

### Supported Languages
- **English (en)**: Default language
- **Kannada (kn)**: ಕನ್ನಡ
- **Tamil (ta)**: தமிழ்  
- **Telugu (te)**: తెలుగు

## Frontend Integration

### New UI Features
1. **Language Selection Warning**: Clear indication of strict language requirements
2. **Validation Error Display**: Detailed error messages for validation failures
3. **Strict Response Section**: Dedicated area for language-compliant evaluation
4. **Compliance Indicators**: Visual confirmation of rule adherence

### Error Handling
- **Language Violation**: Detected language vs selected language comparison
- **Content Issues**: Word count, sentence count, and quality metrics
- **Compliance Violations**: Specific rule violations with explanations

## Testing

### Test Cases
```bash
# Run validation tests
python -m pytest tests/test_validations.py -v

# Test language validation
python -c "
from backend.validations import EssayValidator
v = EssayValidator()
result = v.validate_language_requirement('Test essay', 'en')
print(result)
"
```

### Test Scenarios
1. **Valid Essay**: English essay with English selection
2. **Language Mismatch**: Spanish essay with English selection
3. **Short Essay**: Less than 50 words
4. **Empty Essay**: No content
5. **Multilingual**: Essays in Kannada, Tamil, Telugu

## Implementation Details

### Validation Flow
1. **Input Validation**: Check essay text and language selection
2. **Language Detection**: Detect actual essay language
3. **Language Compliance**: Validate essay language matches selection
4. **Content Validation**: Check minimum requirements
5. **Response Generation**: Create evaluation in target language only
6. **Response Validation**: Ensure response follows language rules
7. **Return Results**: Comprehensive feedback with compliance status

### Security Features
- **Language Detection**: Prevents language bypass attempts
- **Content Validation**: Ensures minimum quality standards
- **Response Validation**: Guarantees language compliance
- **Error Handling**: Clear validation failure messages

## Migration Notes

### Breaking Changes
- Request parameter changed from `target_language` to `selected_language`
- New validation errors with 400 status codes
- Additional response fields for validation status

### Compatibility
- Existing response structure maintained
- New fields are additive
- Error handling enhanced

## Support

For issues with the validation system:
1. Check language detection accuracy
2. Verify content meets minimum requirements
3. Ensure proper language selection
4. Review validation error messages

---

**Version**: 2.0.0  
**Last Updated**: Enhanced with strict validation rules  
**Compliance**: Mandatory language enforcement system
