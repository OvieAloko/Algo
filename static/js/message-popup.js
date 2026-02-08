document.addEventListener("DOMContentLoaded", function() {
    const alerts = document.querySelectorAll(".auth-message .alert");

    alerts.forEach(alert => {
        setTimeout(() => alert.classList.add("show"), 50);
        setTimeout(() => alert.classList.add("hide"), 5000);
    });
});