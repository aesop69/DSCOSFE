const settings = {
    darkMode: false,
    preferredFontSize: "16px",
    theme: "default"
};

function toggleDarkMode() {
    settings.darkMode = !settings.darkMode;
    document.body.classList.toggle("dark-mode");
    localStorage.setItem("darkMode", settings.darkMode);
}

// Apply stored settings
document.addEventListener("DOMContentLoaded", () => {
    if (localStorage.getItem("darkMode") === "true") {
        document.body.classList.add("dark-mode");
    }
});
