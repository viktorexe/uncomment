from flask import Flask, request, jsonify
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.comment_processor import CommentProcessor
from backend.language_detector import LanguageDetector

app = Flask(__name__)

# Initialize processors
comment_processor = CommentProcessor()
language_detector = LanguageDetector()

def handler(request):
    """Vercel serverless function handler"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            code = data.get('code', '')
            language = data.get('language', '')
            
            if not code:
                return jsonify({'error': 'No code provided'}), 400
            
            # Auto-detect language if not provided
            if not language:
                language = language_detector.detect(code)
            
            # Process the code
            result = comment_processor.remove_comments(code, language)
            
            return jsonify({
                'success': True,
                'processed_code': result['code'],
                'detected_language': language,
                'stats': result['stats']
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Method not allowed'}), 405