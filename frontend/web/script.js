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
      allProducts = await fallback.json();
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
    const imgSrc = product.image?.[0]?.url || "products/placeholder.jpg";
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

  const imgSrc = product.image?.[0]?.url || "products/placeholder.jpg";
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
        image: product.image?.[0]?.url || "products/placeholder.jpg",
        quantity
      });
    }

    localStorage.setItem("cart", JSON.stringify(cart));
    loadCartCount();

    //Show confirmation with product name
    alert(`🛒 ${product.name} added to cart!`);

    // Ask if user wants to view cart
    if (confirm("🛒 Product added to cart! Would you like to view your cart now?")) {
      window.location.href = "cart.html";
    }
  });
}



function loadCartCount() {
  const count = cart.reduce((sum, item) => sum + item.quantity, 0);
  const badge = document.getElementById("cart-count");
  if (badge) badge.textContent = count;
}

function loadCartItems() {
  const container = document.getElementById("cart-items");
  let total = 0;
  container.innerHTML = "";

  cart.forEach(item => {
    total += item.price * item.quantity;
    container.innerHTML += `
      <div class="cart-item">
        <img src="${item.image}" alt="${item.name}">
        <h4>${item.name}</h4>
        <p>${item.quantity} × ${item.price} CAD</p>
      </div>
    `;
  });

  document.getElementById("cart-total").textContent = `${total.toFixed(2)} CAD`;
}

function loadOrderSummary() {
  const container = document.getElementById("order-summary");
  let total = 0;
  container.innerHTML = "";

  cart.forEach(item => {
    total += item.price * item.quantity;
    container.innerHTML += `
      <div class="order-item">
        <span>${item.name} (${item.quantity})</span>
        <span>${(item.price * item.quantity).toFixed(2)} CAD</span>
      </div>
    `;
  });

  document.getElementById("order-total").textContent = `${total.toFixed(2)} CAD`;
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
  displayProducts();
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
      displayProducts();
    });
    pagination.appendChild(btn);
  }
}
