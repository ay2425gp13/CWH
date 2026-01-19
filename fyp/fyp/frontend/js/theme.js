// Global Theme Switching System
class ThemeManager {
  constructor() {
    this.currentTheme = localStorage.getItem('theme') || 'light';
    this.init();
  }

  init() {
    // Check if need to force reset to light theme
    if (this.shouldForceLightTheme()) {
      this.forceLightTheme();
    }

    // Apply saved theme
    this.applyTheme(this.currentTheme);

    // Create theme switch component
    this.createThemeSwitch();

    // Listen for system theme changes
    this.watchSystemTheme();
  }

  // Apply theme
  applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    this.currentTheme = theme;
    localStorage.setItem('theme', theme);

    // Update all theme switch button states
    this.updateThemeButtons();

    // Trigger theme change event
    window.dispatchEvent(new CustomEvent('themeChanged', {
      detail: { theme: theme }
    }));
  }

  // Toggle theme
  toggleTheme() {
    const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
    this.applyTheme(newTheme);
  }

  // Set theme
  setTheme(theme) {
    if (theme === 'dark' || theme === 'light') {
      this.applyTheme(theme);
    }
  }

  // Get current theme
  getCurrentTheme() {
    return this.currentTheme;
  }

  // Check if need to force light theme
  shouldForceLightTheme() {
    // Check URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('forceLight') === 'true') {
      return true;
    }

    // Check if there's a force light theme flag
    if (sessionStorage.getItem('forceLightTheme') === 'true') {
      return true;
    }

    return false;
  }

  // Force apply light theme
  forceLightTheme() {
    this.currentTheme = 'light';
    localStorage.setItem('theme', 'light');
    document.documentElement.setAttribute('data-theme', 'light');
    sessionStorage.removeItem('forceLightTheme');
  }

  // Clear theme cache
  clearThemeCache() {
    localStorage.removeItem('theme');
    sessionStorage.removeItem('forceLightTheme');
    this.currentTheme = 'light';
    this.applyTheme('light');
  }

  // Create theme switch component
  createThemeSwitch() {
    // Check if theme switch component already exists
    if (document.querySelector('.theme-switch-container')) {
      return;
    }

    // Create theme switch container
    const themeContainer = document.createElement('div');
    themeContainer.className = 'theme-switch-container';
    themeContainer.style.animation = 'slideInLeft 0.5s ease-out';
    themeContainer.innerHTML = `
      <div class="theme-toggle-btn" id="themeToggleBtn">
        <span class="theme-icon">☀️</span>
        <span class="theme-text">Light</span>
        <div class="theme-switch">
          <input type="checkbox" id="themeSwitch" ${this.currentTheme === 'dark' ? 'checked' : ''}>
          <span class="theme-slider"></span>
        </div>
      </div>
    `;

    // Add to page
    const targetElement = document.querySelector('.nav-user') ||
                         document.querySelector('.nav-right') ||
                         document.querySelector('.header') ||
                         document.body;

    if (targetElement) {
      targetElement.appendChild(themeContainer);
    }

    // Bind events
    this.bindThemeEvents();
  }

  // Bind theme switch events
  bindThemeEvents() {
    const themeSwitch = document.getElementById('themeSwitch');
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const themeText = document.querySelector('.theme-text');
    const themeIcon = document.querySelector('.theme-icon');

    if (themeSwitch) {
      themeSwitch.addEventListener('change', () => {
        this.toggleTheme();
      });
    }

    if (themeToggleBtn) {
      themeToggleBtn.addEventListener('click', () => {
        this.toggleTheme();
      });
    }

    // Update theme text and icon
    this.updateThemeDisplay();
  }

  // Update theme display
  updateThemeDisplay() {
    const themeText = document.querySelector('.theme-text');
    const themeIcon = document.querySelector('.theme-icon');

    if (themeText && themeIcon) {
      if (this.currentTheme === 'dark') {
        themeText.textContent = 'Dark';
        themeIcon.textContent = '🌙';
      } else {
        themeText.textContent = 'Light';
        themeIcon.textContent = '☀️';
      }
    }
  }

  // Update all theme button states
  updateThemeButtons() {
    const themeSwitches = document.querySelectorAll('#themeSwitch');
    themeSwitches.forEach(switchEl => {
      switchEl.checked = this.currentTheme === 'dark';
    });

    this.updateThemeDisplay();
  }

  // Watch system theme changes
  watchSystemTheme() {
    if (window.matchMedia) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      mediaQuery.addListener((e) => {
        // If user hasn't manually set theme, follow system
        if (!localStorage.getItem('theme')) {
          this.applyTheme(e.matches ? 'dark' : 'light');
        }
      });
    }
  }

  // Create floating theme switch button
  createFloatingThemeSwitch() {
    const floatingBtn = document.createElement('div');
    floatingBtn.className = 'theme-indicator';
    floatingBtn.innerHTML = `
      <div class="theme-toggle-btn" id="floatingThemeBtn">
        <span class="theme-icon">☀️</span>
        <div class="theme-switch">
          <input type="checkbox" id="floatingThemeSwitch" ${this.currentTheme === 'dark' ? 'checked' : ''}>
          <span class="theme-slider"></span>
        </div>
      </div>
    `;

    document.body.appendChild(floatingBtn);

    // Bind floating button events
    const floatingSwitch = document.getElementById('floatingThemeSwitch');
    const floatingToggleBtn = document.getElementById('floatingThemeBtn');

    if (floatingSwitch) {
      floatingSwitch.addEventListener('change', () => {
        this.toggleTheme();
      });
    }

    if (floatingToggleBtn) {
      floatingToggleBtn.addEventListener('click', () => {
        this.toggleTheme();
      });
    }
  }

  // Get theme-related CSS variable value
  getThemeVariable(variable) {
    return getComputedStyle(document.documentElement).getPropertyValue(variable);
  }

  // Set theme-related CSS variable value
  setThemeVariable(variable, value) {
    document.documentElement.style.setProperty(variable, value);
  }
}

// Create global theme manager instance
window.themeManager = new ThemeManager();

// Export theme manager class
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ThemeManager;
}

// Theme switch shortcut key (Ctrl/Cmd + Shift + T)
document.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'T') {
    e.preventDefault();
    window.themeManager.toggleTheme();
  }
});

// Initialize theme after page load
document.addEventListener('DOMContentLoaded', () => {
  // Ensure theme is correctly applied
  window.themeManager.applyTheme(window.themeManager.getCurrentTheme());

  // Create floating theme switch button for pages without navigation
  if (!document.querySelector('.top-nav') && !document.querySelector('.theme-switch-container')) {
    window.themeManager.createFloatingThemeSwitch();
  }
});

// Theme change listener
window.addEventListener('themeChanged', (e) => {
  console.log('Theme has been switched to:', e.detail.theme);

  // Can add other post-theme-change processing logic here
  // Such as updating chart colors, re-rendering components, etc.
});
