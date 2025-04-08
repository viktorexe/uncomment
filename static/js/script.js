document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('codeForm');
    const fileInput = document.getElementById('fileInput');
    const codeInput = document.getElementById('codeInput');
    const languageSelect = document.getElementById('language');
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
                    'java': 'java',
                    'cpp': 'cpp',
                    'c': 'c',
                    'cs': 'csharp',
                    'html': 'html',
                    'css': 'css'
                };
                
                if (languageMap[extension]) {
                    languageSelect.value = languageMap[extension];
                }
            };
            reader.readAsText(file);
        }
    });

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
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
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while processing the code.');
        });
    });

    // Rest of your code (language grid population) remains the same...
});
// Add this to your existing script.js
function highlightCode(code, language) {
    const highlightedCode = Prism.highlight(
        code,
        Prism.languages[language],
        language
    );
    return highlightedCode;
}

// Modify your file input handler
fileInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        originalFilename = file.name;
        const reader = new FileReader();
        reader.onload = function(e) {
            const code = e.target.result;
            codeInput.value = code;
            
            const extension = file.name.split('.').pop().toLowerCase();
            const languageMap = {
                'py': 'python',
                'js': 'javascript',
                'java': 'java',
                'cpp': 'cpp',
                'c': 'c',
                'cs': 'csharp',
                'html': 'html',
                'css': 'css'
            };
            
            if (languageMap[extension]) {
                const language = languageMap[extension];
                languageSelect.value = language;
                
                // Create a pre and code element for syntax highlighting
                const pre = document.createElement('pre');
                const codeElement = document.createElement('code');
                codeElement.className = `language-${language}`;
                codeElement.innerHTML = highlightCode(code, language);
                pre.appendChild(codeElement);
                
                // Replace textarea with highlighted code
                codeInput.parentNode.replaceChild(pre, codeInput);
            }
        };
        reader.readAsText(file);
    }
});
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
});
