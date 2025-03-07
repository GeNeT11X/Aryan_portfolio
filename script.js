// Smooth scrolling for navigation links
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

// Navbar scroll effect
const navbar = document.querySelector('.navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    // Add/remove scrolled class based on scroll position
    if (currentScroll > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }

    // Hide/show navbar based on scroll direction
    if (currentScroll > lastScroll && currentScroll > 100) {
        navbar.style.transform = 'translateY(-100%)';
    } else {
        navbar.style.transform = 'translateY(0)';
    }

    lastScroll = currentScroll;
});

// Mobile menu functionality
const menuBtn = document.querySelector('.menu-btn');
const navItems = document.querySelector('.navbar-items');
const navLinks = document.querySelectorAll('.nav li a');

menuBtn.addEventListener('click', () => {
    navItems.classList.toggle('h-class');
    navItems.classList.toggle('v-class');
    menuBtn.classList.toggle('active');
});

// Close mobile menu when clicking a link
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navItems.classList.add('h-class');
        navItems.classList.remove('v-class');
        menuBtn.classList.remove('active');
    });
});

// Portfolio filtering functionality
const filterButtons = document.querySelectorAll('.filter-btn');
const portfolioItems = document.querySelectorAll('.portfolio-item');

filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Remove active class from all buttons
        filterButtons.forEach(btn => btn.classList.remove('active'));
        // Add active class to clicked button
        button.classList.add('active');

        const filterValue = button.getAttribute('data-filter');

        portfolioItems.forEach(item => {
            if (filterValue === 'all' || item.getAttribute('data-category') === filterValue) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    });
});

// Form validation and submission
const contactForm = document.querySelector('.contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get form elements
        const submitBtn = this.querySelector('.submit-btn');
        const nameInput = this.querySelector('input[type="text"]');
        const emailInput = this.querySelector('input[type="email"]');
        const phoneInput = this.querySelector('input[type="tel"]');
        const serviceInput = this.querySelector('select');
        const messageInput = this.querySelector('textarea');

        // Basic form validation
        const name = nameInput.value.trim();
        const email = emailInput.value.toLowerCase().trim();
        const phone = phoneInput.value.trim();
        const service = serviceInput.value;
        const message = messageInput.value.trim();

        // Validate all required fields
        if (!name || !email || !service || !message) {
            alert('Please fill in all required fields');
            return;
        }

        // Email validation
        const emailRegex = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/;
        if (!emailRegex.test(email)) {
            alert('Please enter a valid email address');
            emailInput.focus();
            return;
        }

        // Phone validation (if provided)
        if (phone) {
            const phoneRegex = /^\+?[\d\s-()]{10,}$/;
            if (!phoneRegex.test(phone)) {
                alert('Please enter a valid phone number');
                phoneInput.focus();
                return;
            }
        }

        try {
            // Disable submit button and show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

            // Prepare form data
            const formData = {
                name: name,
                email: email,
                phone: phone,
                service: service,
                message: message
            };

            // Send data to backend
            const response = await fetch('/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (result.success) {
                alert(result.message);
                this.reset();
            } else {
                throw new Error(result.message);
            }
        } catch (error) {
            alert('Sorry, there was an error sending your message. Please try again.');
            console.error('Form submission error:', error);
        } finally {
            // Reset submit button
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Send Message';
        }
    });
}

// Animate elements on scroll
const animateOnScroll = () => {
    const elements = document.querySelectorAll('.animate-on-scroll');
    
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementBottom = element.getBoundingClientRect().bottom;
        
        if (elementTop < window.innerHeight && elementBottom > 0) {
            element.classList.add('animated');
        }
    });
};

window.addEventListener('scroll', animateOnScroll);
window.addEventListener('load', animateOnScroll);

// Image lazy loading
document.addEventListener('DOMContentLoaded', () => {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
});

// Portfolio image hover effect
const portfolioImages = document.querySelectorAll('.portfolio-image');
portfolioImages.forEach(image => {
    image.addEventListener('mouseenter', () => {
        image.style.transform = 'scale(1.05)';
    });
    
    image.addEventListener('mouseleave', () => {
        image.style.transform = 'scale(1)';
    });
});

// Add loading animation to page
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
}); 