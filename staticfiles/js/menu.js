document.addEventListener('DOMContentLoaded', function() {
    console.log('Script chargé'); // Debug
    const filterButtons = document.querySelectorAll('.filter-btn');
    const menuItems = document.querySelectorAll('.menu-item');
    const categoryDetails = document.querySelector('.category-details');
    const categoryName = document.querySelector('.category-name');
    const categoryDescription = document.querySelector('.category-description');

    // Debug - Afficher les éléments trouvés
    console.log('Nombre de boutons:', filterButtons.length);
    console.log('Nombre de menus:', menuItems.length);

    // Fonction pour mettre à jour les détails de la catégorie
    function updateCategoryDetails(name, description) {
        if (categoryDetails && categoryName && categoryDescription) {
            categoryDetails.style.display = 'block';
            categoryName.textContent = name;
            categoryDescription.textContent = description;
        }
    }

    // Fonction pour filtrer les menus
    function filterMenus(filter) {
        console.log('Filtrage pour:', filter); // Debug
        menuItems.forEach(item => {
            const itemCategory = item.getAttribute('data-category');
            console.log('Menu catégorie:', itemCategory); // Debug
            
            if (filter === 'all' || itemCategory === filter) {
                item.style.display = '';
                // Animation de fade in
                item.style.opacity = '0';
                setTimeout(() => {
                    item.style.opacity = '1';
                }, 50);
            } else {
                item.style.display = 'none';
            }
        });
    }

    // Gestionnaire d'événements pour les boutons de filtrage
    filterButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            console.log('Bouton cliqué:', this.getAttribute('data-filter')); // Debug
            
            // Retirer la classe active de tous les boutons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            
            // Ajouter la classe active au bouton cliqué
            this.classList.add('active');
            
            // Récupérer la catégorie et ses détails
            const filter = this.getAttribute('data-filter');
            const name = this.getAttribute('data-category-name');
            const description = this.getAttribute('data-category-description');
            
            // Mettre à jour l'affichage
            filterMenus(filter);
            updateCategoryDetails(name, description);
        });
    });

    // Initialiser avec "Tous" sélectionné
    const allButton = document.querySelector('[data-filter="all"]');
    if (allButton) {
        const name = allButton.getAttribute('data-category-name');
        const description = allButton.getAttribute('data-category-description');
        updateCategoryDetails(name, description);
    }

    // Animation initiale des éléments
    menuItems.forEach(item => {
        item.style.opacity = '0';
        item.style.transition = 'opacity 0.6s ease';
    });

    // Déclencher l'animation initiale après un court délai
    setTimeout(() => {
        menuItems.forEach(item => {
            item.style.opacity = '1';
        });
    }, 100);

    // Animation au scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observer tous les éléments de menu
    menuItems.forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(30px)';
        item.style.transition = 'all 0.6s ease';
        observer.observe(item);
    });

    // Gestion des boutons d'ajout au panier
    const cartButtons = document.querySelectorAll('.btn-cart:not(:disabled)');
    cartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-check me-2"></i>Ajouté !';
            this.style.background = 'linear-gradient(45deg, #28a745, #20c997)';
            
            setTimeout(() => {
                this.innerHTML = originalText;
                this.style.background = 'linear-gradient(45deg, var(--accent-color), #ff8c42)';
            }, 2000);
        });
    });
}); 