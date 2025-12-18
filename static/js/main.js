// DOM Elements
const downloadForm = document.getElementById('downloadForm');
const videoUrl = document.getElementById('videoUrl');
const downloadBtn = document.getElementById('downloadBtn');
const progressContainer = document.getElementById('progressContainer');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const resultContainer = document.getElementById('resultContainer');
const resultTitle = document.getElementById('resultTitle');
const resultInfo = document.getElementById('resultInfo');
const downloadFileBtn = document.getElementById('downloadFileBtn');
const errorContainer = document.getElementById('errorContainer');
const errorMessage = document.getElementById('errorMessage');
const loadingOverlay = document.getElementById('loadingOverlay');

// State
let currentDownloadData = null;

// Smooth scroll for navigation
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href');
        const targetSection = document.querySelector(targetId);
        
        if (targetSection) {
            targetSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }

        // Update active state
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        link.classList.add('active');
    });
});

// Hide messages
function hideAllMessages() {
    progressContainer.style.display = 'none';
    resultContainer.style.display = 'none';
    errorContainer.style.display = 'none';
}

// Show error message
function showError(message) {
    hideAllMessages();
    errorMessage.textContent = message;
    errorContainer.style.display = 'block';
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        errorContainer.style.display = 'none';
    }, 5000);
}

// Show progress
function showProgress(text = 'Processing...', progress = 0) {
    hideAllMessages();
    progressContainer.style.display = 'block';
    progressText.textContent = text;
    progressFill.style.width = `${progress}%`;
}

// Show result
function showResult(title, info) {
    hideAllMessages();
    resultContainer.style.display = 'block';
    resultTitle.textContent = title;
    resultInfo.textContent = info;
}

// Show loading overlay
function showLoading() {
    loadingOverlay.classList.add('active');
}

// Hide loading overlay
function hideLoading() {
    loadingOverlay.classList.remove('active');
}

// Validate URL
function validateUrl(url) {
    try {
        const urlObj = new URL(url);
        const validPlatforms = [
            'youtube.com',
            'youtu.be',
            'facebook.com',
            'fb.watch',
            'instagram.com'
        ];
        
        return validPlatforms.some(platform => 
            urlObj.hostname.includes(platform)
        );
    } catch {
        return false;
    }
}

// Detect platform from URL
function detectPlatform(url) {
    if (url.includes('youtube.com') || url.includes('youtu.be')) {
        return 'YouTube';
    } else if (url.includes('facebook.com') || url.includes('fb.watch')) {
        return 'Facebook';
    } else if (url.includes('instagram.com')) {
        return 'Instagram';
    }
    return 'Unknown';
}

// Get platform icon
function getPlatformIcon(platform) {
    const icons = {
        'youtube': 'fab fa-youtube',
        'facebook': 'fab fa-facebook',
        'instagram': 'fab fa-instagram'
    };
    return icons[platform.toLowerCase()] || 'fas fa-video';
}

// Animate button
function animateButton(button, state) {
    if (state === 'loading') {
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Processing...</span>';
    } else if (state === 'success') {
        button.disabled = false;
        button.innerHTML = '<i class="fas fa-check"></i><span>Success!</span>';
        setTimeout(() => {
            button.innerHTML = '<i class="fas fa-download"></i><span>Download</span>';
        }, 2000);
    } else {
        button.disabled = false;
        button.innerHTML = '<i class="fas fa-download"></i><span>Download</span>';
    }
}

// Handle form submission
downloadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const url = videoUrl.value.trim();
    
    // Validate URL
    if (!url) {
        showError('Please enter a video URL');
        return;
    }
    
    if (!validateUrl(url)) {
        showError('Invalid URL. Please enter a valid YouTube, Facebook, or Instagram URL');
        return;
    }
    
    // Start download process
    animateButton(downloadBtn, 'loading');
    showProgress('Fetching video information...', 20);
    
    try {
        // Get video info
        const infoResponse = await fetch('/api/get-info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url })
        });
        
        const infoData = await infoResponse.json();
        
        if (!infoData.success) {
            throw new Error(infoData.error || 'Failed to get video information');
        }
        
        showProgress('Preparing download...', 50);
        
        // Download video
        const downloadResponse = await fetch('/api/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url })
        });
        
        const downloadData = await downloadResponse.json();
        
        if (!downloadData.success) {
            throw new Error(downloadData.error || 'Download failed');
        }
        
        showProgress('Download complete!', 100);
        
        // Store download data
        currentDownloadData = downloadData;
        
        // Show result
        setTimeout(() => {
            const platform = detectPlatform(url);
            const title = downloadData.title || `${platform} Video`;
            showResult(
                'Ready to Download!',
                `Your ${platform} video is ready. Click the button below to download.`
            );
            animateButton(downloadBtn, 'success');
        }, 500);
        
    } catch (error) {
        console.error('Download error:', error);
        showError(error.message || 'An error occurred during download');
        animateButton(downloadBtn, 'reset');
    }
});

