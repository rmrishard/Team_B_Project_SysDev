// script.js

const API_BASE_URL = "https://www.yallahabibi.online/api/v1";

let allProducts = []; // all products from API or fallback
let filteredProducts = []; // products after filtering
let currentPage = 1;
const pageSize = 9;


// UPDATED: Initialize app with proper cart loading
document.addEventListener("DOMContentLoaded", () => {
  initializeApp();
});

function initializeApp() {
  // UPDATED: Load cart from localStorage first
  cart = JSON.parse(localStorage.getItem("cart")) || [];
  loadCartCount();

  //UPDATED: Ping the API to get session and existing cart information
  let serverCart = null;
  try {
    fetch(`${API_BASE_URL}/shop/cart/`).then(function(resp){
      if (!resp.ok) throw new Error("API failed");
      return resp.json()
    }).then(function(data){
          console.log(data);  //This is what it looks like
          serverCart = data;
    });
  } catch (error) {
      console.warn("API Request failure:", error);
  }
  //END Server cart fetch and API ping

  if (window.location.pathname.endsWith("products.html")) {
    const categoryParam = new URLSearchParams(window.location.search).get("category");
    if (categoryParam) document.getElementById("categoryFilter").value = categoryParam;
    loadProducts();
  }

  if (document.getElementById("registrationForm")) { setupRegistrationForm() ;
      // ADDED: Live password strength indicator on registration page
  const passwordInput = document.getElementById('password');

  // Only run this if the password field exists
  if (passwordInput) {
    passwordInput.addEventListener('input', function () {
      const password = this.value;

      // Get the strength bar and message elements
      const bar = document.getElementById('password-strength-bar');
      const text = document.getElementById('password-strength-text');

      // Initialize strength score
      let strength = 0;

      // Evaluate password rules and add strength points
      if (password.length >= 8) strength += 25;                  // Length check
      if (/[A-Z]/.test(password)) strength += 25;                // Uppercase check
      if (/[0-9]/.test(password)) strength += 25;                // Number check
      if (/[^A-Za-z0-9]/.test(password)) strength += 25;         // Special character check

      // Update progress bar width
      bar.style.width = `${strength}%`;

      // Reset previous class
      bar.className = 'progress-bar';

      // Update strength color and label
      if (strength < 50) {
        bar.classList.add('bg-danger');
        text.textContent = 'Weak password';
      } else if (strength < 75) {
        bar.classList.add('bg-warning');
        text.textContent = 'Moderate password';
      } else {
        bar.classList.add('bg-success');
        text.textContent = 'Strong password';
      }
    });
  }
  }
  if (document.getElementById("contactForm")) setupContactForm();
  if (window.location.pathname.endsWith("cart.html")) loadCartItems();
  if (window.location.pathname.endsWith("checkout.html")) loadOrderSummary();
  
  // ADDED: Initialize order confirmation page
  if (window.location.pathname.endsWith("order-confirmation.html")) {
    loadOrderConfirmation();
  }
  
  // ADDED: Set current year in footer
  const yearElement = document.getElementById("year");
  if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
  }
}

// =========================
// Load Products
// =========================

async function loadProducts() {
  const container = document.getElementById("product-list");
  document.getElementById("loading-products").style.display = "block";
  document.getElementById("no-products-found").style.display = "none";
  container.innerHTML = "";
  allProducts = [];

  try {
    const response = await fetch(`${API_BASE_URL}/products/`);
    if (!response.ok) throw new Error("API failed");
    allProducts = await response.json();
  } catch (error) {
    try {
      const fallback = await fetch("products.json");
      const fallbackData = await fallback.json();
      allProducts = fallbackData.products || [];
      console.warn("Using fallback products.json due to API failure:", error);
    } catch {
      container.innerHTML = `<p>Could not load products.</p>`;
      return;
    }
  }

  allProducts = allProducts.filter(p => p.available && p.visible);
  document.getElementById("loading-products").style.display = "none";
  filterProducts(); // show first page of filtered
}

// =========================
// Filtering, Sorting, Pagination
// =========================

