document.addEventListener('DOMContentLoaded', function() {
    // Gestion des boutons d'augmentation de quantité
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('increase-quantity')) {
            const menuId = e.target.getAttribute('data-menu-id');
            updateQuantity(menuId, 1);
        }
    });

    // Gestion des boutons de diminution de quantité
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('decrease-quantity')) {
            const menuId = e.target.getAttribute('data-menu-id');
            updateQuantity(menuId, -1);
        }
    });

    // Gestion des boutons de suppression d'article
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-item')) {
            const menuId = e.target.getAttribute('data-menu-id');
            removeItem(menuId);
        }
    });

    // Gestion du bouton vider panier
    document.addEventListener('click', function(e) {
        if (e.target.id === 'clear-cart') {
            clearCart();
        }
    });

    // Fonction pour mettre à jour la quantité
    function updateQuantity(menuId, change) {
        fetch(`/commandes/panier/ajouter/${menuId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                quantite: change
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Mettre à jour l'affichage de la quantité
                const quantityDisplay = document.querySelector(`.quantity-display[data-menu-id="${menuId}"]`);
                if (quantityDisplay) {
                    quantityDisplay.textContent = data.quantite;
                }

                // Mettre à jour le sous-total
                const sousTotal = document.querySelector(`.sous-total[data-menu-id="${menuId}"]`);
                if (sousTotal) {
                    sousTotal.textContent = data.sous_total + ' FCFA';
                }

                // Mettre à jour le total
                const cartTotal = document.getElementById('cart-total');
                if (cartTotal) {
                    cartTotal.textContent = data.total + ' FCFA';
                }

                // Si la quantité est 0, supprimer la ligne
                if (data.quantite === 0) {
                    const row = document.querySelector(`tr[data-menu-id="${menuId}"]`);
                    if (row) {
                        row.remove();
                    }
                    
                    // Vérifier s'il reste des articles dans le panier
                    const remainingRows = document.querySelectorAll('tbody tr[data-menu-id]');
                    if (remainingRows.length === 0) {
                        const tbody = document.querySelector('.table tbody');
                        if (tbody) {
                            tbody.innerHTML = '<tr><td colspan="4" class="text-center py-4">Votre panier est vide.</td></tr>';
                        }
                    }
                }

                // Mettre à jour le compteur du panier dans la navbar
                updateCartCount();
            } else {
                console.error('Erreur:', data.message);
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
    }

    // Fonction pour supprimer un article
    function removeItem(menuId) {
        fetch(`/commandes/panier/supprimer/${menuId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Supprimer la ligne du tableau
                const row = document.querySelector(`tr[data-menu-id="${menuId}"]`);
                if (row) {
                    row.remove();
                }

                // Mettre à jour le total
                const cartTotal = document.getElementById('cart-total');
                if (cartTotal) {
                    cartTotal.textContent = data.total + ' FCFA';
                }

                // Vérifier s'il reste des articles dans le panier
                const remainingRows = document.querySelectorAll('tbody tr[data-menu-id]');
                if (remainingRows.length === 0) {
                    const tbody = document.querySelector('.table tbody');
                    if (tbody) {
                        tbody.innerHTML = '<tr><td colspan="4" class="text-center py-4">Votre panier est vide.</td></tr>';
                    }
                }

                // Mettre à jour le compteur du panier dans la navbar
                updateCartCount();
            } else {
                console.error('Erreur:', data.message);
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
    }

    // Fonction pour vider le panier
    function clearCart() {
        if (confirm('Êtes-vous sûr de vouloir vider votre panier ?')) {
            fetch('/commandes/panier/vider/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Vider le contenu du modal
                    const tbody = document.querySelector('.table tbody');
                    if (tbody) {
                        tbody.innerHTML = '<tr><td colspan="4" class="text-center py-4">Votre panier est vide.</td></tr>';
                    }

                    // Mettre à jour le total
                    const cartTotal = document.getElementById('cart-total');
                    if (cartTotal) {
                        cartTotal.textContent = '0 FCFA';
                    }

                    // Mettre à jour le compteur du panier dans la navbar
                    updateCartCount();
                } else {
                    console.error('Erreur:', data.message);
                }
            })
            .catch(error => {
                console.error('Erreur:', error);
            });
        }
    }

    // Fonction pour mettre à jour le compteur du panier
    function updateCartCount() {
        fetch('/commandes/panier/count/')
        .then(response => response.json())
        .then(data => {
            const cartBadge = document.getElementById('cart-count');
            if (cartBadge) {
                cartBadge.textContent = data.count;
                if (data.count === 0) {
                    cartBadge.style.display = 'none';
                } else {
                    cartBadge.style.display = 'inline';
                }
            }
        })
        .catch(error => {
            console.error('Erreur lors de la mise à jour du compteur:', error);
        });
    }

    // Fonction pour récupérer le token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}); 