// Handle download file button
downloadFileBtn.addEventListener('click', () => {
    if (currentDownloadData && currentDownloadData.filename) {
        // Create download link
        const downloadUrl = `/api/download-file/${currentDownloadData.filename}`;
        
        // Create temporary anchor and trigger download
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = currentDownloadData.filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        // Show success message
        showResult(
            'Download Started!',
            'Your file is being downloaded. Check your downloads folder.'
        );
    }
});

// Input validation with debounce
let validationTimeout;
videoUrl.addEventListener('input', (e) => {
    clearTimeout(validationTimeout);
    
    validationTimeout = setTimeout(() => {
        const url = e.target.value.trim();
        
        if (url) {
            if (validateUrl(url)) {
                videoUrl.style.borderColor = 'var(--success)';
            } else {
                videoUrl.style.borderColor = 'var(--danger)';
            }
        } else {
            videoUrl.style.borderColor = 'var(--border)';
        }
    }, 500);
});

// Clear input on focus
videoUrl.addEventListener('focus', () => {
    hideAllMessages();
});

// Platform badge hover effect
document.querySelectorAll('.platform-badge').forEach(badge => {
    badge.addEventListener('click', () => {
        const platform = badge.querySelector('span').textContent.toLowerCase();
        let exampleUrl = '';
        
        switch(platform) {
            case 'youtube':
                exampleUrl = 'https://www.youtube.com/watch?v=...';
                break;
            case 'facebook':
                exampleUrl = 'https://www.facebook.com/...';
                break;
            case 'instagram':
                exampleUrl = 'https://www.instagram.com/p/...';
                break;
        }
        
        videoUrl.value = exampleUrl;
        videoUrl.focus();
        videoUrl.select();
    });
});

// Intersection Observer for scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe feature cards
document.querySelectorAll('.feature-card, .platform-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// Paste detection
videoUrl.addEventListener('paste', (e) => {
    setTimeout(() => {
        const url = videoUrl.value.trim();
        if (validateUrl(url)) {
            // Show platform detected notification
            const platform = detectPlatform(url);
            showProgress(`${platform} video detected! Click download to continue.`, 0);
            
            setTimeout(() => {
                hideAllMessages();
            }, 3000);
        }
    }, 100);
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + V to focus input
    if ((e.ctrlKey || e.metaKey) && e.key === 'v') {
        if (document.activeElement !== videoUrl) {
            e.preventDefault();
            videoUrl.focus();
        }
    }
    
    // Enter to submit when input is focused
    if (e.key === 'Enter' && document.activeElement === videoUrl) {
        downloadForm.dispatchEvent(new Event('submit'));
    }
    
    // Escape to clear
    if (e.key === 'Escape') {
        videoUrl.value = '';
        hideAllMessages();
        videoUrl.blur();
    }
});

// Copy to clipboard functionality
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Show success notification
        const notification = document.createElement('div');
        notification.textContent = 'Copied to clipboard!';
        notification.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--success);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            box-shadow: var(--shadow-lg);
            z-index: 10000;
            animation: slideInRight 0.3s ease;
        `;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 2000);
    });
}

// Add animation keyframes dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Page load animation
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease';
        document.body.style.opacity = '1';
    }, 100);
});

// Handle online/offline status
window.addEventListener('online', () => {
    showError('Connection restored!');
    setTimeout(() => hideAllMessages(), 2000);
});

window.addEventListener('offline', () => {
    showError('No internet connection. Please check your network.');
});

// Console welcome message
console.log('%c🎥 Video Downloader', 'font-size: 24px; font-weight: bold; color: #6366f1;');
console.log('%cWelcome! Download videos from YouTube, Facebook, and Instagram.', 'font-size: 14px; color: #64748b;');
console.log('%cBuilt with ❤️', 'font-size: 12px; color: #ef4444;');