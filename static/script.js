// Add fade-in animation to elements
document.addEventListener("DOMContentLoaded", function () {
    const elements = document.querySelectorAll(".fade-in");
    elements.forEach((element) => {
        element.style.opacity = 0;
        setTimeout(() => {
            element.style.opacity = 1;
        }, 100);
    });
});

// Show loading spinner on quiz submission
document.querySelector("form")?.addEventListener("submit", function (e) {
    const button = document.querySelector(".btn");
    if (button) {
        button.innerHTML = `<span class="loader"></span> Processing...`;
        button.disabled = true;
    }
});
