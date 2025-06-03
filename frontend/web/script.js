// script.js
// Initialize the application when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => {
    initializeApp();
});

// Main initialization function that sets up different features based on the current page
function initializeApp() {
    setCopyrightYear();  // Set the current year in the footer
    loadCartCount();     // Load and display the number of items in cart
    
    // Load products if on the products page
    if (window.location.pathname.endsWith('products.html')) {
        loadProducts();
    }

    // Set up contact form if it exists on the page
    if (document.getElementById('contactForm')) {
        setupContactForm();
    }

    // Set up registration form if it exists on the page
    if (document.getElementById('registrationForm')) {
        setupRegistrationForm();
    }

    // Load cart items if on the cart page
    if (window.location.pathname.endsWith('cart.html')) {
        loadCartItems();
    }
       // Load order summary if on the checkout page
    if (window.location.pathname.endsWith('checkout.html')) {
        loadOrderSummary();
    }
}

// =========================
// CART FUNCTIONALITY
// =========================

// Initialize cart from localStorage or empty array if no cart exists
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Add a product to the cart
function addToCart(productId, quantity = 1) {
    getProductById(productId).then(product => {
        if (!product) return showError('Product not found');

        // Check if product already exists in cart
        const existingItem = cart.find(item => item.id === productId);
        // If exists, increase quantity, otherwise add new item
        existingItem ? existingItem.quantity += quantity : cart.push({ ...product, quantity });

        updateCartStorage();
        showSuccessToast(`${product.name} added to cart`);
    }).catch(error => {
        showError('Failed to add to cart', error);
    });
}

// Remove a product from the cart
function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    updateCartStorage();
    showSuccessToast('Item removed from cart');
}

// Update cart in localStorage and refresh display
function updateCartStorage() {
    localStorage.setItem('cart', JSON.stringify(cart));
    loadCartCount();
    if (window.location.pathname.endsWith('cart.html')) loadCartItems();
}

// Update the cart count badge in the navigation
function loadCartCount() {
    const count = cart.reduce((total, item) => total + item.quantity, 0);
    document.querySelectorAll('#cartCount').forEach(el => el.textContent = count);
}

