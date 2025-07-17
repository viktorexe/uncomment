document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('codeForm');
    const fileInput = document.getElementById('fileInput');
    const codeInput = document.getElementById('codeInput');
    const languageSelect = document.getElementById('language');
    const copyBtn = document.getElementById('copyBtn');
    const themeToggle = document.getElementById('themeToggle');
    const lineNumbers = document.getElementById('lineNumbers');
    let originalFilename = '';

    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            originalFilename = file.name;
            const reader = new FileReader();
            reader.onload = function(e) {
                codeInput.value = e.target.result;
                
                const extension = file.name.split('.').pop().toLowerCase();
                const languageMap = {
                    'py': 'python',
                    'js': 'javascript',
                    'ts': 'typescript',
                    'java': 'java',
                    'cpp': 'cpp',
                    'c': 'c',
                    'cs': 'csharp',
                    'html': 'html',
                    'css': 'css',
                    'scss': 'scss',
                    'less': 'less',
                    'rb': 'ruby',
                    'kt': 'kotlin',
                    'swift': 'swift',
                    'dart': 'dart',
                    'go': 'go',
                    'rs': 'rust',
                    'php': 'php',
                    'sql': 'sql',
                    'ps1': 'powershell',
                    'yaml': 'yaml',
                    'yml': 'yaml'
                };
                
                if (languageMap[extension]) {
                    languageSelect.value = languageMap[extension];
                }
            };
            reader.readAsText(file);
        }
    });

    // Analyze code before submission
    codeInput.addEventListener('input', debounce(function() {
        if (codeInput.value.length > 100 && languageSelect.value) {
            const analyzeData = new FormData();
            analyzeData.append('code', codeInput.value);
            analyzeData.append('language', languageSelect.value);
            
            fetch('/api/analyze', {
                method: 'POST',
                body: analyzeData
            })
            .then(response => response.json())
            .then(data => {
                // Could show a preview of analysis here
                console.log('Analysis:', data);
                
                // Optional: Show a notification with the analysis
                if (data.comment_lines > 0) {
                    showNotification(`Found ${data.comment_lines} comments. Estimated reduction: ${data.estimated_reduction}`, 'info');
                }
            })
            .catch(err => console.error('Analysis error:', err));
        }
    }, 1000)); // Debounce to avoid too many requests
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading state
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.innerHTML = `
            <div class="loading-spinner"></div>
            Processing...
        `;
        submitBtn.disabled = true;
        
        const formData = new FormData(form);
        // Add the original filename to the form data
        formData.append('filename', originalFilename || `processed_code.${languageSelect.value}`);
        
        fetch('/remove_comments', {
            method: 'POST',
            body: formData
        })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = originalFilename || `processed_code.${languageSelect.value}`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();
            
            // Show success notification
            showNotification('Code processed successfully!', 'success');
            
            // Reset button state
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('An error occurred while processing the code.', 'error');
            
            // Reset button state
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;
        });
    });

    // Line numbers functionality
    function updateLineNumbers() {
        const lines = codeInput.value.split('\n').length;
        let lineNumbersHTML = '';
        for (let i = 1; i <= lines; i++) {
            lineNumbersHTML += `${i}<br>`;
        }
        lineNumbers.innerHTML = lineNumbersHTML;
    }

    // Update line numbers on input
    codeInput.addEventListener('input', updateLineNumbers);
    codeInput.addEventListener('scroll', function() {
        lineNumbers.scrollTop = codeInput.scrollTop;
    });

    // Initialize line numbers
    updateLineNumbers();

    // Copy button functionality
    copyBtn.addEventListener('click', function() {
        codeInput.select();
        document.execCommand('copy');
        
        // Show feedback
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
        `;
        copyBtn.style.color = 'var(--success)';
        
        setTimeout(() => {
            copyBtn.innerHTML = originalText;
            copyBtn.style.color = '';
        }, 2000);
    });

    // Theme toggle functionality
    themeToggle.addEventListener('click', function() {
        document.documentElement.classList.toggle('light-theme');
        
        // Update icon based on theme
        if (document.documentElement.classList.contains('light-theme')) {
            themeToggle.innerHTML = `
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                </svg>
            `;
        } else {
            themeToggle.innerHTML = `
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="5"></circle>
                    <line x1="12" y1="1" x2="12" y2="3"></line>
                    <line x1="12" y1="21" x2="12" y2="23"></line>
                    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                    <line x1="1" y1="12" x2="3" y2="12"></line>
                    <line x1="21" y1="12" x2="23" y2="12"></line>
                    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
                </svg>
            `;
        }
    });

    // Tab key handling in textarea
    codeInput.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            e.preventDefault();
            const start = this.selectionStart;
            const end = this.selectionEnd;
            
            // Insert tab at cursor position
            this.value = this.value.substring(0, start) + '    ' + this.value.substring(end);
            
            // Move cursor after the inserted tab
            this.selectionStart = this.selectionEnd = start + 4;
            
            // Update line numbers
            updateLineNumbers();
        }
    });
});
// Function to highlight code
function highlightCode(code, language) {
    if (!Prism.languages[language]) {
        return code; // Return plain code if language not supported
    }
    
    const highlightedCode = Prism.highlight(
        code,
        Prism.languages[language],
        language
    );
    return highlightedCode;
}

// Debounce function to limit how often a function can be called
function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            func.apply(context, args);
        }, wait);
    };
}

// Function to show a notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateY(0)';
        notification.style.opacity = '1';
    }, 10);
    
    // Remove after delay
    setTimeout(() => {
        notification.style.transform = 'translateY(-20px)';
        notification.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}
document.addEventListener('DOMContentLoaded', function() {
    const mobileWarning = document.querySelector('.mobile-warning');
    
    function checkDevice() {
        // Check if device is mobile based on screen width and user agent
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) 
            && window.innerWidth <= 768;
            
        if (isMobile) {
            mobileWarning.style.display = 'block';
            document.body.style.overflow = 'hidden';
        } else {
            mobileWarning.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }

    // Check on load
    checkDevice();
    
    // Check on resize
    window.addEventListener('resize', checkDevice);
    
    // Optional: Allow users to dismiss the warning
    mobileWarning.addEventListener('click', function() {
        this.style.display = 'none';
        document.body.style.overflow = 'auto';
    });
    
    // Add notification styles dynamically
    const style = document.createElement('style');
    style.textContent = `
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            background: var(--accents-1);
            color: var(--foreground);
            border-left: 4px solid var(--primary);
            border-radius: var(--radius);
            box-shadow: var(--shadow-md);
            z-index: 1000;
            transform: translateY(-20px);
            opacity: 0;
            transition: all 0.3s ease;
        }
        
        .notification.success {
            border-left-color: var(--success);
        }
        
        .notification.error {
            border-left-color: var(--error);
        }
        
        .notification.warning {
            border-left-color: var(--warning);
        }
    `;
    document.head.appendChild(style);
});
