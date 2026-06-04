// Smooth scroll behavior for navigation
document.querySelectorAll('a[href^="/"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        // Don't prevent default for actual navigation
        const href = this.getAttribute('href');
        if (href.startsWith('/#')) {
            e.preventDefault();
            const target = document.querySelector(href.substring(1));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// Set active nav link based on current page
function setActiveNavLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// Call on page load
document.addEventListener('DOMContentLoaded', setActiveNavLink);

// Add animation class to elements as they come into view
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all cards
document.querySelectorAll('.stat-card, .about-card, .step').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Form validation feedback
document.querySelectorAll('input, select').forEach(field => {
    field.addEventListener('blur', function() {
        if (this.hasAttribute('required') && !this.value) {
            this.style.borderColor = '#ef4444';
        } else {
            this.style.borderColor = 'rgba(6, 182, 212, 0.3)';
        }
    });
    
    field.addEventListener('focus', function() {
        this.style.borderColor = '#06b6d4';
    });
});
