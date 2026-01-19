// 全局主题切换系统
class ThemeManager {
  constructor() {
    this.currentTheme = localStorage.getItem('theme') || 'light';
    this.init();
  }

  init() {
    // 检查是否需要强制重置为浅色主题
    if (this.shouldForceLightTheme()) {
      this.forceLightTheme();
    }
    
    // 应用保存的主题
    this.applyTheme(this.currentTheme);
    
    // 创建主题切换组件
    this.createThemeSwitch();
    
    // 监听系统主题变化
    this.watchSystemTheme();
  }

  // 应用主题
  applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    this.currentTheme = theme;
    localStorage.setItem('theme', theme);
    
    // 更新所有主题切换按钮的状态
    this.updateThemeButtons();
    
    // 触发主题变化事件
    window.dispatchEvent(new CustomEvent('themeChanged', { 
      detail: { theme: theme } 
    }));
  }

  // 切换主题
  toggleTheme() {
    const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
    this.applyTheme(newTheme);
  }

  // 设置主题
  setTheme(theme) {
    if (theme === 'dark' || theme === 'light') {
      this.applyTheme(theme);
    }
  }

  // 获取当前主题
  getCurrentTheme() {
    return this.currentTheme;
  }

  // 检查是否需要强制浅色主题
  shouldForceLightTheme() {
    // 检查URL参数
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('forceLight') === 'true') {
      return true;
    }
    
    // 检查是否有强制浅色主题的标记
    if (sessionStorage.getItem('forceLightTheme') === 'true') {
      return true;
    }
    
    return false;
  }

  // 强制应用浅色主题
  forceLightTheme() {
    this.currentTheme = 'light';
    localStorage.setItem('theme', 'light');
    document.documentElement.setAttribute('data-theme', 'light');
    sessionStorage.removeItem('forceLightTheme');
  }

  // 清除主题缓存
  clearThemeCache() {
    localStorage.removeItem('theme');
    sessionStorage.removeItem('forceLightTheme');
    this.currentTheme = 'light';
    this.applyTheme('light');
  }

  // 创建主题切换组件
  createThemeSwitch() {
    // 检查是否已经存在主题切换组件
    if (document.querySelector('.theme-switch-container')) {
      return;
    }

    // 创建主题切换容器
    const themeContainer = document.createElement('div');
    themeContainer.className = 'theme-switch-container';
    themeContainer.innerHTML = `
      <div class="theme-toggle-btn" id="themeToggleBtn">
        <span class="theme-icon">☀️</span>
        <span class="theme-text">浅色</span>
        <div class="theme-switch">
          <input type="checkbox" id="themeSwitch" ${this.currentTheme === 'dark' ? 'checked' : ''}>
          <span class="theme-slider"></span>
        </div>
      </div>
    `;

    // 添加到页面
    const targetElement = document.querySelector('.nav-user') || 
                         document.querySelector('.nav-right') || 
                         document.querySelector('.header') ||
                         document.body;
    
    if (targetElement) {
      targetElement.appendChild(themeContainer);
    }

    // 绑定事件
    this.bindThemeEvents();
  }

  // 绑定主题切换事件
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

    // 更新主题文本和图标
    this.updateThemeDisplay();
  }

  // 更新主题显示
  updateThemeDisplay() {
    const themeText = document.querySelector('.theme-text');
    const themeIcon = document.querySelector('.theme-icon');
    
    if (themeText && themeIcon) {
      if (this.currentTheme === 'dark') {
        themeText.textContent = '深色';
        themeIcon.textContent = '🌙';
      } else {
        themeText.textContent = '浅色';
        themeIcon.textContent = '☀️';
      }
    }
  }

  // 更新所有主题按钮状态
  updateThemeButtons() {
    const themeSwitches = document.querySelectorAll('#themeSwitch');
    themeSwitches.forEach(switchEl => {
      switchEl.checked = this.currentTheme === 'dark';
    });
    
    this.updateThemeDisplay();
  }

  // 监听系统主题变化
  watchSystemTheme() {
    if (window.matchMedia) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      mediaQuery.addListener((e) => {
        // 如果用户没有手动设置过主题，则跟随系统
        if (!localStorage.getItem('theme')) {
          this.applyTheme(e.matches ? 'dark' : 'light');
        }
      });
    }
  }

  // 创建浮动主题切换按钮
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

    // 绑定浮动按钮事件
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

  // 获取主题相关的CSS变量值
  getThemeVariable(variable) {
    return getComputedStyle(document.documentElement).getPropertyValue(variable);
  }

  // 设置主题相关的CSS变量值
  setThemeVariable(variable, value) {
    document.documentElement.style.setProperty(variable, value);
  }
}

// 创建全局主题管理器实例
window.themeManager = new ThemeManager();

// 导出主题管理器类
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ThemeManager;
}

// 主题切换快捷键 (Ctrl/Cmd + Shift + T)
document.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'T') {
    e.preventDefault();
    window.themeManager.toggleTheme();
  }
});

// 页面加载完成后初始化主题
document.addEventListener('DOMContentLoaded', () => {
  // 确保主题正确应用
  window.themeManager.applyTheme(window.themeManager.getCurrentTheme());
  
  // 为没有导航栏的页面创建浮动主题切换按钮
  if (!document.querySelector('.top-nav') && !document.querySelector('.theme-switch-container')) {
    window.themeManager.createFloatingThemeSwitch();
  }
});

// 主题变化监听器
window.addEventListener('themeChanged', (e) => {
  console.log('主题已切换为:', e.detail.theme);
  
  // 可以在这里添加其他主题变化后的处理逻辑
  // 比如更新图表颜色、重新渲染组件等
});
