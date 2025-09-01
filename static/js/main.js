// Main JavaScript for Notebook Hub Dashboard

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeSidebar();
    initializeSearch();
    initializeViewToggle();
    initializeFlashMessages();
    initializeDashboardCharts();
    
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Sidebar Functions
function initializeSidebar() {
    // Handle upload button click
    const uploadBtn = document.querySelector('.upload-btn');
    if (uploadBtn) {
        uploadBtn.addEventListener('click', function() {
            window.location.href = '/upload';
        });
    }
    
    // Handle category and tag checkboxes
    document.querySelectorAll('.category-item, .tag-item').forEach(item => {
        item.addEventListener('change', function() {
            // TODO: Implement filtering logic
            console.log('Filter changed:', this.querySelector('span').textContent);
        });
    });
}

// Search Functions
function initializeSearch() {
    const searchInput = document.querySelector('.search-input input');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length >= 2) {
                searchTimeout = setTimeout(() => {
                    performSearch(query);
                }, 300);
            }
        });
        
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch(this.value.trim());
            }
        });
    }
}

function performSearch(query) {
    // TODO: Implement actual search functionality
    console.log('Searching for:', query);
    // Redirect to search page or perform AJAX search
    if (query) {
        window.location.href = `/search?q=${encodeURIComponent(query)}`;
    }
}

// View Toggle Functions
function initializeViewToggle() {
    const viewBtns = document.querySelectorAll('.view-btn');
    const notebooksContainer = document.getElementById('notebooksContainer');
    
    if (viewBtns.length && notebooksContainer) {
        viewBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const viewType = this.getAttribute('data-view');
                
                // Update active button
                viewBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                // Toggle view
                if (viewType === 'list') {
                    notebooksContainer.style.gridTemplateColumns = '1fr';
                } else {
                    notebooksContainer.style.gridTemplateColumns = 'repeat(auto-fill, minmax(300px, 1fr))';
                }
            });
        });
    }
}

// Flash Message Functions
function initializeFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        const closeBtn = message.querySelector('.flash-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                message.remove();
            });
        }
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (message.parentNode) {
                message.remove();
            }
        }, 5000);
    });
}

// Utility Functions
function showNotification(message, type = 'info') {
    // Create a simple notification
    const notification = document.createElement('div');
    notification.className = `flash-message flash-${type}`;
    notification.innerHTML = `
        ${message}
        <button class="flash-close">&times;</button>
    `;
    
    const flashContainer = document.querySelector('.flash-messages') || document.body;
    flashContainer.appendChild(notification);
    
    // Initialize the new flash message
    initializeFlashMessages();
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 1) {
        return 'Yesterday';
    } else if (diffDays < 7) {
        return `${diffDays} days ago`;
    } else {
        return date.toLocaleDateString();
    }
}

// API Functions
async function likeNotebook(notebookId) {
    try {
        // TODO: Implement actual like functionality
        showNotification('Like functionality coming soon!', 'info');
    } catch (error) {
        console.error('Error liking notebook:', error);
        showNotification('Error liking notebook', 'danger');
    }
}

async function downloadNotebook(notebookId) {
    try {
        // TODO: Implement actual download functionality
        showNotification('Download functionality coming soon!', 'info');
    } catch (error) {
        console.error('Error downloading notebook:', error);
        showNotification('Error downloading notebook', 'danger');
    }
}

// Keyboard Shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for search focus
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('.search-input input');
        if (searchInput) {
            searchInput.focus();
        }
    }
});

// Performance Optimization
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Initialize lazy loading
if ('IntersectionObserver' in window) {
    lazyLoadImages();
}

// Service Worker Registration (for PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Dashboard Charts Functions
function initializeDashboardCharts() {
    // Only initialize if we're on the dashboard page
    if (document.getElementById('marketCapChart')) {
        createMarketCapChart();
        createAdoptionChart();
        createStablecoinChart();
        initializeChartButtons();
    }
}

function createMarketCapChart() {
    const ctx = document.getElementById('marketCapChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['USDT', 'USDC', 'BUSD', 'DAI', 'Other'],
            datasets: [{
                data: [45, 25, 15, 10, 5],
                backgroundColor: [
                    '#26A69A',
                    '#2196F3',
                    '#FFC107',
                    '#4CAF50',
                    '#9E9E9E'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                }
            }
        }
    });
}

function createAdoptionChart() {
    const ctx = document.getElementById('adoptionChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['2020', '2021', '2022', '2023', '2024', '2025'],
            datasets: [{
                label: 'CBDC Projects',
                data: [12, 25, 45, 67, 78, 87],
                borderColor: '#2196F3',
                backgroundColor: 'rgba(33, 150, 243, 0.1)',
                tension: 0.4,
                fill: true
                }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        display: false
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function createStablecoinChart() {
    const ctx = document.getElementById('stablecoinChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['USDT', 'USDC', 'BUSD', 'DAI'],
            datasets: [{
                label: 'Market Cap ($B)',
                data: [95.2, 52.8, 15.6, 8.4],
                backgroundColor: [
                    '#26A69A',
                    '#2196F3',
                    '#FFC107',
                    '#4CAF50'
                ],
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        display: false
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function initializeChartButtons() {
    const chartBtns = document.querySelectorAll('.chart-btn');
    chartBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active class from all buttons
            chartBtns.forEach(b => b.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
            
            // TODO: Implement chart switching logic
            console.log('Switching to:', this.getAttribute('data-chart'));
        });
    });
}
