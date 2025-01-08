document.addEventListener("DOMContentLoaded", function () {
    const videoContainers = document.querySelectorAll(".video-container");

    videoContainers.forEach((container) => {
        const video = container.querySelector("video");

        if (video) {
            // Play video on hover
            container.addEventListener("mouseenter", () => video.play());
            container.addEventListener("mouseleave", () => video.pause());
        } else {
            // Remove hover effects for containers without video
            container.classList.remove("has-video");
        }
    });
});


feather.replace();


function applySorting() {
    const sortValue = document.getElementById('sort_by').value;
    const urlParams = new URLSearchParams(window.location.search);
    const brand = urlParams.get('brand') || 'All';
    const newUrl = `?brand=${brand}&sort_by=${sortValue}`;
    window.location.href = newUrl;
}