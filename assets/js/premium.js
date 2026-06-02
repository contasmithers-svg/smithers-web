document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
  const buttons = document.querySelectorAll('[data-track]');
  buttons.forEach(btn => btn.addEventListener('click', () => {
    try { console.log('Smithers CTA:', btn.dataset.track); } catch(e) {}
  }));

  // Show mobile nav on small screens
  function checkMobile() {
    var nav = document.querySelector('.mobile-hero-nav');
    if (!nav) return;
    if (window.innerWidth <= 930) {
      nav.style.display = 'grid';
    } else {
      nav.style.display = '';
    }
  }
  checkMobile();
  window.addEventListener('resize', checkMobile);
});
