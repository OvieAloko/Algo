const toggleBtn = document.getElementById("navToggle");
const nav = document.querySelector(".nav");

toggleBtn.addEventListener("click", () => {
    nav.classList.toggle("collapsed");
});