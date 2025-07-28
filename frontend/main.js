class CommentRemover {
    constructor() {
        this.apiBase = '/api/v1';
        this.isDarkMode = true;
        this.initializeElements();
        this.attachEventListeners();
        this.loadSupportedLanguages();
    }

    initializeElements() {
        this.elements = {
            languageSelect: document.getElementById('languageSelect'),
            processBtn: document.getElementById('processBtn'),
            inputCode: document.getElementById('inputCode'),
            outputCode: document.getElementById('outputCode'),
            dropZone: document.getElementById('dropZone'),
            fileInput: document.getElementById('fileInput'),
            copyBtn: document.getElementById('copyBtn'),
            downloadBtn: document.getElementById('downloadBtn'),
            themeToggle: document.getElementById('themeToggle'),
            loading: document.getElementById('loading'),
            originalLines: document.getElementById('originalLines'),
            processedLines: document.getElementById('processedLines')
        };
    }

    attachEventListeners() {
        this.elements.processBtn.addEventListener('click', () => this.processCode());
        this.elements.copyBtn.addEventListener('click', () => this.copyToClipboard());
        this.elements.downloadBtn.addEventListener('click', () => this.downloadCode());
        this.elements.themeToggle.addEventListener('click', () => this.toggleTheme());
        
        // File handling
        this.elements.dropZone.addEventListener('click', () => this.elements.fileInput.click());
        this.elements.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        
        // Drag and drop
        this.elements.dropZone.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.elements.dropZone.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.elements.dropZone.addEventListener('drop', (e) => this.handleDrop(e));
        
        // Auto-process on input change
        this.elements.inputCode.addEventListener('input', () => this.updateStats());
    }

    async loadSupportedLanguages() {
        try {
            const response = await fetch(`${this.apiBase}/languages`);
            const data = await response.json();
            
            this.elements.languageSelect.innerHTML = '';
            data.languages.forEach(lang => {
                const option = document.createElement('option');
                option.value = lang;
                option.textContent = lang.charAt(0).toUpperCase() + lang.slice(1);
                this.elements.languageSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Failed to load languages:', error);
        }
    }

    async processCode() {
        const code = this.elements.inputCode.value.trim();
        if (!code) {
            this.showNotification('Please enter some code to process', 'error');
            return;
        }

        this.showLoading(true);
        
        try {
            const response = await fetch(`${this.apiBase}/process`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    code: code,
                    language: this.elements.languageSelect.value,
                    preserve_structure: true
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            this.elements.outputCode.value = result.processed_code;
            this.elements.originalLines.textContent = result.original_lines;
            this.elements.processedLines.textContent = result.processed_lines;
            
            this.showNotification('Code processed successfully!', 'success');
            
        } catch (error) {
            console.error('Processing error:', error);
            this.showNotification('Failed to process code. Please try again.', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    handleFileSelect(event) {
        const files = Array.from(event.target.files);
        if (files.length > 0) {
            this.processFiles(files);
        }
    }

    handleDragOver(event) {
        event.preventDefault();
        this.elements.dropZone.classList.add('drag-over');
    }

    handleDragLeave(event) {
        event.preventDefault();
        this.elements.dropZone.classList.remove('drag-over');
    }

    handleDrop(event) {
        event.preventDefault();
        this.elements.dropZone.classList.remove('drag-over');
        
        const files = Array.from(event.dataTransfer.files);
        if (files.length > 0) {
            this.processFiles(files);
        }
    }

    async processFiles(files) {
        if (files.length === 1) {
            const file = files[0];
            const content = await this.readFileContent(file);
            this.elements.inputCode.value = content;
            
            // Auto-detect language from file extension
            const extension = file.name.split('.').pop().toLowerCase();
            const languageMap = {
                'py': 'python',
                'js': 'javascript',
                'ts': 'typescript',
                'java': 'java',
                'cpp': 'cpp',
                'c': 'c',
                'go': 'go',
                'php': 'php',
                'rs': 'rust',
                'rb': 'ruby'
            };
            
            if (languageMap[extension]) {
                this.elements.languageSelect.value = languageMap[extension];
            }
            
            this.updateStats();
            this.showNotification(`Loaded ${file.name}`, 'success');
        }
    }

    readFileContent(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = (e) => reject(e);
            reader.readAsText(file);
        });
    }

    copyToClipboard() {
        const output = this.elements.outputCode.value;
        if (!output) {
            this.showNotification('No processed code to copy', 'error');
            return;
        }

        navigator.clipboard.writeText(output).then(() => {
            this.showNotification('Code copied to clipboard!', 'success');
        }).catch(() => {
            this.showNotification('Failed to copy code', 'error');
        });
    }

    downloadCode() {
        const output = this.elements.outputCode.value;
        if (!output) {
            this.showNotification('No processed code to download', 'error');
            return;
        }

        const language = this.elements.languageSelect.value;
        const extensions = {
            'python': 'py',
            'javascript': 'js',
            'typescript': 'ts',
            'java': 'java',
            'cpp': 'cpp',
            'c': 'c',
            'go': 'go',
            'php': 'php',
            'rust': 'rs',
            'ruby': 'rb'
        };

        const extension = extensions[language] || 'txt';
        const filename = `processed_code.${extension}`;

        const blob = new Blob([output], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        this.showNotification(`Downloaded ${filename}`, 'success');
    }

    toggleTheme() {
        this.isDarkMode = !this.isDarkMode;
        document.body.classList.toggle('light-mode', !this.isDarkMode);
        this.elements.themeToggle.textContent = this.isDarkMode ? '🌙 Dark Mode' : '☀️ Light Mode';
    }

    updateStats() {
        const code = this.elements.inputCode.value;
        const lines = code.split('\n').filter(line => line.trim()).length;
        this.elements.originalLines.textContent = lines;
    }

    showLoading(show) {
        this.elements.loading.classList.toggle('hidden', !show);
    }

    showNotification(message, type) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 px-6 py-3 rounded-lg text-white z-50 ${
            type === 'success' ? 'bg-green-600' : 'bg-red-600'
        }`;
        notification.textContent = message;

        document.body.appendChild(notification);

        // Remove after 3 seconds
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 3000);
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new CommentRemover();
});