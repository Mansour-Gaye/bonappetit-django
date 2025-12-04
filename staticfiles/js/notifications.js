// Gestion du badge de notifications et du dropdown

document.addEventListener('DOMContentLoaded', function() {
    const badge = document.getElementById('notification-badge');
    const icon = document.getElementById('notification-icon');
    const dropdown = document.getElementById('notification-dropdown');
    const alerts = document.querySelectorAll('.notification-alert');

    // Compteur dynamique : nombre de notifications visibles
    function updateBadge() {
        const count = alerts.length;
        if (badge) {
            if (count > 0) {
                badge.textContent = count;
                badge.classList.remove('d-none');
                badge.classList.add('new');
            } else {
                badge.textContent = '0';
                badge.classList.add('d-none');
                badge.classList.remove('new');
            }
        }
    }
    updateBadge();

    // Marquage comme lu (sessionStorage, reset badge)
    function markNotificationsRead() {
        sessionStorage.setItem('notificationsRead', '1');
        if (badge) {
            badge.textContent = '0';
            badge.classList.add('d-none');
            badge.classList.remove('new');
        }
    }

    // Affichage du dropdown au clic sur la cloche
    icon && icon.addEventListener('click', function(e) {
        e.preventDefault();
        dropdown.classList.toggle('show');
        markNotificationsRead();
        // Remplir le dropdown avec les notifications (exemple)
        let html = '';
        alerts.forEach(function(alert) {
            html += `<div class=\"dropdown-item\">${alert.textContent}</div>`;
        });
        dropdown.innerHTML = html || '<span class="dropdown-item-text text-muted">Aucune notification</span>';
    });

    // Fermer le dropdown si clic ailleurs
    document.addEventListener('click', function(e) {
        if (!icon.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.classList.remove('show');
        }
    });

    // Auto-dismiss notifications (success/info) après 3s
    alerts.forEach(function(alert) {
        if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
            setTimeout(function() {
                alert.classList.add('fade-out');
                setTimeout(function() {
                    alert.remove();
                    updateBadge();
                }, 600);
            }, 3000);
        }
    });

    // Préparation du polling AJAX (structure, à compléter)
    function pollNotifications() {
        // TODO: requête AJAX pour vérifier les notifications côté serveur
        // Adapter le polling selon le type d'utilisateur si besoin
        // setTimeout(pollNotifications, 15000); // 15s
    }
    // pollNotifications();

    // Marquer toutes les notifications comme lues
    const markAllBtn = document.getElementById('mark-all-read-btn');
    if (markAllBtn) {
        markAllBtn.addEventListener('click', function(e) {
            e.preventDefault();
            fetch('/notifications/mark_all_read/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Vider le dropdown et le badge
                    const dropdown = document.getElementById('notification-dropdown');
                    const badge = document.getElementById('notification-badge');
                    if (dropdown) dropdown.innerHTML = '<span class="dropdown-item-text text-muted">Aucune notification</span>';
                    if (badge) {
                        badge.textContent = '0';
                        badge.classList.add('d-none');
                        badge.classList.remove('new');
                    }
                }
            });
        });
    }

    // Gestion de l'overlay custom pour la modale notifications
    const notifOverlay = document.getElementById('notification-overlay');
    const notifModal = document.getElementById('notificationsModal');
    if (notifModal && notifOverlay) {
        notifModal.addEventListener('show.bs.modal', function() {
            notifOverlay.style.display = 'block';
        });
        notifModal.addEventListener('hidden.bs.modal', function() {
            notifOverlay.style.display = 'none';
        });
    }
}); 