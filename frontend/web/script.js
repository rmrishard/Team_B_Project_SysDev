// script.js

const API_BASE_URL = "https://www.yallahabibi.online/api/v1";

let allProducts = []; // all products from API or fallback
let filteredProducts = []; // products after filtering
let currentPage = 1;
const pageSize = 9;

document.addEventListener("DOMContentLoaded", () => {
  initializeApp();
});


function initializeApp() {
  loadCartCount();

  if (window.location.pathname.endsWith("products.html")) {
    const categoryParam = new URLSearchParams(window.location.search).get("category");
    if (categoryParam) document.getElementById("categoryFilter").value = categoryParam;
    loadProducts();
  }

  if (document.getElementById("registrationForm")) setupRegistrationForm();
  if (document.getElementById("contactForm")) setupContactForm();
  if (window.location.pathname.endsWith("cart.html")) loadCartItems();
  if (window.location.pathname.endsWith("checkout.html")) loadOrderSummary();
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
  const searchTerm = document.getElementById("productSearch").value.toLowerCase().trim();
  const category = document.getElementById("categoryFilter").value;
  const sort = document.getElementById("sortProducts").value;

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
    let imgSrc = null;
    if ( Array.isArray(product.image)){
        imgSrc = product.image.at(0)["url"];
    } else if (product.image) {
        imgSrc = product.image.url;
    }

    imgSrc = imgSrc || "products/placeholder.jpg";

    const card = `
      <div class="col">
        <div class="card h-100">
          <img src="${imgSrc}" class="card-img-top" alt="${product.name}" style="height: 200px; object-fit: cover; cursor: pointer;" onclick="showProductDetail('${product.id}')">
          <div class="card-body">
            <h5 class="card-title">${product.name}</h5>
            <p class="card-text">${product.description}</p>
            <span class="fw-bold">${product.price} CAD</span>
          </div>
          <div class="card-footer bg-white border-0">
            <button class="btn btn-danger w-100" onclick="addToCart('${product.id}')">Add to Cart</button>
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

  const imgSrc = product.image || "products/placeholder.jpg";
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
        <p><strong>Price:</strong> ${product.price} CAD</p>
        <button class="btn btn-danger mt-3" onclick="addToCart('${product.id}')">Add to Cart</button>
      </div>
    </div>
  `;
  modal.show();
}

// =========================
// Cart Logic
// =========================

let cart = JSON.parse(localStorage.getItem("cart")) || [];



function addToCart(productId, quantity = 1) {
  getProductById(productId).then(product => {
    if (!product) return alert("Product not found");
    if (!product.available) return alert("Product unavailable");

    const existingItem = cart.find(item => item.id === productId);
    if (existingItem) {
      existingItem.quantity += quantity;
    } else {
      cart.push({
        id: product.id,
        name: product.name,
        price: parseFloat(product.price),
        image: product.image || "products/placeholder.jpg",
        quantity
      });
    }

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
  const badge = document.getElementById("cart-count");
  if (badge) badge.textContent = count;
}

// ✅ Main cart loader for cart.html
function loadCartItems() {
  const container = document.getElementById("cart-items");
  container.innerHTML = "";
  let total = 0;

  if (cart.length === 0) {
    container.innerHTML = `
      <div class="text-center py-5">
        <i class="fas fa-shopping-cart fa-3x text-muted mb-3"></i>
        <h5 class="text-muted">Your cart is empty</h5>
        <a href="products.html" class="btn btn-danger mt-3">Start Shopping</a>
      </div>
    `;
    document.getElementById("cart-total").textContent = `0.00 CAD`;
    return;
  }

  cart.forEach(item => {
    const itemTotal = item.price * item.quantity;
    total += itemTotal;

    container.innerHTML += `
      <div class="row align-items-center mb-3 border-bottom pb-2">
        <div class="col-3 col-md-2">
          <img src="${item.image}" alt="${item.name}" class="img-fluid rounded">
        </div>
        <div class="col-5 col-md-6">
          <h5>${item.name}</h5>
          <p class="text-muted mb-0">${item.quantity} × ${item.price.toFixed(2)} CAD</p>
        </div>
        <div class="col-2">
          <h6>${(itemTotal).toFixed(2)} CAD</h6>
        </div>
        <div class="col-2 text-end">
          <button class="btn btn-sm btn-outline-danger" onclick="removeFromCart('${item.id}')">
            <i class="fas fa-trash"></i>
          </button>
        </div>
      </div>
    `;
  });

  document.getElementById("cart-total").textContent = `${total.toFixed(2)} CAD`;
}

// Remove product from cart
function removeFromCart(productId) {
  cart = cart.filter(item => item.id !== productId);
  updateCartStorage();
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
  form.addEventListener("submit", e => {
    e.preventDefault();
    alert("📩 Message sent!");
    form.reset();
  });
}


function setupRegistrationForm() {
  const form = document.getElementById("registrationForm");
  form.addEventListener("submit", e => {
    e.preventDefault();
    alert("✅ Registered!");
    form.reset();
  });
}
// =========================
// Filter + Sort + Pagination Enhancements
// =========================

document.addEventListener("DOMContentLoaded", () => {
  const categoryFilter = document.getElementById("categoryFilter");
  if (categoryFilter) {
    categoryFilter.addEventListener("change", () => {
      filterProducts();
      renderPagination();
    });
  }

  const sortBy = document.getElementById("sortBy");
  if (sortBy) {
    sortBy.addEventListener("change", () => {
      sortProducts(sortBy.value);
      renderPagination();
    });
  }
});

function filterProducts() {
  const category = document.getElementById("categoryFilter")?.value;
  filteredProducts = allProducts.filter(p => !category || p.category === category);
  currentPage = 1;
  sortProducts(document.getElementById("sortBy")?.value || "");
  renderProductsPage(currentPage);
  renderPagination();
}

function sortProducts(criteria) {
  if (!filteredProducts) return;
  if (criteria === "priceAsc") {
    filteredProducts.sort((a, b) => a.price - b.price);
  } else if (criteria === "priceDesc") {
    filteredProducts.sort((a, b) => b.price - a.price);
  } else if (criteria === "name") {
    filteredProducts.sort((a, b) => a.name.localeCompare(b.name));
  }
}

function renderPagination() {
  const pagination = document.getElementById("pagination");
  if (!pagination) return;
  pagination.innerHTML = "";

  const totalPages = Math.ceil(filteredProducts.length / pageSize);
  for (let i = 1; i <= totalPages; i++) {
    const btn = document.createElement("button");
    btn.textContent = i;
    btn.className = "btn btn-outline-secondary m-1";
    if (i === currentPage) btn.classList.add("active");
    btn.addEventListener("click", () => {
      currentPage = i;
       renderProductsPage(currentPage);
    });
    pagination.appendChild(btn);
  }
}
