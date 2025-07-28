from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.comment_processor import CommentProcessor
from backend.language_detector import LanguageDetector

app = Flask(__name__)
CORS(app)


comment_processor = CommentProcessor()
language_detector = LanguageDetector()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process_code():
    try:
        data = request.get_json()
        code = data.get('code', '')
        language = data.get('language', '')
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        

        if not language:
            language = language_detector.detect(code)
        

        result = comment_processor.remove_comments(code, language)
        
        return jsonify({
            'success': True,
            'processed_code': result['code'],
            'detected_language': language,
            'stats': result['stats']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/languages')
def get_supported_languages():
    return jsonify(comment_processor.get_supported_languages())

if __name__ == '__main__':
    app.run(debug=True)