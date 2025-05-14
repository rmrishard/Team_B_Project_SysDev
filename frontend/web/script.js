// STARTS WHEN PAGE LOADS
    document.addEventListener("DOMContentLoaded", () => {
    console.log("Yalla Habibi Imports site loaded with Bootstrap!");
    
    // Set current year
    document.getElementById("year").textContent = new Date().getFullYear();
    
    // Load products when on products page
    if (window.location.pathname.endsWith('products.html')) {
        loadProducts();
    }

    // Contact form handling (only on contact page)
    const contactForm = document.getElementById('contactForm');
    if (contactForm) { 
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleFormSubmission(this);
        });
    }
});

// HANDLE FORM SUBMISSION
function handleFormSubmission(form) {
    try {
        //checks if the form is fillwd correctly
        if (!form.checkValidity()) {
            throw new Error('Form validation failed');
        }
        //display success msg
        alert('Thank you for your message! We will get back to you soon.');
        form.reset();
    } catch (error) {
        console.error('Submission error:', error);
        alert('There was an error submitting your message. Please try again.');
    }
}

// LOAD AND SHOW PRODUCTS
async function loadProducts() {
  const productList = document.getElementById("product-list");
  
  try {
    // Show loading state
    productList.innerHTML = `
      <div class="col-12 text-center py-5">
        <div class="spinner-border text-danger" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Loading products...</p>
      </div>
    `;
// fetching product data 
    const response = await fetch('products.json');
    if (!response.ok) throw new Error(`HTTP error! ${response.status}`);
    //get product list
    const data = await response.json();
    if (!data?.products?.length) throw new Error('No products found');
    //create product cards
    productList.innerHTML = data.products.map(product => `
      <div class="col">
        <div class="card h-100 shadow-sm">
          <img src="${product.image}" 
               class="card-img-top p-3 bg-light" 
               alt="${product.name}"
               style="height: 300px; object-fit: contain;"
               onerror="this.onerror=null;this.src='fallback-image.jpg';">
          
          <div class="card-body d-flex flex-column">
            <h3 class="card-title h5 text-danger">${product.name}</h3>
            <p class="card-text flex-grow-1">${product.description}</p>
            
            <div class="mt-auto">
              <div class="d-flex justify-content-between align-items-center">
                <span class="h4 text-primary">$${product.price.toFixed(2)}</span>
                <span class="badge bg-warning text-dark">${product.origin}</span>
              </div>
              
              ${product.details ? `
              <div class="mt-3 border-top pt-2">
                <ul class="list-unstyled small">
                  ${product.details.volume ? `<li><strong>Volume:</strong> ${product.details.volume}</li>` : ''}
                  ${product.details.type ? `<li><strong>Type:</strong> ${product.details.type}</li>` : ''}
                  ${product.details.certification ? `<li><strong>Certification:</strong> ${product.details.certification}</li>` : ''}
                  ${product.details.arabic_text ? `<li class="text-end" dir="rtl" lang="ar">${product.details.arabic_text}</li>` : ''}
                </ul>
              </div>
              ` : ''}
            </div>
          </div>
        </div>
      </div>
    `).join('');


    // SHOW ERROR MESSAGE
  } catch (error) {
    console.error('Loading error:', error);
    productList.innerHTML = `
      <div class="col-12 text-center py-5">
        <div class="alert alert-danger" role="alert">
          <h4 class="alert-heading">⚠️ Error Loading Products</h4>
          <p>${error.message}</p>
          <hr>
          <button class="btn btn-danger" onclick="window.location.reload()">
            Reload Page
          </button>
        </div>
      </div>
    `;
  }
}