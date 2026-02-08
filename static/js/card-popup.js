const emailchangepopupWrapper = document.getElementById("email-change-card");
const changeEmailBtn = document.getElementById("change-email");

const passwordchangepopupWrapper = document.getElementById("password-change-card");
const changePasswordBtn = document.getElementById("change-password");

const deleteAccountWrapper = document.getElementById("account-deletion-card");
const deleteAccountBtn = document.getElementById("delete-account");

changeEmailBtn.addEventListener("click", (e) => {
    e.preventDefault();
    emailchangepopupWrapper.classList.add("show");
    window.location.hash = "#email-change-card";
});

emailchangepopupWrapper.addEventListener("click", (e) => {
    if (e.target === emailchangepopupWrapper) {
        emailchangepopupWrapper.classList.remove("show");
        history.replaceState(null, null, " ");
    }
});

changePasswordBtn.addEventListener("click", (e) => {
    e.preventDefault();
    passwordchangepopupWrapper.classList.add("show"); 
    window.location.hash = "#password-change-card";

});

passwordchangepopupWrapper.addEventListener("click", (e) => {
    if (e.target === passwordchangepopupWrapper) {
        passwordchangepopupWrapper.classList.remove("show");
        history.replaceState(null, null, " ");
    }
});

deleteAccountBtn.addEventListener("click", (e) => {
    e.preventDefault();
    deleteAccountWrapper.classList.add("show"); 
    window.location.hash = "#delete-account";

});

deleteAccountWrapper.addEventListener("click", (e) => {
    if (e.target === deleteAccountWrapper) {
        deleteAccountWrapper.classList.remove("show");
        history.replaceState(null, null, " ");
    }
});

document.addEventListener("DOMContentLoaded", () => {
    if (window.location.hash === "#email-change-card") {
        emailchangepopupWrapper.classList.add("show");
    }
    else if (window.location.hash === "#password-change-card") {
        passwordchangepopupWrapper.classList.add("show");
    }
    else if (window.location.hash === "#delete-account") {
        deleteAccountWrapper.classList.add("show");
    }
});