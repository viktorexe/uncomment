class UnCommentApp {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.loadSupportedLanguages();
    }

    initializeElements() {
        this.inputCode = document.getElementById('inputCode');
        this.outputCode = document.getElementById('outputCode');
        this.languageSelect = document.getElementById('language');
        this.processBtn = document.getElementById('processBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.copyBtn = document.getElementById('copyBtn');
        this.fileInput = document.getElementById('fileInput');
        this.stats = document.getElementById('stats');
        this.loadingOverlay = document.getElementById('loadingOverlay');
    }

    bindEvents() {
        this.processBtn.addEventListener('click', () => this.processCode());
        this.clearBtn.addEventListener('click', () => this.clearCode());
        this.copyBtn.addEventListener('click', () => this.copyResult());
        this.fileInput.addEventListener('change', (e) => this.handleFileUpload(e));
        

        this.inputCode.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.processCode();
            }
        });


        this.inputCode.addEventListener('input', () => this.autoResize());
    }

    async loadSupportedLanguages() {
        try {
            const response = await fetch('/api/languages');
            const languages = await response.json();
            

            const autoDetect = this.languageSelect.querySelector('option[value=""]');
            this.languageSelect.innerHTML = '';
            this.languageSelect.appendChild(autoDetect);
            

            languages.forEach(lang => {
                const option = document.createElement('option');
                option.value = lang;
                option.textContent = this.formatLanguageName(lang);
                this.languageSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Failed to load supported languages:', error);
        }
    }

    formatLanguageName(lang) {
        const names = {
            'javascript': 'JavaScript',
            'typescript': 'TypeScript',
            'python': 'Python',
            'java': 'Java',
            'cpp': 'C++',
            'c': 'C',
            'csharp': 'C#',
            'go': 'Go',
            'rust': 'Rust',
            'php': 'PHP',
            'ruby': 'Ruby',
            'swift': 'Swift',
            'kotlin': 'Kotlin',
            'scala': 'Scala',
            'html': 'HTML',
            'css': 'CSS',
            'sql': 'SQL'
        };
        return names[lang] || lang.charAt(0).toUpperCase() + lang.slice(1);
    }

    async processCode() {
        const code = this.inputCode.value.trim();
        if (!code) {
            this.showNotification('Please enter some code to process', 'warning');
            return;
        }

        this.showLoading(true);
        this.processBtn.disabled = true;

        try {
            const response = await fetch('/api/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    code: code,
                    language: this.languageSelect.value
                })
            });

            const result = await response.json();

            if (result.success) {
                this.displayResult(result);
                this.showNotification('Comments removed successfully!', 'success');
            } else {
                throw new Error(result.error || 'Processing failed');
            }
        } catch (error) {
            console.error('Processing error:', error);
            this.showNotification(`Error: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
            this.processBtn.disabled = false;
        }
    }

    displayResult(result) {
        this.outputCode.value = result.processed_code;
        

        this.updateStats(result.stats, result.detected_language);
    }

    getPrismLanguage(lang) {
        const mapping = {
            'javascript': 'javascript',
            'typescript': 'typescript',
            'python': 'python',
            'java': 'java',
            'cpp': 'cpp',
            'c': 'c',
            'csharp': 'csharp',
            'go': 'go',
            'rust': 'rust',
            'php': 'php',
            'ruby': 'ruby',
            'swift': 'swift',
            'kotlin': 'kotlin',
            'scala': 'scala',
            'html': 'html',
            'css': 'css',
            'sql': 'sql'
        };
        return mapping[lang] || 'text';
    }

    updateStats(stats, detectedLanguage) {
        this.stats.innerHTML = `
            <span>Language: ${this.formatLanguageName(detectedLanguage)}</span>
            <span>Comments Removed: ${stats.removed}</span>
        `;
    }

    clearCode() {
        this.inputCode.value = '';
        this.outputCode.value = '';
        this.stats.innerHTML = '';
        this.languageSelect.value = '';
        this.showNotification('Code cleared', 'info');
    }

    async copyResult() {
        const code = this.outputCode.value;
        if (!code) {
            this.showNotification('No code to copy', 'warning');
            return;
        }

        try {
            await navigator.clipboard.writeText(code);
            this.showNotification('Code copied to clipboard!', 'success');
        } catch (error) {
            this.outputCode.select();
            document.execCommand('copy');
            this.showNotification('Code copied to clipboard!', 'success');
        }
    }

    handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;


        if (file.size > 5 * 1024 * 1024) {
            this.showNotification('File too large. Maximum size is 5MB.', 'error');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            this.inputCode.value = e.target.result;
            this.autoDetectLanguage(file.name);
            this.showNotification(`File "${file.name}" loaded successfully`, 'success');
        };
        reader.onerror = () => {
            this.showNotification('Error reading file', 'error');
        };
        reader.readAsText(file);
    }

    autoDetectLanguage(filename) {
        const extension = filename.split('.').pop().toLowerCase();
        const extensionMap = {
            'py': 'python',
            'js': 'javascript',
            'ts': 'typescript',
            'java': 'java',
            'cpp': 'cpp',
            'cc': 'cpp',
            'cxx': 'cpp',
            'c': 'c',
            'cs': 'csharp',
            'go': 'go',
            'rs': 'rust',
            'php': 'php',
            'rb': 'ruby',
            'swift': 'swift',
            'kt': 'kotlin',
            'scala': 'scala',
            'html': 'html',
            'htm': 'html',
            'css': 'css',
            'sql': 'sql'
        };

        const detectedLang = extensionMap[extension];
        if (detectedLang) {
            this.languageSelect.value = detectedLang;
        }
    }

    autoResize() {
        this.inputCode.style.height = 'auto';
        this.inputCode.style.height = Math.max(500, this.inputCode.scrollHeight) + 'px';
    }

    showLoading(show) {
        this.loadingOverlay.classList.toggle('active', show);
    }

    showNotification(message, type = 'info') {

        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        

        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '1rem 1.5rem',
            borderRadius: '0.5rem',
            color: 'white',
            fontWeight: '600',
            zIndex: '1001',
            transform: 'translateX(100%)',
            transition: 'transform 0.3s ease',
            maxWidth: '300px'
        });


        const colors = {
            success: '#059669',
            error: '#dc2626',
            warning: '#d97706',
            info: '#2563eb'
        };
        notification.style.backgroundColor = colors[type] || colors.info;

        document.body.appendChild(notification);


        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);


        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
}


document.addEventListener('DOMContentLoaded', () => {
    new UnCommentApp();
});