function loadCartItems() {
    const cartItemsContainer = document.getElementById('cartItems');
    if (!cartItemsContainer) return;

    if (cart.length === 0) {
        cartItemsContainer.innerHTML = `
            <div class="card-body text-center py-5">
                <i class="fas fa-shopping-cart fa-3x text-muted mb-3"></i>
                <h5 class="text-muted">Your cart is empty</h5>
                <a href="products.html" class="btn btn-danger mt-3">Start Shopping</a>
            </div>
        `;
        updateOrderSummary(0);
        return;
    }

    cartItemsContainer.innerHTML = `
        <div class="card-body">
            ${cart.map(item => `
                <div class="row align-items-center mb-4 cart-item" data-id="${item.id}">
                    <div class="col-2">
                        <img src="${item.image}" class="img-fluid rounded" alt="${item.name}">
                    </div>
                    <div class="col-4">
                        <h5 class="mb-1">${item.name}</h5>
                        <p class="text-muted mb-0">$${item.price.toFixed(2)} each</p>
                    </div>
                    <div class="col-3">
                        <div class="input-group">
                            <button class="btn btn-outline-danger" onclick="updateQuantity(${item.id}, -1)">-</button>
                            <input type="number" class="form-control text-center" value="${item.quantity}" 
                                   min="1" onchange="updateQuantity(${item.id}, this.value - ${item.quantity})">
                            <button class="btn btn-outline-danger" onclick="updateQuantity(${item.id}, 1)">+</button>
                        </div>
                    </div>
                    <div class="col-2 text-end">
                        <h5 class="mb-0">$${(item.price * item.quantity).toFixed(2)}</h5>
                    </div>
                    <div class="col-1 text-end">
                        <button class="btn btn-link text-danger" onclick="removeFromCart(${item.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `).join('')}
        </div>
    `;

    updateOrderSummary();
}

function updateQuantity(productId, change) {
    const item = cart.find(item => item.id === productId);
    if (!item) return;

    const newQuantity = item.quantity + change;
    if (newQuantity < 1) {
        removeFromCart(productId);
        return;
    }

    item.quantity = newQuantity;
    updateCartStorage();
    loadCartItems();
}

function updateOrderSummary() {
    const subtotal = cart.reduce((total, item) => total + (item.price * item.quantity), 0);
    const shipping = subtotal > 0 ? 10 : 0; // $10 shipping if there are items
    const tax = subtotal * 0.13; // 13% tax
    const total = subtotal + shipping + tax;

    document.getElementById('subtotal').textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById('shipping').textContent = `$${shipping.toFixed(2)}`;
    document.getElementById('tax').textContent = `$${tax.toFixed(2)}`;
    document.getElementById('total').textContent = `$${total.toFixed(2)}`;
}

function checkout() {
    if (cart.length === 0) {
        showError('Your cart is empty');
        return;
    }
        window.location.href = 'checkout.html';
}

function processOrder() {
    const form = document.getElementById('checkoutForm');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    // Simulate order processing
    const orderNumber = Math.floor(Math.random() * 1000000);
    
    // Clear cart
    cart = [];
    updateCartStorage();

    // Show success message
    const modal = document.getElementById('checkoutModal');
    const checkoutModal = bootstrap.Modal.getInstance(modal);
    checkoutModal.hide();

    // Show order confirmation
    const confirmationModal = document.createElement('div');
    confirmationModal.className = 'modal fade';
    confirmationModal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Order Confirmed!</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body text-center">
                    <i class="fas fa-check-circle text-success fa-3x mb-3"></i>
                    <h5>Thank you for your order!</h5>
                    <p>Your order number is: <strong>#${orderNumber}</strong></p>
                    <p>A confirmation email has been sent to your email address.</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-danger" data-bs-dismiss="modal" onclick="window.location.href='index.html'">Return to Home</button>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(confirmationModal);
    const confirmationBootstrapModal = new bootstrap.Modal(confirmationModal);
    confirmationBootstrapModal.show();

    // Clean up modal when hidden
    confirmationModal.addEventListener('hidden.bs.modal', () => {
        confirmationModal.remove();
    });
}

// =========================
// PRODUCT FUNCTIONALITY
// =========================

// Fetch a single product by its ID
async function getProductById(productId) {
    try {
        const response = await fetch('products.json?' + new Date().getTime(), {
            cache: 'no-store',
            headers: {
                'Cache-Control': 'no-cache'
            }
        });
        const data = await response.json();
        return data.products.find(product => product.id === productId);
    } catch (error) {
        showError('Failed to fetch product details', error);
        return null;
    }
}

// Load all products from the JSON file
async function loadProducts() {
    try {
        console.log('Attempting to fetch products...');
        const response = await fetch('products.json?' + new Date().getTime(), {
            cache: 'no-store',
            headers: {
                'Cache-Control': 'no-cache'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Products data loaded:', data);
        
        if (!data.products || !Array.isArray(data.products)) {
            throw new Error('Invalid products data format');
        }
        
        displayProducts(data.products);
    } catch (error) {
        console.error('Detailed error:', error);
        const container = document.getElementById('product-list');
        container.innerHTML = `
            <div class="col-12 text-center">
                <div class="alert alert-danger" role="alert">
                    <h4 class="alert-heading">Failed to load products!</h4>
                    <p>${error.message}</p>
                    <p>Please try refreshing the page or contact support if the problem persists.</p>
                </div>
            </div>
        `;
    }
}

// Display products in the product list container
function displayProducts(products) {
    console.log('Displaying products:', products);
    const container = document.getElementById('product-list');
    if (!container) {
        console.error('Product list container not found!');
        return;
    }
    
    const productHTML = products.map(product => {
        console.log('Processing product:', product);
        return `
            <div class="col">
                <div class="card h-100 shadow-sm">
                    <img src="${product.image}" class="card-img-top p-3" alt="${product.name}">
                    <div class="card-body">
                        <h3 class="h5">${product.name}</h3>
                        <p class="text-danger fw-bold">$${product.price.toFixed(2)}</p>
                        <button class="btn btn-danger w-100" onclick="addToCart(${product.id})">
                            <i class="fas fa-cart-plus me-2"></i>Add to Cart
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    console.log('Generated HTML:', productHTML);
    container.innerHTML = productHTML;
}

