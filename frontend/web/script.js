// script.js - Frontend script

document.addEventListener("DOMContentLoaded", () => {
    console.log("Yalla Habibi Imports site loaded with Bootstrap!");
});

// Dynamically set the current year
  document.getElementById("year").textContent = new Date().getFullYear();

if (contactForm) { 
     
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        try {
            // Form validation check
            if (!this.checkValidity()) {
                throw new Error('Form validation failed');
            }

            // Simulate form submission 
            alert('Thank you for your message! We will get back to you soon.');

            // Reset form
            this.reset();

        } catch (error) {
            console.error('Submission error:', error);
            alert('There was an error submitting your message. Please try again.');
        }
    });
}