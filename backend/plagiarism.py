import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from bs4 import BeautifulSoup
import re
import time
from typing import Dict, List, Optional, Union
import os
from urllib.parse import quote_plus

class PlagiarismDetector:
    def __init__(self, threshold: float = 0.8, google_api_key: str = None, 
                 google_cse_id: str = None, request_delay: float = 1.0):
        """
        Initialize the plagiarism detector.
        
        Args:
            threshold: Similarity threshold (0-1) to consider as plagiarism
            google_api_key: Google Custom Search JSON API key
            google_cse_id: Google Custom Search Engine ID
            request_delay: Delay between API requests in seconds
        """
        self.threshold = threshold
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.google_api_key = google_api_key or os.getenv('GOOGLE_API_KEY')
        self.google_cse_id = google_cse_id or os.getenv('GOOGLE_CSE_ID')
        self.request_delay = request_delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def check_plagiarism(self, text1: str, text2: str) -> Dict[str, Union[float, bool, str]]:
        """
        Check similarity between two texts using cosine similarity.
        
        Args:
            text1: First text to compare
            text2: Second text to compare
            
        Returns:
            Dictionary containing similarity score, plagiarism flag, and threshold
        """
        if not text1 or not text2:
            return {
                'error': 'Both text1 and text2 must be non-empty strings',
                'similarity_score': 0.0,
                'is_plagiarized': False,
                'threshold': self.threshold
            }
            
        try:
            tfidf = self.vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
            
            return {
                'similarity_score': round(float(similarity), 4),
                'is_plagiarized': bool(similarity > self.threshold),
                'threshold': float(self.threshold)
            }
        except Exception as e:
            return {
                'error': str(e),
                'similarity_score': 0.0,
                'is_plagiarized': False,
                'threshold': float(self.threshold)
            }

    def _extract_text_from_url(self, url: str) -> str:
        """Extract clean text from a webpage URL."""
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
                
            # Get text and clean it
            text = soup.get_text(separator=' ', strip=True)
            text = ' '.join(text.split())  # Normalize whitespace
            return text
        except Exception as e:
            print(f"Error extracting text from {url}: {str(e)}")
            return ""

    def _google_search(self, query: str, num_results: int = 5) -> List[Dict]:
        """Search Google using Custom Search JSON API."""
        if not self.google_api_key or not self.google_cse_id:
            raise ValueError("Google API key and CSE ID are required for online search")
            
        search_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'q': query,
            'key': self.google_api_key,
            'cx': self.google_cse_id,
            'num': min(num_results, 10)  # Google allows max 10 results per request
        }
        
        try:
            response = self.session.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get('items', []):
                results.append({
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', '')
                })
            return results
        except Exception as e:
            print(f"Google Search API error: {str(e)}")
            return []

    def check_online_sources(self, text: str, max_results: int = 3) -> Dict:
        """
        Check text against online sources for potential plagiarism.
        
        Args:
            text: Text to check
            max_results: Maximum number of online sources to check
            
        Returns:
            Dictionary containing search results and potential matches
        """
        if not text.strip():
            return {
                'error': 'Input text cannot be empty',
                'sources_checked': 0,
                'potential_matches': []
            }
            
        try:
            # Extract key phrases or use first few words
            words = text.split()
            query = ' '.join(words[:10])  # Use first 10 words as search query
            
            # Search online
            search_results = self._google_search(query, max_results)
            if not search_results:
                return {
                    'sources_checked': 0,
                    'potential_matches': [],
                    'note': 'No search results found'
                }
            
            potential_matches = []
            
            for result in search_results:
                time.sleep(self.request_delay)  # Be nice to the API
                
                # Check snippet first (faster than full page)
                snippet_similarity = self.check_plagiarism(text, result['snippet'])
                
                if snippet_similarity['similarity_score'] > self.threshold * 0.7:  # Lower threshold for snippets
                    # If snippet looks promising, check full page
                    page_text = self._extract_text_from_url(result['link'])
                    if page_text:
                        page_similarity = self.check_plagiarism(text, page_text[:10000])  # Check first 10k chars
                        
                        if page_similarity['similarity_score'] > self.threshold:
                            potential_matches.append({
                                'url': result['link'],
                                'title': result['title'],
                                'similarity_score': page_similarity['similarity_score'],
                                'snippet': result['snippet'][:200] + '...'  # Truncate long snippets
                            })
            
            return {
                'sources_checked': len(search_results),
                'potential_matches': sorted(
                    potential_matches, 
                    key=lambda x: x['similarity_score'], 
                    reverse=True
                )[:max_results]  # Return top N matches
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'sources_checked': 0,
                'potential_matches': []
            }

# Initialize a global instance with default settings
plagiarism_detector = PlagiarismDetector()