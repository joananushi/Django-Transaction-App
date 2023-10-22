document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");
    const registerForm = document.getElementById("register-form");
    const loginTab = document.getElementById("login-tab");
    const registerTab = document.getElementById("register-tab");

    registerForm.style.display = "none";

    loginTab.addEventListener("click", () => {
        loginForm.style.display = "block";
        registerForm.style.display = "none";
        loginTab.classList.add("active");
        registerTab.classList.remove("active");
    });

    registerTab.addEventListener("click", () => {
        registerForm.style.display = "block";
        loginForm.style.display = "none";
        registerTab.classList.add("active");
        loginTab.classList.remove("active");
    });
});

