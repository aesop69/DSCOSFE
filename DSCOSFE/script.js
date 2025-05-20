// Version: 1.8 | Last Updated: May 20, 2025

// Constants
const COMMANDS = {
    'find': 'commands/find.html',
    'ls': 'commands/ls.html',
    'rm': 'commands/rm.html',
    'ps': 'commands/ps.html',
    'kill': 'commands/kill.html',
    'ping': 'commands/ping.html',
    'curl': 'commands/curl.html'
};

// DOM Elements
const searchInput = document.getElementById('search');
const navButtons = document.querySelectorAll('nav button');
const collapsibles = document.querySelectorAll('.collapsible');

// Debounced search function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Enhanced search functionality
function executeSearch(query) {
    query = query.toLowerCase();
    const matches = Object.entries(COMMANDS).filter(([cmd]) => 
        cmd.includes(query) || cmd.startsWith(query)
    );

    if (matches.length > 0) {
        const [cmd, url] = matches[0];
        window.location.href = url;
    } else {
        alert('Command not found. Try searching for: ' + 
            Object.keys(COMMANDS).join(', '));
    }
}

// Initialize search
const debouncedSearch = debounce(executeSearch, 300);
searchInput.addEventListener('input', (e) => {
    debouncedSearch(e.target.value);
});

// Collapsible sections
function toggleCollapsible(event) {
    const button = event.currentTarget;
    const content = button.nextElementSibling;
    
    content.style.display = content.style.display === "block" ? "none" : "block";
    button.setAttribute('aria-expanded', content.style.display === "block");
}

collapsibles.forEach(button => {
    button.addEventListener('click', toggleCollapsible);
    button.setAttribute('aria-expanded', 'false');
});

// Dark mode
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Settings
function openSettings() {
    const settingsModal = document.createElement('div');
    settingsModal.className = 'settings-modal';
    settingsModal.innerHTML = `
        <div class="settings-content">
            <h2>Settings</h2>
            <div>
                <label>
                    <input type="checkbox" id="darkModeToggle">
                    Dark Mode
                </label>
            </div>
            <button onclick="closeSettings()">Close</button>
        </div>
    `;
    document.body.appendChild(settingsModal);
}

function closeSettings() {
    const settingsModal = document.querySelector('.settings-modal');
    if (settingsModal) {
        settingsModal.remove();
    }
}

// Initialize dark mode
function initDarkMode() {
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
    }
}

// Add keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeSettings();
    }
});

// Initialize everything
initDarkMode();