function filterProducts() {
  const searchTerm = document.getElementById("productSearch")?.value.toLowerCase().trim() || "";
  const category = document.getElementById("categoryFilter")?.value || "";
  const sort = document.getElementById("sortBy")?.value || "";

  filteredProducts = allProducts.filter(product => {
    const nameMatch = product.name.toLowerCase().includes(searchTerm);
    const categoryMatch = !category || product.details?.type === category;
    return nameMatch && categoryMatch;
  });

  switch (sort) {
    case "price-asc":
      filteredProducts.sort((a, b) => a.price - b.price);
      break;
    case "price-desc":
      filteredProducts.sort((a, b) => b.price - a.price);
      break;
    case "name-asc":
      filteredProducts.sort((a, b) => a.name.localeCompare(b.name));
      break;
    case "name-desc":
      filteredProducts.sort((a, b) => b.name.localeCompare(a.name));
      break;
  }

  currentPage = 1;
  renderProductsPage(currentPage);
  renderPagination();
}

function renderProductsPage(page) {
  const container = document.getElementById("product-list");
  container.innerHTML = "";

  const start = (page - 1) * pageSize;
  const end = start + pageSize;
  const productsToShow = filteredProducts.slice(start, end);

  if (productsToShow.length === 0) {
    document.getElementById("no-products-found").style.display = "block";
    return;
  } else {
    document.getElementById("no-products-found").style.display = "none";
  }

  productsToShow.forEach(product => {
    // UPDATED: Better image handling for product display
    let imgSrc = "products/placeholder.jpg"; // default fallback
    
    if (Array.isArray(product.image) && product.image.length > 0) {
      imgSrc = product.image[0].url || product.image[0];
    } else if (product.image && typeof product.image === 'object') {
      imgSrc = product.image.url;
    } else if (product.image && typeof product.image === 'string') {
      imgSrc = product.image;
    }

    
    const card = `
      <div class="col">
        <div class="card h-100">
          <img src="${imgSrc}" class="card-img-top" alt="${product.name}" style="height: 200px; object-fit: cover; cursor: pointer;" onclick="showProductDetail('${product.id}')">
          <div class="card-body">
            <h5 class="card-title">${product.name}</h5>
            <p class="card-text">${product.description}</p>
            <span class="fw-bold">$${product.price} CAD</span>
          </div>
          <div class="card-footer bg-white border-0">
            <button class="btn btn-danger w-100" onclick="addToCart('${product.id}')">Add to Cart</button>
              <button class="btn btn-outline-danger w-100" onclick="addToWishlist('${product.id}')">
    <i class="fas fa-heart"></i> Add to Wishlist
  </button>

          </div>
        </div>
      </div>
    `;
    container.innerHTML += card;
  });
}

function renderPagination() {
  const totalPages = Math.ceil(filteredProducts.length / pageSize);
  const container = document.getElementById("pagination");
  if (!container) return;
  container.innerHTML = "";

  for (let i = 1; i <= totalPages; i++) {
    container.innerHTML += `
      <li class="page-item ${i === currentPage ? "active" : ""}">
        <button class="page-link" onclick="goToPage(${i})">${i}</button>
      </li>
    `;
  }
}

function goToPage(page) {
  currentPage = page;
  renderProductsPage(currentPage);
  renderPagination();
}

// =========================
// Product Detail Modal
// =========================

async function showProductDetail(productId) {
  const modal = new bootstrap.Modal(document.getElementById("productDetailModal"));
  const content = document.getElementById("productDetailContent");
  const product = await getProductById(productId);

  if (!product) return;

  // UPDATED: Better image handling for modal
  let imgSrc = "products/placeholder.jpg";
  if (Array.isArray(product.image) && product.image.length > 0) {
    imgSrc = product.image[0].url || product.image[0];
  } else if (product.image && typeof product.image === 'object') {
    imgSrc = product.image.url;
  } else if (product.image && typeof product.image === 'string') {
    imgSrc = product.image;
  }

  content.innerHTML = `
    <div class="row">
      <div class="col-md-5">
        <img src="${imgSrc}" alt="${product.name}" class="img-fluid rounded">
      </div>
      <div class="col-md-7">
        <h3>${product.name}</h3>
        <p>${product.description}</p>
        <p><strong>Origin:</strong> ${product.origin || "N/A"}</p>
        <p><strong>Type:</strong> ${product.details?.type || "N/A"}</p>
        <p><strong>Price:</strong> $${product.price} CAD</p>
        <button class="btn btn-danger mt-3" onclick="addToCart('${product.id}')">Add to Cart</button>
        <button class="btn btn-outline-danger mt-3" onclick="addToWishlist('${product.id}')">
          <i class="fas fa-heart"></i> Add to Wishlist
        </button>
      </div>
    </div>
  `;
  modal.show();
}

