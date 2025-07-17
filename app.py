from flask import Flask, render_template, request, send_file, jsonify
import re
import io
import os
import time
import hashlib

app = Flask(__name__)

def remove_comments(code, language):
    """
    Remove comments from code based on language.
    Preserves string literals to avoid removing comment-like content inside strings.
    """
    # Save strings to prevent comment removal inside string literals
    strings = {}
    string_count = 0
    
    def preserve_strings(match):
        nonlocal string_count
        placeholder = f"__STRING_PLACEHOLDER_{string_count}__"
        strings[placeholder] = match.group(0)
        string_count += 1
        return placeholder
    
    # Handle language-specific string patterns before removing comments
    if language in ['python', 'javascript', 'typescript', 'java', 'ruby', 'php']:
        # Preserve string literals
        code = re.sub(r'"(?:\\"|[^"])*?"|\'(?:\\\'|[^\'])*?\'', preserve_strings, code)
    
    # Now remove comments based on language
    if language in ['python']:
        # Handle docstrings first (triple quotes)
        code = re.sub(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'', '', code)
        # Then handle single line comments
        code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)

    elif language in ['javascript', 'typescript', 'java', 'cpp', 'c', 'csharp', 'kotlin', 'swift', 'dart', 'go', 'rust', 'php']:
        # Handle multi-line comments first
        code = re.sub(r'/\*[\s\S]*?\*/', '', code)
        # Then handle single line comments
        code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)

    elif language in ['html']:
        code = re.sub(r'<!--[\s\S]*?-->', '', code)

    elif language in ['css', 'scss', 'less']:
        code = re.sub(r'/\*[\s\S]*?\*/', '', code)
        # For SCSS/LESS single line comments
        if language in ['scss', 'less']:
            code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
            
    elif language in ['ruby']:
        code = re.sub(r'=begin[\s\S]*?=end', '', code)
        code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
        
    elif language in ['sql']:
        code = re.sub(r'/\*[\s\S]*?\*/', '', code)
        code = re.sub(r'--.*$', '', code, flags=re.MULTILINE)
        
    elif language in ['powershell']:
        code = re.sub(r'<#[\s\S]*?#>', '', code)
        code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
        
    elif language in ['yaml']:
        code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
        
    # Restore preserved strings
    for placeholder, string in strings.items():
        code = code.replace(placeholder, string)
    
    # Clean up excessive newlines
    code = re.sub(r'\n\s*\n', '\n\n', code)
    return code.strip()

def count_comments(code, language):
    """Count comments in code based on language"""
    comment_count = 0
    if language == 'python':
        comment_count = len(re.findall(r'#.*$|"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'', code))
    elif language in ['javascript', 'typescript', 'java', 'cpp', 'c', 'csharp', 'kotlin', 'swift', 'dart', 'go', 'rust', 'php']:
        comment_count = len(re.findall(r'//.*$|/\*[\s\S]*?\*/', code))
    elif language in ['html']:
        comment_count = len(re.findall(r'<!--[\s\S]*?-->', code))
    elif language in ['css', 'scss', 'less']:
        multi_line = len(re.findall(r'/\*[\s\S]*?\*/', code))
        single_line = 0
        if language in ['scss', 'less']:
            single_line = len(re.findall(r'//.*$', code, flags=re.MULTILINE))
        comment_count = multi_line + single_line
    elif language in ['ruby']:
        multi_line = len(re.findall(r'=begin[\s\S]*?=end', code))
        single_line = len(re.findall(r'#.*$', code, flags=re.MULTILINE))
        comment_count = multi_line + single_line
    elif language in ['sql']:
        multi_line = len(re.findall(r'/\*[\s\S]*?\*/', code))
        single_line = len(re.findall(r'--.*$', code, flags=re.MULTILINE))
        comment_count = multi_line + single_line
    elif language in ['powershell']:
        multi_line = len(re.findall(r'<#[\s\S]*?#>', code))
        single_line = len(re.findall(r'#.*$', code, flags=re.MULTILINE))
        comment_count = multi_line + single_line
    elif language in ['yaml']:
        comment_count = len(re.findall(r'#.*$', code, flags=re.MULTILINE))
    return comment_count

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Return statistics about code processing"""
    stats = {
        'processed_files': 0,  # In a real app, you'd track this
        'supported_languages': 20,
        'server_time': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(stats)

@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    """Analyze code without removing comments"""
    code = request.form.get('code')
    language = request.form.get('language')
    
    if not code or not language:
        return jsonify({'error': 'Missing code or language selection'}), 400
    
    # Count lines and comments
    total_lines = len(code.split('\n'))
    comment_count = count_comments(code, language)
    
    # Generate a hash of the code for caching purposes
    code_hash = hashlib.md5(code.encode()).hexdigest()
    
    analysis = {
        'total_lines': total_lines,
        'comment_lines': comment_count,
        'code_hash': code_hash,
        'language': language,
        'estimated_reduction': f"{(comment_count/total_lines)*100:.1f}%" if total_lines > 0 else "0%"
    }
    
    return jsonify(analysis)

@app.route('/remove_comments', methods=['POST'])
def process_code():
    code = request.form.get('code')
    language = request.form.get('language')
    original_filename = request.form.get('filename', 'processed_code')
    format_option = request.form.get('format', 'download')  # New parameter for response format
    
    if not code or not language:
        return 'Missing code or language selection', 400

    # Process the code
    processed_code = remove_comments(code, language)
    
    # If JSON response is requested
    if format_option == 'json':
        return jsonify({
            'original_size': len(code),
            'processed_size': len(processed_code),
            'reduction_percentage': f"{((len(code) - len(processed_code)) / len(code) * 100):.1f}%" if len(code) > 0 else "0%",
            'processed_code': processed_code
        })
    
    # Default: return as downloadable file
    mem_file = io.BytesIO()
    mem_file.write(processed_code.encode('utf-8'))
    mem_file.seek(0)
    
    # Determine mime type based on language
    mime_types = {
        'python': 'text/x-python',
        'javascript': 'application/javascript',
        'typescript': 'application/typescript',
        'java': 'text/x-java',
        'cpp': 'text/x-c++',
        'c': 'text/x-c',
        'csharp': 'text/x-csharp',
        'html': 'text/html',
        'css': 'text/css',
        'scss': 'text/x-scss',
        'less': 'text/x-less',
        'ruby': 'text/x-ruby',
        'kotlin': 'text/x-kotlin',
        'swift': 'text/x-swift',
        'dart': 'text/x-dart',
        'go': 'text/x-go',
        'rust': 'text/x-rust',
        'php': 'text/x-php',
        'sql': 'text/x-sql',
        'powershell': 'text/x-powershell',
        'yaml': 'text/x-yaml'
    }
    
    mime_type = mime_types.get(language, 'text/plain')
    
    return send_file(
        mem_file,
        as_attachment=True,
        download_name=original_filename,
        mimetype=mime_type
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')