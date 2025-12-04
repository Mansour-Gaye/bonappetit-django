// Gestionnaire d'erreur global pour capturer toutes les erreurs
window.addEventListener('error', function(e) {
    console.error('ERREUR GLOBALE CAPTURÉE:', e.error);
    console.error('Message:', e.message);
    console.error('Fichier:', e.filename);
    console.error('Ligne:', e.lineno);
    console.error('Colonne:', e.colno);
    return false;
});

// Gestionnaire pour les promesses non gérées
window.addEventListener('unhandledrejection', function(e) {
    console.error('PROMESSE NON GÉRÉE:', e.reason);
    return false;
});

document.addEventListener('DOMContentLoaded', function() {
    console.log('CART MODAL JS CHARGÉ - VERSION DEBUG'); // Debug pour forcer le cache
    console.log('TEST: Le JS cart_modal.js est bien chargé !');
    // Initialisation : Mettre à jour le compteur au chargement
    updateCartCount();
    
    // Recharger le contenu du panier quand la modale s'ouvre
    const cartModal = document.getElementById('cartModal');
    if (cartModal) {
        cartModal.addEventListener('show.bs.modal', function() {
            reloadCartModal();
        });
    }

    // Gestion de tous les formulaires d'ajout au panier
    const forms = document.querySelectorAll('.add-to-cart-form');
    console.log('DEBUG: Nombre de formulaires trouvés:', forms.length);
    forms.forEach(form => {
        console.log('DEBUG: Ajout d\'event listener sur le formulaire:', form.action);
        form.addEventListener('submit', function(e) {
            console.log('DEBUG: Formulaire soumis, action:', form.action);
            // On autorise l'ajout au panier même si non connecté
            // Plus de redirection ni de stockage d'intention
            e.preventDefault(); // Empêche la redirection

            const button = form.querySelector('button[type="submit"]');
            const originalButtonHtml = button.innerHTML;
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

            // Correction : utiliser FormData pour compatibilité Django
            const formData = new FormData(form);

            console.log('DEBUG: Envoi de la requête fetch vers:', form.action);
            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: formData
            })
            .then(response => {
                console.log('DEBUG: Réponse reçue, status:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('DEBUG: Données reçues:', data);
                if (data.status === 'success' || data.success) {
                    updateCartCount(); // Mettre à jour le compteur
                    showSuccessNotification('Article ajouté au panier !');
                } else {
                    console.error('Erreur lors de l\'ajout au panier:', data.message);
                }
            })
            .catch(error => {
                console.error('DEBUG: Erreur Fetch:', error);
            })
            .finally(() => {
                // Réactiver le bouton après un court délai
                setTimeout(() => {
                    button.disabled = false;
                    button.innerHTML = originalButtonHtml;
                }, 500);
            });
        });
    });

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
                // Recharger le contenu du modal
                reloadCartModal();
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
                // Recharger le contenu du modal
                reloadCartModal();
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
                    // Recharger le contenu du modal
                    reloadCartModal();
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

    // Fonction pour recharger dynamiquement le contenu du modal panier
    function reloadCartModal() {
        fetch('/commandes/panier/modal/')
        .then(response => response.text())
        .then(html => {
            // Remplacer le contenu du modal (adapter le sélecteur à votre structure)
            const modalBody = document.querySelector('#cartModal .modal-body, .cart-modal-body');
            if (modalBody) {
                modalBody.innerHTML = html;
            }
        })
        .catch(error => {
            console.error('Erreur lors du rechargement du panier:', error);
        });
    }

    // Fonction pour afficher une notification de succès
    function showSuccessNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'alert alert-success alert-dismissible fade show';
        notification.style.position = 'fixed';
        notification.style.top = '20px';
        notification.style.right = '20px';
        notification.style.zIndex = '1050';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        document.body.appendChild(notification);
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => { notification.remove(); }, 150);
        }, 3000);
    }
}); 