// =========================
// Cart Logic
// =========================

let cart = JSON.parse(localStorage.getItem("cart")) || [];

/* Code added to support API */
const CartModifyRequest = class {
  constructor(product_id, quantity) {
    this.data = {}
    this.data["product_id"] = product_id; //UUID
    this.data["quantity"] = quantity;     //Integer
  }

  async send() {
    let response = false;
    try {
      response = await fetch(`${API_BASE_URL}/shop/cart/modify`, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.data)
      });
      if (!response.ok) throw new Error("API failed");
    } catch (error) {
      console.warn("Operation failed due to API failure:", error);
    }
  }
}
/* End API support code */

// UPDATED: Better image handling when adding to cart
function addToCart(productId, quantity = 1) {
  getProductById(productId).then(product => {
    if (!product) return alert("Product not found");
    if (!product.available) return alert("Product unavailable");

    // UPDATED: Better image extraction for cart storage
    let productImage = "products/placeholder.jpg";
    if (Array.isArray(product.image) && product.image.length > 0) {
      productImage = product.image[0].url || product.image[0];
    } else if (product.image && typeof product.image === 'object') {
      productImage = product.image.url;
    } else if (product.image && typeof product.image === 'string') {
      productImage = product.image;
    }

    let cartItem = cart.find(item => item.id === productId);
    if (cartItem) {
      cartItem.quantity += quantity;
    } else {
      cartItem = {
        id: product.id,
        name: product.name,
        price: parseFloat(product.price),
        image: productImage,
        quantity: quantity,
        description: product.description || ""
      };
      cart.push(cartItem);
    }

    //Make a request to the API
    const updateCart = new CartModifyRequest(cartItem.id,quantity)
    updateCart.send(); //Ignore result for now

    updateCartStorage();
    alert(`🛒 ${product.name} added to cart!`);
    
    if (confirm("🛒 Product added to cart! Would you like to view your cart now?")) {
      window.location.href = "cart.html";
    }
  });
}


// Save cart and refresh UI
function updateCartStorage() {
  localStorage.setItem("cart", JSON.stringify(cart));
  loadCartCount();
  if (window.location.pathname.endsWith("cart.html")) loadCartItems();
  if (window.location.pathname.endsWith("checkout.html")) loadOrderSummary();
}

// Display total item count in navbar
function loadCartCount() {
  const count = cart.reduce((sum, item) => sum + item.quantity, 0);
  const badges = document.querySelectorAll("#cart-count, #cartCount");
  badges.forEach(badge => {
    if (badge) badge.textContent = count;
  });
}

