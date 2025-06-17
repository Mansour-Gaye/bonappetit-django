/**
 * Custom JavaScript for Bon Appétit Restaurant
 */

$(document).ready(function() {
    // Initialize AOS (Animate On Scroll)
    AOS.init({
        duration: 1000,
        easing: 'ease-in-out',
        once: true,
        mirror: false
    });

    // Initialize GLightbox for video popups
    GLightbox({
        selector: '.glightbox'
    });

    // Initialize Isotope for menu filtering
    if ($('.isotope-container').length) {
        $('.isotope-container').isotope({
            itemSelector: '.isotope-item',
            layoutMode: 'masonry',
            masonry: {
                columnWidth: '.isotope-item'
            }
        });
    }

    // Menu filter functionality
    $('.menu-filters li').on('click', function() {
        $('.menu-filters li').removeClass('filter-active');
        $(this).addClass('filter-active');
        
        var filterValue = $(this).attr('data-filter');
        $('.isotope-container').isotope({
            filter: filterValue
        });
    });

    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 100
            }, 1000);
        }
    });

    // Header scroll effect
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('#header').addClass('header-scrolled');
        } else {
            $('#header').removeClass('header-scrolled');
        }
    });

    // Mobile navigation toggle
    $('.mobile-nav-toggle').on('click', function() {
        $('#navmenu').toggleClass('mobile-nav-active');
        $(this).toggleClass('bi-list bi-x');
    });

    // Close mobile menu when clicking on a link
    $('#navmenu a').on('click', function() {
        if ($('#navmenu').hasClass('mobile-nav-active')) {
            $('#navmenu').removeClass('mobile-nav-active');
            $('.mobile-nav-toggle').removeClass('bi-x').addClass('bi-list');
        }
    });

    // Add to cart functionality
    $('.add-to-cart').on('click', function() {
        var menuId = $(this).data('menu-id');
        var menuName = $(this).data('menu-name');
        var button = $(this);
        
        // Disable button during request
        button.prop('disabled', true).html('<i class="bi bi-hourglass-split"></i> Ajout...');
        
        $.ajax({
            url: '/commandes/ajouter_au_panier/' + menuId + '/',
            method: 'POST',
            data: JSON.stringify({
                quantite: 1
            }),
            contentType: 'application/json',
            success: function(response) {
                if (response.success) {
                    // Show success message
                    button.html('<i class="bi bi-check-circle"></i> Ajouté !').removeClass('btn-primary').addClass('btn-success');
                    
                    // Trigger cart update event
                    document.dispatchEvent(new Event('cartUpdated'));
                    
                    // Reset button after 2 seconds
                    setTimeout(function() {
                        button.html('<i class="bi bi-cart-plus"></i> Ajouter au panier').removeClass('btn-success').addClass('btn-primary').prop('disabled', false);
                    }, 2000);
                } else {
                    button.html('<i class="bi bi-exclamation-triangle"></i> Erreur').removeClass('btn-primary').addClass('btn-danger');
                    setTimeout(function() {
                        button.html('<i class="bi bi-cart-plus"></i> Ajouter au panier').removeClass('btn-danger').addClass('btn-primary').prop('disabled', false);
                    }, 2000);
                }
            },
            error: function(xhr, status, error) {
                console.log('Status:', xhr.status);
                console.log('Response:', xhr.responseText);
                
                // Check if it's a redirect to login
                if (xhr.status === 401 || xhr.status === 403 || xhr.status === 302) {
                    window.location.href = '/comptes/login/';
                } else {
                    button.html('<i class="bi bi-exclamation-triangle"></i> Erreur').removeClass('btn-primary').addClass('btn-danger');
                    setTimeout(function() {
                        button.html('<i class="bi bi-cart-plus"></i> Ajouter au panier').removeClass('btn-danger').addClass('btn-primary').prop('disabled', false);
                    }, 2000);
                }
            }
        });
    });

    // Quantity controls in menu detail
    $('#increaseQuantity').on('click', function() {
        var quantity = parseInt($('#quantity').val());
        if (quantity < 10) {
            $('#quantity').val(quantity + 1);
        }
    });
    
    $('#decreaseQuantity').on('click', function() {
        var quantity = parseInt($('#quantity').val());
        if (quantity > 1) {
            $('#quantity').val(quantity - 1);
        }
    });

    // Add to cart from detail page
    $('.add-to-cart-detail').on('click', function() {
        var menuId = $(this).data('menu-id');
        var menuName = $(this).data('menu-name');
        var quantity = parseInt($('#quantity').val());
        var button = $(this);
        
        // Disable button during request
        button.prop('disabled', true).html('<i class="bi bi-hourglass-split"></i> Ajout...');
        
        $.ajax({
            url: '/commandes/ajouter_au_panier/' + menuId + '/',
            method: 'POST',
            data: JSON.stringify({
                quantite: quantity
            }),
            contentType: 'application/json',
            success: function(response) {
                if (response.success) {
                    // Show success message
                    button.html('<i class="bi bi-check-circle"></i> Ajouté !').removeClass('btn-primary').addClass('btn-success');
                    
                    // Trigger cart update event
                    document.dispatchEvent(new Event('cartUpdated'));
                    
                    // Reset button after 2 seconds
                    setTimeout(function() {
                        button.html('<i class="bi bi-cart-plus"></i> Ajouter au panier').removeClass('btn-success').addClass('btn-primary').prop('disabled', false);
                    }, 2000);
                } else {
                    button.html('<i class="bi bi-exclamation-triangle"></i> Erreur').removeClass('btn-primary').addClass('btn-danger');
                    setTimeout(function() {
                        button.html('<i class="bi bi-cart-plus"></i> Ajouter au panier').removeClass('btn-danger').addClass('btn-primary').prop('disabled', false);
                    }, 2000);
                }
            },
            error: function(xhr, status, error) {
                console.log('Status:', xhr.status);
                console.log('Response:', xhr.responseText);
                
                // Check if it's a redirect to login
                if (xhr.status === 401 || xhr.status === 403 || xhr.status === 302) {
                    window.location.href = '/comptes/login/';
                } else {
                    button.html('<i class="bi bi-exclamation-triangle"></i> Erreur').removeClass('btn-primary').addClass('btn-danger');
                    setTimeout(function() {
                        button.html('<i class="bi bi-cart-plus"></i> Ajouter au panier').removeClass('btn-danger').addClass('btn-primary').prop('disabled', false);
                    }, 2000);
                }
            }
        });
    });

    // Cart functionality
    function loadCartContent() {
        $.get('/commandes/cart_modal_content/', function(data) {
            $('#cartModalBody').html(data);
        });
    }

    function updateCartCount() {
        $.get('/commandes/get_cart_count/', function(data) {
            $('#cartCount').text(data.count);
        });
    }

    // Listen for cart update event
    document.addEventListener('cartUpdated', function() {
        updateCartCount();
        loadCartContent();
    });

    // Load cart content when modal opens
    $('#cartModal').on('show.bs.modal', function() {
        loadCartContent();
    });

    // Handle order button
    $('#btnCommander').on('click', function() {
        window.location.href = '/commandes/nouvelle_commande/';
    });

    // Form validation
    $('.php-email-form').on('submit', function(e) {
        e.preventDefault();
        
        var form = $(this);
        var submitBtn = form.find('button[type="submit"]');
        
        submitBtn.prop('disabled', true).html('Envoi en cours...');
        
        // Simulate form submission (replace with actual form handling)
        setTimeout(function() {
            submitBtn.html('Message envoyé !').removeClass('btn-primary').addClass('btn-success');
            form[0].reset();
            
            setTimeout(function() {
                submitBtn.html('Envoyer Message').removeClass('btn-success').addClass('btn-primary').prop('disabled', false);
            }, 3000);
        }, 2000);
    });

    // Preloader
    $(window).on('load', function() {
        if ($('#preloader').length) {
            $('#preloader').fadeOut('slow', function() {
                $(this).remove();
            });
        }
    });
}); 