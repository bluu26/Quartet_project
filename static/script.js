// Funkcja do ustawienia klasy 'active' na podstawie localStorage
function setActiveLink() {
  const activeLink = localStorage.getItem('activeLink');
  if (activeLink) {
    document.querySelectorAll('#navbar li a').forEach(link => {
      link.classList.remove('active');
      if (link.href === activeLink) {
        link.classList.add('active');
      }
    });
  }
}

// Ustawienie klasy 'active' po załadowaniu strony
document.addEventListener('DOMContentLoaded', function() {
  setActiveLink();

  // Dodanie nasłuchiwaczy do linków
  document.querySelectorAll('#navbar li a').forEach(item => {
    item.addEventListener('click', function(event) {
      // Usunięcie klasy 'active' z wszystkich linków
      document.querySelectorAll('#navbar li a').forEach(link => {
        link.classList.remove('active');
      });

      // Dodanie klasy 'active' do klikniętego linku
      event.target.classList.add('active');

      // Zapisanie klikniętego linku do localStorage
      localStorage.setItem('activeLink', event.target.href);
    });
  });
});