// UPDATED: Complete cart items loader with proper image display and order summary
function loadCartItems() {
  const container = document.getElementById("cart-items");
  if (!container) return;
  
  container.innerHTML = "";

  if (cart.length === 0) {
    container.innerHTML = `
      <div class="card-body text-center py-5">
        <i class="fas fa-shopping-cart fa-3x text-muted mb-3"></i>
        <h5 class="text-muted">Your cart is empty</h5>
        <p class="text-muted">Add some products to get started!</p>
        <a href="products.html" class="btn btn-danger mt-3">Start Shopping</a>
      </div>
    `;
    updateOrderSummary(0, 0, 0, 0);
    return;
  }

  // UPDATED: Better cart item display with quantity controls
  let cartHTML = '<div class="card-body">';
  cart.forEach((item, index) => {
    const itemTotal = item.price * item.quantity;
    
    cartHTML += `
      <div class="row align-items-center mb-3 pb-3 ${index < cart.length - 1 ? 'border-bottom' : ''}">
        <div class="col-3 col-md-2">
          <img src="${item.image}" alt="${item.name}" class="img-fluid rounded" style="max-height: 80px; object-fit: cover;">
        </div>
        <div class="col-6 col-md-5">
          <h6 class="mb-1">${item.name}</h6>
          <p class="text-muted small mb-2">${item.description ? item.description.substring(0, 50) + '...' : ''}</p>
          <p class="text-muted mb-0">$${item.price.toFixed(2)} CAD each</p>
        </div>
        <div class="col-3 col-md-2">
          <div class="input-group input-group-sm">
            <button class="btn btn-outline-secondary" type="button" onclick="updateQuantity('${item.id}', ${item.quantity - 1})">-</button>
            <input type="text" class="form-control text-center" value="${item.quantity}" readonly>
            <button class="btn btn-outline-secondary" type="button" onclick="updateQuantity('${item.id}', ${item.quantity + 1})">+</button>
          </div>
        </div>
        <div class="col-6 col-md-2 mt-2 mt-md-0">
          <h6 class="mb-0">$${itemTotal.toFixed(2)}</h6>
        </div>
        <div class="col-6 col-md-1 mt-2 mt-md-0 text-end">
          <button class="btn btn-sm btn-outline-danger" onclick="confirmRemoveItem('${item.id}', '${item.name}')" title="Remove item">
            <i class="fas fa-trash"></i>
          </button>
        </div>
      </div>
    `;
  });
  cartHTML += '</div>';
  
  container.innerHTML = cartHTML;
  
  // UPDATED: Calculate and update order summary
  const subtotal = cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  const shipping = subtotal > 50 ? 0 : 10; // Free shipping over $50
  const tax = subtotal * 0.13; // 13% tax
  const total = subtotal + shipping + tax;
  
  updateOrderSummary(subtotal, shipping, tax, total);
}

// ADDED: Update quantity function
function updateQuantity(productId, newQuantity) {
  //Make a request to the API
  const updateCart = new CartModifyRequest(productId,newQuantity)
  updateCart.send(); //Ignore result for now


  if (newQuantity <= 0) {
    const item = cart.find(item => item.id === productId);
    if (item) {
      confirmRemoveItem(productId, item.name);
    }
    return;
  }
  
  const item = cart.find(item => item.id === productId);
  if (item) {
    item.quantity = newQuantity;
    updateCartStorage();
  }
}

// ADDED: Confirm remove item with modal
function confirmRemoveItem(productId, productName) {
  const modal = new bootstrap.Modal(document.getElementById("removeItemModal"));
  const modalBody = document.querySelector("#removeItemModal .modal-body");
  modalBody.textContent = `Are you sure you want to remove "${productName}" from your cart?`;
  
  const confirmButton = document.getElementById("confirmRemove");
  confirmButton.onclick = () => {
    removeFromCart(productId);
    modal.hide();
  };
  
  modal.show();
}

// UPDATED: Remove product from cart
function removeFromCart(productId) {
  //Make a request to the API
  const updateCart = new CartModifyRequest(productId,0) //Zero triggers removal
  updateCart.send(); //Ignore result for now

  cart = cart.filter(item => item.id !== productId);
  updateCartStorage();
  
  // Show success message
  const toast = document.createElement('div');
  toast.className = 'toast-container position-fixed top-0 end-0 p-3';
  toast.innerHTML = `
    <div class="toast show" role="alert">
      <div class="toast-header">
        <strong class="me-auto">Cart Updated</strong>
        <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
      </div>
      <div class="toast-body">
        Item removed from cart successfully!
      </div>
    </div>
  `;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}

// ADDED: Update order summary in cart page
function updateOrderSummary(subtotal, shipping, tax, total) {
  const subtotalElement = document.getElementById("subtotal");
  const shippingElement = document.getElementById("shipping");
  const taxElement = document.getElementById("tax");
  const totalElement = document.getElementById("total");
  
  if (subtotalElement) subtotalElement.textContent = `$${subtotal.toFixed(2)}`;
  if (shippingElement) shippingElement.textContent = `$${shipping.toFixed(2)}`;
  if (taxElement) taxElement.textContent = `$${tax.toFixed(2)}`;
  if (totalElement) totalElement.textContent = `$${total.toFixed(2)}`;
}

