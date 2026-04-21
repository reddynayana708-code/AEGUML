# backend/feedback_engine.py
import re
import nltk
from textblob import TextBlob
import textstat
from typing import Dict, List, Any, Tuple
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('vader_lexicon', quiet=True)

def clean_text(text: str) -> str:
    """Clean and preprocess text."""
    if not text or not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove punctuation and special characters
    text = re.sub(r'[^\w\s]', '', text)
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def grammar_feedback(text: str) -> Dict[str, Any]:
    """Analyze grammar and provide feedback."""
    feedback = {
        'score': 0.0,
        'issues': [],
        'suggestions': []
    }
    
    try:
        if not text or not isinstance(text, str) or not text.strip():
            return feedback
            
        # Basic text analysis
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())
        word_count = len(words)
        
        if not sentences:
            return feedback
            
        # Calculate average sentence length
        avg_sentence_length = word_count / len(sentences)
        
        # Check for long sentences
        long_sentences = [s for s in sentences if len(word_tokenize(s)) > 30]
        if long_sentences:
            feedback['issues'].append(f"Found {len(long_sentences)} long sentences (over 30 words).")
            feedback['suggestions'].append("Consider breaking long sentences into shorter ones for better readability.")
        
        # Check for passive voice
        passive_voice = [s for s in sentences 
                        if re.search(r'\b(am|are|were|being|is|been|was|be)\s+\w+ed\b', s, re.IGNORECASE)]
        if passive_voice:
            feedback['issues'].append(f"Found {len(passive_voice)} instances of passive voice.")
            feedback['suggestions'].append("Consider using active voice for more direct and engaging writing.")
        
        # Basic grammar score
        issue_count = len(long_sentences) + len(passive_voice)
        feedback['score'] = max(0.0, min(1.0, 0.8 - (issue_count * 0.05)))
        
    except Exception as e:
        print(f"Error in grammar analysis: {str(e)}")
        feedback['error'] = str(e)
    
    return feedback

def readability_metrics(text: str) -> Dict[str, Any]:
    """Calculate various readability metrics."""
    metrics = {
        'flesch_reading_ease': 0.0,
        'flesch_kincaid_grade': 0.0,
        'gunning_fog': 0.0,
        'smog_index': 0.0,
        'automated_readability_index': 0.0,
        'coleman_liau_index': 0.0,
        'dale_chall_readability_score': 0.0,
        'difficult_words': 0,
        'linsear_write_formula': 0.0,
        'text_standard': '',
        'word_count': 0,
        'sentence_count': 0,
        'avg_word_length': 0.0,
        'avg_sentence_length': 0.0,
        'passive_voice_instances': 0,
        'long_sentences': 0
    }
    
    try:
        if not text or not isinstance(text, str) or not text.strip():
            return metrics
            
        # Basic text statistics
        words = [word for word in re.findall(r'\b\w+\b', text) if word]
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
        metrics['word_count'] = len(words)
        metrics['sentence_count'] = len(sentences) if sentences else 1
        
        if words:
            metrics['avg_word_length'] = sum(len(word) for word in words) / len(words)
            metrics['avg_sentence_length'] = len(words) / metrics['sentence_count']
        
        # Only calculate other metrics if we have enough text
        if metrics['word_count'] > 0 and metrics['sentence_count'] > 0:
            try:
                metrics['flesch_reading_ease'] = textstat.flesch_reading_ease(text)
                metrics['flesch_kincaid_grade'] = textstat.flesch_kincaid_grade(text)
                metrics['gunning_fog'] = textstat.gunning_fog(text)
                metrics['smog_index'] = textstat.smog_index(text)
                metrics['automated_readability_index'] = textstat.automated_readability_index(text)
                metrics['coleman_liau_index'] = textstat.coleman_liau_index(text)
                metrics['dale_chall_readability_score'] = textstat.dale_chall_readability_score(text)
                metrics['difficult_words'] = textstat.difficult_words(text)
                metrics['linsear_write_formula'] = textstat.linsear_write_formula(text)
                metrics['text_standard'] = textstat.text_standard(text)
            except Exception as e:
                print(f"Error in textstat calculations: {str(e)}")
        
        # Check for passive voice
        metrics['passive_voice_instances'] = len(re.findall(
            r'\b(am|are|were|being|is|been|was|be)\s+\w+ed\b', 
            text, 
            re.IGNORECASE
        ))
        
        # Check for long sentences
        metrics['long_sentences'] = len([
            s for s in sentences 
            if len(re.findall(r'\b\w+\b', s)) > 30
        ])
        
    except Exception as e:
        print(f"Error in readability metrics: {str(e)}")
        metrics['error'] = str(e)
    
    return metrics

