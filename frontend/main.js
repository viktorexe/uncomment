class UncommentApp {
    constructor() {
        this.apiBase = '/api';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupTheme();
        this.loadSupportedLanguages();
    }

    setupEventListeners() {
        // Theme toggle
        document.getElementById('theme-toggle').addEventListener('click', () => {
            this.toggleTheme();
        });

        // File upload
        const dropZone = document.getElementById('drop-zone');
        const fileInput = document.getElementById('file-input');

        dropZone.addEventListener('click', () => fileInput.click());
        dropZone.addEventListener('dragover', this.handleDragOver.bind(this));
        dropZone.addEventListener('dragleave', this.handleDragLeave.bind(this));
        dropZone.addEventListener('drop', this.handleDrop.bind(this));
        fileInput.addEventListener('change', this.handleFileSelect.bind(this));

        // Process button
        document.getElementById('process-btn').addEventListener('click', () => {
            this.processCode();
        });

        // Clear input
        document.getElementById('clear-input').addEventListener('click', () => {
            document.getElementById('input-code').value = '';
            this.updateStats();
        });

        // Copy output
        document.getElementById('copy-output').addEventListener('click', () => {
            this.copyToClipboard();
        });

        // Input stats update
        document.getElementById('input-code').addEventListener('input', () => {
            this.updateStats();
        });
    }

    setupTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        if (savedTheme === 'dark') {
            document.documentElement.classList.add('dark');
        }
    }

    toggleTheme() {
        const isDark = document.documentElement.classList.toggle('dark');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    }

    async loadSupportedLanguages() {
        try {
            const response = await fetch(`${this.apiBase}/supported-languages`);
            const data = await response.json();
            
            const select = document.getElementById('language-select');
            select.innerHTML = '';
            
            data.languages.forEach(lang => {
                const option = document.createElement('option');
                option.value = lang;
                option.textContent = lang.charAt(0).toUpperCase() + lang.slice(1);
                select.appendChild(option);
            });
        } catch (error) {
            console.error('Failed to load supported languages:', error);
        }
    }

    handleDragOver(e) {
        e.preventDefault();
        document.getElementById('drop-zone').classList.add('drag-over');
    }

    handleDragLeave(e) {
        e.preventDefault();
        document.getElementById('drop-zone').classList.remove('drag-over');
    }

    handleDrop(e) {
        e.preventDefault();
        document.getElementById('drop-zone').classList.remove('drag-over');
        
        const files = Array.from(e.dataTransfer.files);
        this.processFiles(files);
    }

    handleFileSelect(e) {
        const files = Array.from(e.target.files);
        this.processFiles(files);
    }

    async processFiles(files) {
        if (files.length === 0) return;

        if (files.length === 1) {
            const file = files[0];
            const content = await this.readFileContent(file);
            document.getElementById('input-code').value = content;
            
            // Auto-detect language from file extension
            const extension = file.name.split('.').pop().toLowerCase();
            const languageMap = {
                'py': 'python',
                'js': 'javascript',
                'ts': 'typescript',
                'java': 'java',
                'c': 'c',
                'cpp': 'cpp',
                'cc': 'cpp',
                'cxx': 'cpp',
                'go': 'go',
                'php': 'php',
                'rs': 'rust',
                'rb': 'ruby'
            };
            
            if (languageMap[extension]) {
                document.getElementById('language-select').value = languageMap[extension];
            }
            
            this.updateStats();
        } else {
            // Multiple files - process them all
            await this.processMultipleFiles(files);
        }
    }

    readFileContent(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = e => resolve(e.target.result);
            reader.onerror = reject;
            reader.readAsText(file);
        });
    }

    async processMultipleFiles(files) {
        this.showLoading(true);
        
        try {
            const formData = new FormData();
            files.forEach(file => formData.append('files', file));
            
            const response = await fetch(`${this.apiBase}/process-multiple`, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const results = await response.json();
            this.displayMultipleResults(results);
            
        } catch (error) {
            this.showNotification('Error processing files: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    displayMultipleResults(results) {
        let output = '// Multiple files processed:\n\n';
        
        Object.entries(results).forEach(([filename, result]) => {
            if (result.error) {
                output += `// ERROR in ${filename}: ${result.error}\n\n`;
            } else {
                output += `// File: ${filename} (${result.language})\n`;
                output += `// Original lines: ${result.original_lines}, Cleaned lines: ${result.cleaned_lines}\n`;
                output += `// Processing time: ${result.processing_time.toFixed(3)}s\n\n`;
                output += result.cleaned_code + '\n\n';
                output += '// ' + '='.repeat(50) + '\n\n';
            }
        });
        
        document.getElementById('output-code').value = output;
        this.updateOutputStats();
    }

    async processCode() {
        const code = document.getElementById('input-code').value.trim();
        const language = document.getElementById('language-select').value;
        
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
                    language: language,
                    preserve_structure: true
                })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            
            document.getElementById('output-code').value = result.cleaned_code;
            document.getElementById('processing-time').textContent = 
                `Processed in ${result.processing_time.toFixed(3)}s`;
            
            this.updateOutputStats();
            this.showNotification('Code processed successfully!', 'success');
            
        } catch (error) {
            this.showNotification('Error: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    updateStats() {
        const input = document.getElementById('input-code').value;
        const lines = input ? input.split('\n').length : 0;
        document.getElementById('input-stats').textContent = `${lines} lines`;
    }

    updateOutputStats() {
        const output = document.getElementById('output-code').value;
        const lines = output ? output.split('\n').length : 0;
        document.getElementById('output-stats').textContent = `${lines} lines`;
    }

    async copyToClipboard() {
        const output = document.getElementById('output-code').value;
        
        if (!output) {
            this.showNotification('Nothing to copy', 'error');
            return;
        }
        
        try {
            await navigator.clipboard.writeText(output);
            this.showNotification('Copied to clipboard!', 'success');
        } catch (error) {
            // Fallback for older browsers
            const textarea = document.getElementById('output-code');
            textarea.select();
            document.execCommand('copy');
            this.showNotification('Copied to clipboard!', 'success');
        }
    }

    showLoading(show) {
        const loading = document.getElementById('loading');
        const processBtn = document.getElementById('process-btn');
        
        if (show) {
            loading.classList.remove('hidden');
            processBtn.disabled = true;
            processBtn.textContent = 'Processing...';
        } else {
            loading.classList.add('hidden');
            processBtn.disabled = false;
            processBtn.textContent = 'Remove Comments';
        }
    }

    showNotification(message, type) {
        // Remove existing notifications
        const existing = document.querySelector('.notification');
        if (existing) {
            existing.remove();
        }
        
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        // Hide notification after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new UncommentApp();
});