// ADDED: Checkout function
function checkout() {
  if (cart.length === 0) {
    alert("Your cart is empty! Please add some items before checkout.");
    return;
  }
  
  // Store checkout data for the checkout page
  const checkoutData = {
    items: cart,
    subtotal: cart.reduce((total, item) => total + (item.price * item.quantity), 0),
    timestamp: new Date().toISOString()
  };
  
  localStorage.setItem("checkoutData", JSON.stringify(checkoutData));
  window.location.href = "checkout.html";
}

// UPDATED: Load order summary for checkout page
function loadOrderSummary() {
  const orderSummaryContainer = document.getElementById('orderSummary');
  if (!orderSummaryContainer) return;

  if (cart.length === 0) {
    orderSummaryContainer.innerHTML = `
      <div class="alert alert-warning">
        <i class="fas fa-exclamation-triangle me-2"></i>
        Your cart is empty. <a href="products.html" class="alert-link">Continue shopping</a>
      </div>
    `;
    return;
  }

  const subtotal = cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  const shipping = subtotal > 50 ? 0 : 10;
  const tax = subtotal * 0.13;
  const total = subtotal + shipping + tax;

  orderSummaryContainer.innerHTML = `
    <div class="mb-3">
      ${cart.map(item => `
        <div class="d-flex justify-content-between align-items-center mb-2 pb-2 border-bottom">
          <div class="d-flex align-items-center">
            <img src="${item.image}" alt="${item.name}" class="me-2 rounded" style="width: 40px; height: 40px; object-fit: cover;">
            <div>
              <h6 class="mb-0 small">${item.name}</h6>
              <small class="text-muted">Qty: ${item.quantity}</small>
            </div>
          </div>
          <span class="fw-bold">$${(item.price * item.quantity).toFixed(2)}</span>
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
      <span class="text-success">${shipping === 0 ? 'FREE' : '$' + shipping.toFixed(2)}</span>
    </div>
    <div class="d-flex justify-content-between mb-2">
      <span>Tax (13%)</span>
      <span>$${tax.toFixed(2)}</span>
    </div>
    <hr>
    <div class="d-flex justify-content-between mb-2">
      <strong>Total</strong>
      <strong class="text-danger">$${total.toFixed(2)}</strong>
    </div>
    ${shipping === 0 ? '<small class="text-success"><i class="fas fa-truck me-1"></i>Free shipping applied!</small>' : '<small class="text-muted">Free shipping on orders over $50</small>'}
  `;
}

// ADDED: Process order function
function processOrder() {
  const form = document.getElementById('checkoutForm');
  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }
  
  if (cart.length === 0) {
    alert("Your cart is empty!");
    return;
  }
  
  // Simulate order processing
  const orderData = {
    orderId: 'ORD-' + Date.now(),
    items: cart,
    total: cart.reduce((total, item) => total + (item.price * item.quantity), 0),
    orderDate: new Date().toISOString(),
    customerInfo: {
      firstName: form.querySelector('input[type="text"]').value,
      lastName: form.querySelectorAll('input[type="text"]')[1].value,
      email: form.querySelector('input[type="email"]').value,
      phone: form.querySelector('input[type="tel"]').value,
      address: form.querySelectorAll('input[type="text"]')[2].value,
      city: form.querySelectorAll('input[type="text"]')[3].value,
      province: form.querySelectorAll('input[type="text"]')[4].value,
      postalCode: form.querySelectorAll('input[type="text"]')[5].value
    }
  };
  
  // Store order data and clear cart
  localStorage.setItem('lastOrder', JSON.stringify(orderData));
  localStorage.removeItem('cart');
  cart = [];
  
  // Redirect to confirmation page
  window.location.href = 'order-confirmation.html';
}

// ADDED: Load order confirmation
function loadOrderConfirmation() {
  const lastOrder = JSON.parse(localStorage.getItem('lastOrder'));
  if (!lastOrder) {
    document.querySelector('.container').innerHTML = `
      <div class="text-center py-5">
        <h2>No Order Found</h2>
        <p>We couldn't find your order details.</p>
        <a href="products.html" class="btn btn-danger">Continue Shopping</a>
      </div>
    `;
    return;
  }
  
  // Set order date
  const orderDate = new Date(lastOrder.orderDate);
  const deliveryDate = new Date(orderDate.getTime() + (5 * 24 * 60 * 60 * 1000)); // 5 days later
  
  document.getElementById('orderDate').textContent = orderDate.toLocaleDateString();
  document.getElementById('deliveryDate').textContent = deliveryDate.toLocaleDateString();
  
  // Load order summary
  const subtotal = lastOrder.items.reduce((total, item) => total + (item.price * item.quantity), 0);
  const shipping = subtotal > 50 ? 0 : 10;
  const tax = subtotal * 0.13;
  const total = subtotal + shipping + tax;
  
  document.getElementById('orderSummary').innerHTML = `
    <div class="mb-3">
      ${lastOrder.items.map(item => `
        <div class="d-flex justify-content-between align-items-center mb-2 pb-2 border-bottom">
          <div class="d-flex align-items-center">
            <img src="${item.image}" alt="${item.name}" class="me-2 rounded" style="width: 50px; height: 50px; object-fit: cover;">
            <div>
              <h6 class="mb-0">${item.name}</h6>
              <small class="text-muted">Qty: ${item.quantity} × $${item.price.toFixed(2)}</small>
            </div>
          </div>
          <span class="fw-bold">$${(item.price * item.quantity).toFixed(2)}</span>
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
    <div class="d-flex justify-content-between">
      <strong>Total</strong>
      <strong class="text-success">$${total.toFixed(2)}</strong>
    </div>
  `;
  
  // Load addresses
  const customer = lastOrder.customerInfo;
  const addressHTML = `
    <strong>${customer.firstName} ${customer.lastName}</strong><br>
    ${customer.address}<br>
    ${customer.city}, ${customer.province} ${customer.postalCode}<br>
    <strong>Phone:</strong> ${customer.phone}<br>
    <strong>Email:</strong> ${customer.email}
  `;
  
  document.getElementById('shippingAddress').innerHTML = addressHTML;
  document.getElementById('billingAddress').innerHTML = addressHTML;
}

// =========================
// Utilities
// =========================

async function getProductById(productId) {
  try {
    const response = await fetch(`${API_BASE_URL}/products/${productId}`);
    if (!response.ok) throw new Error("Not found");
    return await response.json();
  } catch {
    return allProducts.find(p => p.id === productId) || null;
  }
}

function setupContactForm() {
  const form = document.getElementById("contactForm");
  if (form) {
    form.addEventListener("submit", e => {
      e.preventDefault();
      alert("📩 Message sent!");
      form.reset();
    });
  }
}

function setupRegistrationForm() {
  const form = document.getElementById("registrationForm");
  if (form) {
    form.addEventListener("submit", e => {
      e.preventDefault();
      alert("✅ Registered!");
      form.reset();
    });
  }
}

// =========================
// Filter + Sort + Pagination Enhancements
// =========================

document.addEventListener("DOMContentLoaded", () => {
  const categoryFilter = document.getElementById("categoryFilter");
  if (categoryFilter) {
    categoryFilter.addEventListener("change", filterProducts);
  }

  const sortBy = document.getElementById("sortBy");
  if (sortBy) {
    sortBy.addEventListener("change", filterProducts);
  }
  
  const productSearch = document.getElementById("productSearch");
  if (productSearch) {
    productSearch.addEventListener("input", filterProducts);
  }
  
});
// =========================
// Toggle Password Visibility 
// =========================

function togglePassword(inputId) {
  const input = document.getElementById(inputId);
  const icon = input?.nextElementSibling?.querySelector("i");

  if (!input || !icon) return;

  if (input.type === "password") {
    input.type = "text";
    icon.classList.remove("fa-eye");
    icon.classList.add("fa-eye-slash");
  } else {
    input.type = "password";
    icon.classList.remove("fa-eye-slash");
    icon.classList.add("fa-eye");
  }
}
//START OF BACKEND-INTEGRATED SECTION

// ========== User Registration ==========
async function registerUser(userData) {
  try {
    const response = await fetch(`${API_BASE_URL}/users/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });

    const result = await response.json();
    if (!response.ok) throw new Error(result.message || "Registration failed");
    return result;
  } catch (error) {
    throw new Error("Registration error: " + error.message);
  }
}

// ========== User Login ==========
async function loginUser(email, password) {
  try {
    const response = await fetch(`${API_BASE_URL}/users/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    const result = await response.json();
    if (!response.ok) throw new Error(result.message || "Login failed");

    // Store JWT or session token locally
    localStorage.setItem("authToken", result.token);
    localStorage.setItem("userEmail", email);
    return result;
  } catch (error) {
    throw new Error("Login error: " + error.message);
  }
}

// ========== Authenticated Fetch Helper ==========
function getAuthHeaders() {
  const token = localStorage.getItem("authToken");
  return {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  };
}

// ========== Cart Persistence API ==========
async function saveCartToServer(cartData) {
  try {
    const response = await fetch(`${API_BASE_URL}/cart/save`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(cartData)
    });
    return await response.json();
  } catch (error) {
    console.error("Error saving cart:", error.message);
  }
}

async function fetchCartFromServer() {
  try {
    const response = await fetch(`${API_BASE_URL}/cart`, {
      method: 'GET',
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error("Failed to fetch cart");
    return await response.json();
  } catch (error) {
    console.error("Error loading cart:", error.message);
    return [];
  }
}

// ========== Order Submission ==========
async function submitOrder(orderData) {
  try {
    const response = await fetch(`${API_BASE_URL}/orders`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(orderData)
    });

    const result = await response.json();
    if (!response.ok) throw new Error(result.message || "Order failed");
    return result;
  } catch (error) {
    throw new Error("Order submission error: " + error.message);
  }
}
// =========================
// USER DASHBOARD LOGIC
// =========================

function initializeUserDashboard() {
  const isLoggedIn = localStorage.getItem('isLoggedIn');
  const userEmail = localStorage.getItem('userEmail');

  if (!isLoggedIn || !userEmail) {
    window.location.href = 'login.html';
    return;
  }

  document.getElementById('userName').textContent = userEmail.split('@')[0];
  document.getElementById('userEmail').textContent = userEmail;
  const profileEmailInput = document.getElementById('profileEmail');
  if (profileEmailInput) profileEmailInput.value = userEmail;

  document.getElementById('logoutBtn')?.addEventListener('click', function (e) {
    e.preventDefault();
    localStorage.clear();
    window.location.href = 'login.html';
  });

  const profileForm = document.getElementById('profileForm');
  if (profileForm) {
    profileForm.addEventListener('submit', async function (e) {
      e.preventDefault();
      profileForm.classList.add('was-validated');

      if (profileForm.checkValidity()) {
        // Simulated backend update
        showSuccessToast('Profile updated successfully.');
      }
    });
  }

  loadOrders();
  loadAddresses();
  loadWishlist();
}

async function loadOrders() {
  try {
    const response = await fetch(`${API_BASE_URL}/orders`, {
      method: 'GET',
      headers: getAuthHeaders()
    });
    const orders = await response.json();
    const tbody = document.getElementById('recentOrdersTableBody');
    if (!orders.length) {
      tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No recent orders found.</td></tr>';
      return;
    }

    tbody.innerHTML = orders.slice(0, 5).map(order => `
      <tr>
        <td>${order.orderId}</td>
        <td>${new Date(order.orderDate).toLocaleDateString()}</td>
        <td>${order.status}</td>
        <td>$${order.total.toFixed(2)}</td>
        <td>
          <button class="btn btn-sm btn-outline-danger" onclick="viewOrderDetails('${order.orderId}')">
            View
          </button>
        </td>
      </tr>`).join('');
  } catch (error) {
    console.error('Failed to load orders:', error);
  }
}

// Fetch full order details by orderId 
async function fetchOrderDetails(orderId) {
  try {
    const response = await fetch(`${API_BASE_URL}/orders/${orderId}`, {
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error("Failed to load order details");
    return await response.json();
  } catch (error) {
    console.error("fetchOrderDetails error:", error);
    return null;
  }
}

// Render full order detail into the modal
function renderOrderDetails(order) {
  if (!order) return "<div class='text-danger'>Order not found.</div>";
  return `
    <h5>Order #${order.orderId}</h5>
    <p><strong>Date:</strong> ${new Date(order.orderDate).toLocaleDateString()}</p>
    <p><strong>Status:</strong> ${order.status}</p>
    <ul class="list-group mb-3">
      ${order.items.map(item => `
        <li class="list-group-item d-flex justify-content-between align-items-center">
          <div>
            <strong>${item.name}</strong><br>
            <small>Qty: ${item.quantity} × $${item.price.toFixed(2)}</small>
          </div>
          <span>$${(item.price * item.quantity).toFixed(2)}</span>
        </li>
      `).join("")}
    </ul>
    <p><strong>Total:</strong> $${order.total.toFixed(2)}</p>
  `;
}


async function loadAddresses() {
  try {
    const response = await fetch(`${API_BASE_URL}/addresses`, {
      headers: getAuthHeaders()
    });
    const addresses = await response.json();
    const container = document.getElementById('addressList');
    if (!addresses.length) {
      container.innerHTML = '<div class="col-12 text-center text-muted">No addresses found.</div>';
      return;
    }

    container.innerHTML = addresses.map(address => `
      <div class="col-md-6">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <h5 class="card-title">${address.addressName}</h5>
            <p class="card-text">${address.fullName}<br>${address.addressLine1}, ${address.city}, ${address.province} ${address.postalCode}</p>
            <p class="card-text"><strong>Phone:</strong> ${address.phone}</p>
          </div>
        </div>
      </div>`).join('');
  } catch (error) {
    console.error("Error loading addresses:", error);
  }
}

async function loadWishlist() {
  try {
    const response = await fetch(`${API_BASE_URL}/wishlist`, {
      headers: getAuthHeaders()
    });
    const wishlist = await response.json();
    const container = document.getElementById('wishlistItems');

    if (!wishlist.length) {
      document.getElementById("emptyWishlist").style.display = "block";
      container.innerHTML = '';
      return;
    }

    document.getElementById("emptyWishlist").style.display = "none";
    container.innerHTML = wishlist.map(item => `
      <div class="col-md-4">
        <div class="card h-100 border-0 shadow-sm">
          <img src="${item.image}" class="card-img-top" alt="${item.name}">
          <div class="card-body">
            <h4 class="h6">${item.name}</h4>
            <p class="text-danger fw-bold">$${item.price.toFixed(2)}</p>
            <button class="btn btn-sm btn-outline-danger w-100" onclick="addToCart('${item.id}')">
              <i class="fas fa-cart-plus me-1"></i> Add to Cart
            </button>
            <!-- === NEW === Remove from wishlist button -->
            <button class="btn btn-sm btn-link text-danger mt-2" onclick="removeFromWishlist('${item.id}')">
              <i class="fas fa-heart-broken"></i> Remove
            </button>
          </div>
        </div>
      </div>
    `).join('');
  } catch (error) {
    console.error("Error loading wishlist:", error);
  }
}
// Add to wishlist
async function addToWishlist(productId) {
  try {
    const response = await fetch(`${API_BASE_URL}/wishlist`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ productId })
    });
    if (!response.ok) throw new Error("Failed to add to wishlist");
    showSuccessToast("Added to wishlist!");
  } catch (error) {
    console.error("Add to wishlist error:", error);
  }
}

//  Remove from wishlist
async function removeFromWishlist(productId) {
  try {
    const response = await fetch(`${API_BASE_URL}/wishlist/${productId}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to remove from wishlist');
    showSuccessToast('Removed from wishlist!');
    loadWishlist();
  } catch (error) {
    console.error('Remove from wishlist error:', error);
  }
}

function showSuccessToast(message) {
  const toast = document.createElement("div");
  toast.className = 'toast-container position-fixed top-0 end-0 p-3';
  toast.innerHTML = `
    <div class="toast show" role="alert">
      <div class="toast-header">
        <strong class="me-auto">Success</strong>
        <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
      </div>
      <div class="toast-body">${message}</div>
    </div>`;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}

if (window.location.pathname.endsWith("user.html")) {
  document.addEventListener("DOMContentLoaded", initializeUserDashboard);
}
