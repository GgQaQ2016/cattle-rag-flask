// Global site behaviors

document.addEventListener('DOMContentLoaded', function () {
  // Dismissible alerts
  document.querySelectorAll('.alert .close').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.parentElement.style.display = 'none';
    });
  });

  // Example logout handler
  const logout = document.getElementById('logout-btn');
  if (logout) {
    logout.addEventListener('click', function (e) {
      e.preventDefault();
      fetch('/logout', { method: 'POST' }).then(() => {
        window.location.href = '/login';
      });
    });
  }
});
