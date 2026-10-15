// ===== Переключение темы =====
(function() {
  const saved = localStorage.getItem('theme');
  if (saved === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
  }

  document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('theme-toggle');
    if (!btn) return;

    const updateIcon = () => {
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      btn.textContent = isDark ? '☀️' : '🌙';
    };
    updateIcon();

    btn.addEventListener('click', function() {
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      if (isDark) {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
      } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
      }
      updateIcon();
    });
  });
})();