def sentiment_summary(text: str) -> Dict[str, float]:
    """Analyze sentiment of the text."""
    sentiment = {
        'positive': 0.0,
        'neutral': 0.0,
        'negative': 0.0,
        'compound': 0.0,
        'sentiment_score': 0.0
    }
    
    try:
        if not text or not isinstance(text, str) or not text.strip():
            return sentiment
            
        sia = SentimentIntensityAnalyzer()
        scores = sia.polarity_scores(text)
        
        sentiment.update({
            'positive': scores['pos'],
            'neutral': scores['neu'],
            'negative': scores['neg'],
            'compound': scores['compound'],
            'sentiment_score': scores['compound']  # For backward compatibility
        })
        
    except Exception as e:
        print(f"Error in sentiment analysis: {str(e)}")
        sentiment['error'] = str(e)
    
    return sentiment

def detect_bias(text: str) -> Dict[str, Any]:
    """Detect potential bias in the text."""
    bias = {
        'bias_score': 0.0,
        'biased_phrases': [],
        'explanation': '',
        'suggestions': []
    }
    
    try:
        if not text or not isinstance(text, str) or not text.strip():
            return bias
            
        # List of potentially biased terms
        biased_terms = {
            'always', 'never', 'everyone knows', 'clearly', 'obviously',
            'undoubtedly', 'certainly', 'naturally', 'of course', 'everyone agrees',
            'best', 'worst', 'everyone', 'nobody', 'all', 'none'
        }
        
        # Check for biased language
        words = set(word_tokenize(text.lower()))
        found_biased = list(biased_terms.intersection(words))
        
        if found_biased:
            bias['biased_phrases'] = found_biased
            bias['bias_score'] = min(1.0, len(found_biased) * 0.2)
            bias['explanation'] = 'Potential bias detected in the text.'
            bias['suggestions'].append('Consider using more neutral language and providing evidence for claims.')
        else:
            bias['explanation'] = 'No significant bias detected.'
            
    except Exception as e:
        print(f"Error in bias detection: {str(e)}")
        bias['error'] = str(e)
    
    return bias

def suggestions(text: str, metrics: dict = None, grammar: dict = None) -> List[str]:
    """Generate suggestions for improving the essay."""
    suggestions_list = []
    
    try:
        if not text or not isinstance(text, str) or not text.strip():
            return suggestions_list
            
        # Add grammar suggestions
        if grammar and 'suggestions' in grammar:
            suggestions_list.extend(grammar['suggestions'])
        
        # Add readability suggestions
        if metrics:
            if metrics.get('avg_sentence_length', 0) > 25:
                suggestions_list.append("Your sentences are quite long. Try breaking them into shorter ones for better readability.")
            
            if metrics.get('passive_voice_instances', 0) > 3:
                suggestions_list.append("Consider using active voice more often for clearer writing.")
            
            if metrics.get('flesch_reading_ease', 0) < 50:
                suggestions_list.append("Your text may be difficult to read. Consider using simpler words and shorter sentences.")
            
            if metrics.get('avg_word_length', 0) > 6:
                suggestions_list.append("Some words are quite long. Consider using simpler alternatives where possible.")
        
        # Add sentiment-based suggestions
        sentiment = sentiment_summary(text)
        if sentiment['compound'] < -0.5:
            suggestions_list.append("The tone seems negative. Consider balancing with more positive language.")
        elif sentiment['compound'] > 0.5:
            suggestions_list.append("The tone is quite positive. For academic writing, aim for a more neutral tone.")
        
        # Ensure we don't have too many suggestions
        return list(set(suggestions_list[:5]))  # Return up to 5 unique suggestions
        
    except Exception as e:
        print(f"Error generating suggestions: {str(e)}")
        return ["Error generating suggestions."]

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()