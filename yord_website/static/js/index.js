function goToHomepage() {
    window.location.href = "../general/home"
};

function goToMailingList() {
    window.location.href = "../mailing/members"
}

function errorGoToHomepage() {
    var tryAgainButton = document.getElementById('error-try-again');

    tryAgainButton.addEventListener('click', goToHomepage());
};

const menuToggle = document.querySelector(".menu-toggle");
const navMenu = document.querySelector(".nav-menu");
const navLink = document.querySelector(".nav-link")

menuToggle.addEventListener("click", mobileMenu)
menuToggle.addEventListener("blur", closeMenu)
navLink.forEach(n => n.addEventListener("click", closeMenu));

function mobileMenu() {
    menuToggle.classList.toggle("active");
    navMenu.classList.toggle("active")
    menuToggle.setAttribute('aria-expanded', true)
}

function closeMenu() {
    menuToggle.classList.remove("active")
    navMenu.classList.remove("active")
    menuToggle.setAttribute('aria-expanded', false)
}