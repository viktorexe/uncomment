from flask import Flask, render_template, request, send_file
import re
import io
import os

app = Flask(__name__)

def remove_comments(code, language):
    if language in ['python']:
        code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
        code = re.sub(r'"""[\s\S]*?"""', '', code)
        code = re.sub(r"'''[\s\S]*?'''", '', code)

    elif language in ['javascript', 'java', 'cpp', 'c', 'csharp']:
        code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        code = re.sub(r'/\*[\s\S]*?\*/', '', code)

    elif language in ['html']:
        code = re.sub(r'<!--[\s\S]*?-->', '', code)

    elif language in ['css']:
        code = re.sub(r'/\*[\s\S]*?\*/', '', code)

    code = re.sub(r'\n\s*\n', '\n\n', code)
    return code.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove_comments', methods=['POST'])
def process_code():
    code = request.form.get('code')
    language = request.form.get('language')
    original_filename = request.form.get('filename', 'processed_code')
    
    if not code or not language:
        return 'Missing code or language selection', 400

    processed_code = remove_comments(code, language)
    
    # Create in-memory file
    mem_file = io.BytesIO()
    mem_file.write(processed_code.encode('utf-8'))
    mem_file.seek(0)
    
    # Determine mime type based on language
    mime_types = {
        'python': 'text/x-python',
        'javascript': 'application/javascript',
        'java': 'text/x-java',
        'cpp': 'text/x-c++',
        'c': 'text/x-c',
        'csharp': 'text/x-csharp',
        'html': 'text/html',
        'css': 'text/css'
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
