// Slider and Icon Initialization

document.addEventListener('DOMContentLoaded', function () {
    // Slider Logic
    const slides = document.querySelectorAll('.slider-slide');
    let currentIndex = 0;
    const intervalTime = 15000; // 15 seconds

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.toggle('hidden', i !== index);
        });
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % slides.length;
        showSlide(currentIndex);
    }

    showSlide(currentIndex);
    const interval = setInterval(nextSlide, intervalTime);

    // Add click event to videos to pause automatic sliding
    slides.forEach((slide, index) => {
        const video = slide.querySelector('video');
        video.addEventListener('click', () => {
            clearInterval(interval); // Stop the automatic sliding
            currentIndex = (index + 1) % slides.length;
            showSlide(currentIndex);
        });
    });

    // Icon Initialization
    function initIcons() {
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }

    // Initialize icons on page load
    initIcons();
});