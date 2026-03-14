// shared-sidebar.js — inject sidebar + shell into any dashboard page

function buildSidebar(activePage, user) {
  const nav = [
    { id: 'dashboard',  icon: '⬡', label: 'Dashboard',       href: 'dashboard.html' },
    { id: 'sessions',   icon: '◎', label: 'Session log',      href: 'sessions.html' },
    { id: 'nudges',     icon: '◈', label: 'Nudge history',    href: 'nudges.html' },
    { id: 'insights',   icon: '◑', label: 'Weekly insights',  href: 'insights.html' },
    { id: 'settings',   icon: '◌', label: 'Settings',         href: 'settings.html' },
    { id: 'rewards',    icon: '💎', label: 'Rewards store',    href: 'rewards.html' },
  ];

  const items = nav.map(n => `
    <a href="${n.href}" class="nav-item ${n.id === activePage ? 'active' : ''}">
      <span class="nav-icon">${n.icon}</span>
      <span>${n.label}</span>
    </a>
  `).join('');

  return `
    <div class="mobile-hamburger" id="mobileMenuBtn">≡</div>
    <div class="sidebar-overlay" id="sidebarOverlay"></div>
    <aside class="sidebar" id="appSidebar">
      <div class="sidebar-logo">
        <div class="logo-pulse"></div>
        <span class="logo-text">Presence Pulse</span>
      </div>
      <div class="nav-section-label">Menu</div>
      ${items}
      <div class="nav-spacer"></div>
      <a href="landing.html" class="nav-item">
        <span class="nav-icon">↖</span>
        <span>Landing page</span>
      </a>
      <div class="nav-user">
        <div class="user-avatar">${user.initials}</div>
        <div>
          <div class="user-name">${user.name}</div>
          <div class="user-plan">Premium · Alt-f4</div>
        </div>
      </div>
    </aside>
  `;
}

document.addEventListener('DOMContentLoaded', () => {
  const page = document.body.dataset.page;
  const pp = window.__PP_USER || {};
  const user = {
    name:     pp.name     || 'User',
    initials: pp.initials || 'U',
  };
  document.querySelector('.app-shell').insertAdjacentHTML('afterbegin', buildSidebar(page, user));

  const btn = document.getElementById('mobileMenuBtn');
  const overlay = document.getElementById('sidebarOverlay');
  const sidebar = document.getElementById('appSidebar');

  if (btn && overlay && sidebar) {
    btn.addEventListener('click', () => {
      sidebar.classList.add('open');
      overlay.classList.add('open');
    });
    overlay.addEventListener('click', () => {
      sidebar.classList.remove('open');
      overlay.classList.remove('open');
    });
  }
});