// =========================
// FORM HANDLING
// =========================

// Set up contact form submission handler
function setupContactForm() {
    document.getElementById('contactForm').addEventListener('submit', e => {
        e.preventDefault();
        if (validateForm(e.target)) {
            alert('Thank you for your message! We will respond within 24 hours.');
            e.target.reset();
        }
    });
}

// Set up registration form submission handler
function setupRegistrationForm() {
    const form = document.getElementById('registrationForm');
    form.addEventListener('submit', e => {
        e.preventDefault();
        if (validateRegistration(form)) {
            alert('Registration successful! Redirecting to login...');
            window.location.href = 'user.html';
        }
    });
}

// Validate form fields
function validateForm(form) {
    let isValid = true;
    Array.from(form.elements).forEach(element => {
        if (element.required && !element.value.trim()) {
            isValid = false;
            element.classList.add('is-invalid');
        } else {
            element.classList.remove('is-invalid');
        }
    });
    return isValid;
}

// =========================
// HELPER FUNCTIONS
// =========================

// Update copyright year in the footer
function setCopyrightYear() {
    document.getElementById('year').textContent = new Date().getFullYear();
}

// Display error message
function showError(message, error) {
    console.error(message, error);
    alert(message);
}

// Display success message as a toast notification
function showSuccessToast(message) {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = 'position-fixed bottom-0 end-0 p-3';
    toast.style.zIndex = '5';
    toast.innerHTML = `
        <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header bg-success text-white">
                <strong class="me-auto">Success</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    // Add to document
    document.body.appendChild(toast);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.remove();
    }, 3000);
}
function loadOrderSummary() {
    const orderSummaryContainer = document.getElementById('orderSummary');
    if (!orderSummaryContainer) return;

    if (cart.length === 0) {
        orderSummaryContainer.innerHTML = `
            <div class="alert alert-warning">
                Your cart is empty. <a href="products.html">Continue shopping</a>
            </div>
        `;
        return;
    }

    const subtotal = cart.reduce((total, item) => total + (item.price * item.quantity), 0);
    const shipping = subtotal > 0 ? 10 : 0;
    const tax = subtotal * 0.13;
    const total = subtotal + shipping + tax;

    orderSummaryContainer.innerHTML = `
        <div class="mb-3">
            ${cart.map(item => `
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <div>
                        <h6 class="mb-0">${item.name}</h6>
                        <small class="text-muted">Qty: ${item.quantity}</small>
                    </div>
                    <span>$${(item.price * item.quantity).toFixed(2)}</span>
                </div>
            `).join('')}
        </div>
        <hr>
        <div class="d-flex justify-content-between mb-2">
            <span>Subtotal</span>
            <span>$${subtotal.toFixed(2)}</span>
        </div>
        <div class="d-flex justify-content-between mb-2">
            <span>Shipping</span>
            <span>$${shipping.toFixed(2)}</span>
        </div>
        <div class="d-flex justify-content-between mb-2">
            <span>Tax (13%)</span>
            <span>$${tax.toFixed(2)}</span>
        </div>
        <hr>
        <div class="d-flex justify-content-between mb-2">
            <strong>Total</strong>
            <strong>$${total.toFixed(2)}</strong>
        </div>
    `;
}
document.addEventListener("DOMContentLoaded", function () {
    // Check if we're on the login page
    if (window.location.pathname.includes("login.html")) {
        const loginForm = document.getElementById("loginForm");

        loginForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value.trim();

            if (email === "" || password === "") {
                alert("Please enter both email and password");
                return;
            }

            // Simulated login check (hardcoded for now)
            const dummyUser = {
                email: "user@example.com",
                password: "123456"
            };

            if (email === dummyUser.email && password === dummyUser.password) {
                alert("Login successful!");
                // Redirect to user profile or homepage
                window.location.href = "user.html";
            } else {
                alert("Invalid credentials. Please try again");
            }
        });
    }
});

