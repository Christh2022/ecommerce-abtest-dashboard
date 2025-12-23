// Script pour le bouton Retour en haut
document.addEventListener('DOMContentLoaded', function() {
    const scrollBtn = document.getElementById('scroll-top-btn');
    
    if (!scrollBtn) return;
    
    // Afficher/masquer le bouton selon le scroll
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollBtn.classList.add('show');
        } else {
            scrollBtn.classList.remove('show');
        }
    });
    
    // Scroll smooth vers le haut au clic
    scrollBtn.addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});
