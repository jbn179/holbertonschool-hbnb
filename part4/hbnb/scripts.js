// API base URL 
const API_URL = 'http://localhost:5000/api/v1';

/**
 * ===========================
 * AUTHENTICATION FUNCTIONS
 * ===========================
 */

// Authentication token management
function setAuthToken(token) {
  setCookie('auth_token', token);
  try {
    localStorage.setItem('auth_token', token);
  } catch (e) {
    console.error('Failed to store token in localStorage:', e);
  }
}

function getAuthToken() {
  const cookieToken = getCookie('auth_token');
  if (cookieToken) return cookieToken;
  
  try {
    return localStorage.getItem('auth_token');
  } catch (e) {
    console.error('Failed to get token from localStorage:', e);
    return null;
  }
}

function removeAuthToken() {
  deleteCookie('auth_token');
  try {
    localStorage.removeItem('auth_token');
  } catch (e) {
    console.error('Failed to remove token from localStorage:', e);
  }
}

function isAuthenticated() {
  return getAuthToken() !== null;
}

function updateAuthUI() {
  const loginLink = document.getElementById('login-link');
  const logoutLink = document.getElementById('logout-link');
  
  if (isAuthenticated()) {
    if (loginLink) loginLink.style.display = 'none';
    if (logoutLink) {
      logoutLink.style.display = 'inline-block';
      logoutLink.classList.add('logout-button');
    }
  } else {
    if (loginLink) loginLink.style.display = 'inline-block';
    if (logoutLink) logoutLink.style.display = 'none';
  }
}

/**
 * ===========================
 * COOKIE MANAGEMENT
 * ===========================
 */

function setCookie(name, value, days = 7) {
  const expirationDate = new Date();
  expirationDate.setDate(expirationDate.getDate() + days);
  const cookieValue = encodeURIComponent(value) + (days ? `; expires=${expirationDate.toUTCString()}` : '') + '; path=/';
  document.cookie = `${name}=${cookieValue}`;
}

function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [cookieName, cookieValue] = cookie.trim().split('=');
    if (cookieName === name) {
      return decodeURIComponent(cookieValue);
    }
  }
  return null;
}

function deleteCookie(name) {
  setCookie(name, '', -1);
}

/**
 * ===========================
 * UI NOTIFICATIONS
 * ===========================
 */

function showMessage(message, type = 'error') {
  const messageContainer = document.getElementById('message-container');
  if (messageContainer) {
    messageContainer.innerHTML = `<div class="message ${type}">${message}</div>`;
    setTimeout(() => {
      messageContainer.innerHTML = '';
    }, 5000);
  }
}

function showPopupMessage(message, type = 'error', duration = 5000) {
  // Create or find popup container
  let popupContainer = document.querySelector('.popup-message-container');
  if (!popupContainer) {
    popupContainer = document.createElement('div');
    popupContainer.className = 'popup-message-container';
    document.body.appendChild(popupContainer);
  }
  
  // Create popup element
  const popup = document.createElement('div');
  popup.className = `popup-message ${type}`;
  popup.style.opacity = '0';
  popup.style.transform = 'translateY(-20px)';
  
  popup.innerHTML = `
    <span>${message}</span>
    <span class="close-popup">&times;</span>
  `;
  
  popupContainer.appendChild(popup);
  
  // Show popup with animation
  setTimeout(() => {
    popup.style.opacity = '1';
    popup.style.transform = 'translateY(0)';
    popup.style.animation = 'slideInDown 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94), fadeIn 0.5s ease';
  }, 10);
  
  // Add close button handler
  const closeButton = popup.querySelector('.close-popup');
  if (closeButton) {
    closeButton.addEventListener('click', () => {
      popup.style.opacity = '0';
      popup.style.transform = 'translateY(-20px)';
      
      setTimeout(() => {
        if (popup.parentNode) popup.remove();
      }, 500);
    });
  }
  
  // Auto-close after duration
  return new Promise(resolve => {
    setTimeout(() => {
      if (popup.parentNode) {
        popup.style.opacity = '0';
        popup.style.transform = 'translateY(-20px)';
        
        setTimeout(() => {
          if (popup.parentNode) popup.remove();
          resolve();
        }, 500);
      } else {
        resolve();
      }
    }, duration);
  });
}

/**
 * ===========================
 * FORM VALIDATION
 * ===========================
 */

function showInputError(inputId, message) {
  const inputElement = document.getElementById(inputId);
  if (!inputElement) return;
  
  const errorElement = document.createElement('div');
  errorElement.className = 'error-text';
  errorElement.textContent = message;
  
  const parent = inputElement.parentNode;
  parent.insertBefore(errorElement, inputElement.nextSibling);
}

/**
 * ===========================
 * API INTERACTIONS
 * ===========================
 */

// Login handling
async function handleLogin(event) {
  event.preventDefault();
  
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value.trim();
  
  if (!email || !password) {
    showPopupMessage('Please enter both email and password', 'error');
    return;
  }
  
  try {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({ email, password }),
      mode: 'cors',
      credentials: 'same-origin'
    });
    
    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.message || 'Login failed. Please check your credentials.');
    }
    
    const data = await response.json();
    
    if (data.access_token) {
      setAuthToken(data.access_token);
      
      const animationDuration = 3000;
      await showPopupMessage('Login successful! Redirecting...', 'success', animationDuration);
      
      window.location.href = 'index.html';
    } else {
      throw new Error('No token received from server');
    }
  } catch (error) {
    console.error('Login error:', error);
    showPopupMessage(error.message, 'error', 5000);
  }
}

// Logout handling
function handleLogout(event) {
  event.preventDefault();
  
  removeAuthToken();
  
  const animationDuration = 3000;
  showPopupMessage('Logged out successfully', 'success', animationDuration);
  
  updateAuthUI();
  
  const isIndexPage = window.location.pathname.includes('index.html') || 
                    window.location.pathname.endsWith('/') || 
                    window.location.pathname.endsWith('/hbnb/');
  
  if (!isIndexPage) {
    setTimeout(() => window.location.href = 'index.html', animationDuration + 500);
  } else {
    setTimeout(() => loadPlaces(), 500);
  }
}

// Places management
async function loadPlaces() {
  try {
    const headers = { 'Accept': 'application/json' };
    
    if (isAuthenticated()) {
      headers['Authorization'] = `Bearer ${getAuthToken()}`;
    }
    
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    
    // Plutôt qu'un loader, préparer le conteneur pour les cartes
    placesList.innerHTML = '';
    
    // Fetch places
    const response = await fetch(`${API_URL}/places`, {
      method: 'GET',
      headers,
      mode: 'cors',
      credentials: 'omit'
    });
    
    if (!response.ok) {
      throw new Error(`Failed to fetch places: ${response.status}`);
    }
    
    const places = await response.json();
    
    // Get detailed place info with prices
    const detailedPlaces = await Promise.all(
      places.map(async (place) => {
        try {
          const detailResponse = await fetch(`${API_URL}/places/${place.id}`, {
            method: 'GET',
            headers,
            mode: 'cors',
            credentials: 'omit'
          });
          
          if (!detailResponse.ok) return { ...place, price: 'Not specified' };
          
          const detailedPlace = await detailResponse.json();
          return { ...place, price: detailedPlace.price || 'Not specified' };
        } catch (error) {
          return { ...place, price: 'Not specified' };
        }
      })
    );
    
    // Sort by price (ascending)
    detailedPlaces.sort((a, b) => {
      const priceA = typeof a.price === 'number' ? a.price : parseFloat(a.price) || 0;
      const priceB = typeof b.price === 'number' ? b.price : parseFloat(b.price) || 0;
      return priceA - priceB;
    });
    
    // Render places with cascade effect
    const fragment = document.createDocumentFragment();
    
    if (detailedPlaces.length === 0) {
      const noResults = document.createElement('p');
      noResults.className = 'no-results';
      noResults.textContent = 'No places found matching your criteria.';
      fragment.appendChild(noResults);
    } else {
      detailedPlaces.forEach((place, index) => {
        const name = place.title || 'Unnamed Place';
        const id = place.id || 0;
        const price = place.price;
        
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        // Masquer initialement pour l'effet d'apparition
        placeCard.style.opacity = '0';
        placeCard.style.transform = 'translateY(20px)';
        
        placeCard.innerHTML = `
          <div class="place-info centered-content">
            <h3 class="place-name">${name}</h3>
            <p class="place-price">Price per night $${price}</p>
            <a href="place.html?id=${id}" class="view-details-btn details-button">View Details</a>
          </div>
        `;
        
        fragment.appendChild(placeCard);
      });
    }
    
    // Ajouter toutes les cartes au DOM en une seule fois
    placesList.appendChild(fragment);
    
    // Animer l'apparition des cartes en cascade
    revealCardsSequentially();
    
    applyFilters();
    
  } catch (error) {
    console.error('Error loading places:', error);
    
    // Show error state with better visual feedback
    const placesList = document.getElementById('places-list');
    if (placesList) {
      placesList.innerHTML = `
        <div class="centered-content" style="padding: 40px;">
          <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#FF5A5F" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12" y2="16"></line>
          </svg>
          <h3 style="margin-top: 20px; color: #484848">Unable to load places</h3>
          <p style="color: #767676">Please try again later</p>
          <button onclick="loadPlaces()" class="details-button" style="margin-top: 20px">Retry</button>
        </div>
      `;
    }
  }
}

// Animation séquentielle des cartes sans loader préalable
function revealCardsSequentially() {
  const cards = document.querySelectorAll('.place-card');
  
  if (cards.length === 0) return;
  
  // Animer séquentiellement chaque carte
  cards.forEach((card, index) => {
    setTimeout(() => {
      card.style.transition = 'opacity 0.5s ease, transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1)';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 100 + index * 100); // Délai progressif pour effet cascade
  });
}

// Remplaçons la fonction existante par notre nouvelle fonction
function animateCards() {
  revealCardsSequentially();
}

function renderPlaces(places, container) {
  const fragment = document.createDocumentFragment();
  
  if (places.length === 0) {
    const noResults = document.createElement('p');
    noResults.className = 'no-results';
    noResults.textContent = 'No places found matching your criteria.';
    fragment.appendChild(noResults);
  } else {
    places.forEach(place => {
      const name = place.title || 'Unnamed Place';
      const id = place.id || 0;
      const price = place.price;
      
      const placeCard = document.createElement('div');
      placeCard.className = 'place-card';
      placeCard.innerHTML = `
        <div class="place-info centered-content">
          <h3 class="place-name">${name}</h3>
          <p class="place-price">Price per night $${price}</p>
          <a href="place.html?id=${id}" class="view-details-btn details-button">View Details</a>
        </div>
      `;
      
      fragment.appendChild(placeCard);
    });
  }
  
  container.innerHTML = '';
  container.appendChild(fragment);
}

function setupFilters() {
  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    priceFilter.addEventListener('change', applyFilters);
  }
}

function applyFilters() {
  const priceFilter = document.getElementById('price-filter');
  const maxPrice = priceFilter?.value || '';
  
  const placeCards = document.querySelectorAll('.place-card');
  
  placeCards.forEach(card => {
    const priceElement = card.querySelector('.place-price');
    if (!priceElement) {
      card.style.display = '';
      return;
    }
    
    const priceText = priceElement.textContent;
    const priceMatch = priceText.match(/\$(\d+)/);
    const price = priceMatch ? parseFloat(priceMatch[1]) : 0;
    
    // Show all if no maxPrice filter is set
    if (!maxPrice) {
      card.style.display = '';
      return;
    }
    
    // Filter by max price
    card.style.display = (price <= parseFloat(maxPrice)) ? '' : 'none';
  });
  
  // Animer uniquement les cartes visibles après filtrage
  setTimeout(() => {
    const visibleCards = Array.from(placeCards).filter(card => 
      card.style.display !== 'none'
    );
    
    visibleCards.forEach((card, index) => {
      card.style.opacity = '0';
      card.style.transform = 'translateY(20px)';
      
      setTimeout(() => {
        card.style.transition = 'opacity 0.5s ease, transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1)';
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
      }, 50 + index * 80);
    });
  }, 50);
}

// Place details handling
async function loadPlaceDetails() {
  try {
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    
    if (!placeId) {
      showMessage('Place ID not provided');
      return;
    }
    
    // Show skeleton loading UI
    const placeContainer = document.getElementById('place-details');
    const reviewsContainer = document.getElementById('place-reviews');
    
    if (placeContainer) {
      placeContainer.innerHTML = `
        <div class="skeleton-card">
          <div class="skeleton-box skeleton-title"></div>
          <div class="skeleton-box skeleton-text" style="width: 60%;"></div>
          <div class="skeleton-box skeleton-text"></div>
          <div class="skeleton-box skeleton-text"></div>
          <div class="skeleton-box skeleton-text" style="width: 80%;"></div>
        </div>
      `;
    }
    
    if (reviewsContainer) {
      reviewsContainer.innerHTML = `
        <h2>Reviews</h2>
        <div class="skeleton-card">
          <div class="skeleton-box skeleton-text" style="width: 40%;"></div>
          <div class="skeleton-box skeleton-text" style="width: 30%;"></div>
          <div class="skeleton-box skeleton-text"></div>
          <div class="skeleton-box skeleton-text" style="width: 90%;"></div>
        </div>
      `;
    }
    
    const headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };
    
    if (isAuthenticated()) {
      headers['Authorization'] = `Bearer ${getAuthToken()}`;
    }
    
    // Load place details
    const placeResponse = await fetch(`${API_URL}/places/${placeId}`, {
      method: 'GET',
      headers,
      mode: 'cors',
      credentials: 'omit'
    });
    
    if (!placeResponse.ok) {
      throw new Error('Failed to fetch place details');
    }
    
    const place = await placeResponse.json();
    let host = place.owner || null;
    
    // Update UI with real data with fade effect
    if (placeContainer) {
      placeContainer.classList.add('fade-out');
      
      setTimeout(() => {
        displayPlaceDetails(place, host);
        placeContainer.classList.remove('fade-out');
        placeContainer.classList.add('fade-in');
      }, 300);
    }
    
    // Load place reviews
    const reviewsResponse = await fetch(`${API_URL}/places/${placeId}/reviews`, {
      method: 'GET',
      headers,
      mode: 'cors',
      credentials: 'omit'
    });
    
    if (!reviewsResponse.ok) {
      throw new Error('Failed to fetch reviews');
    }
    
    const reviews = await reviewsResponse.json();
    displayPlaceReviews(reviews);
    
  } catch (error) {
    console.error('Error loading place details:', error);
    showMessage('Failed to load place details. Please try again later.');
  }
}

function displayPlaceDetails(place, host) {
  document.title = `${place.title || 'Place Details'} - HBNB`;
  
  const placeContainer = document.getElementById('place-details');
  if (!placeContainer) return;
  
  const amenities = place.amenities || [];
  
  // Format host info
  let hostInfo = '';
  if (host) {
    const firstName = host.first_name || '';
    const lastName = host.last_name || '';
    const hostName = firstName && lastName 
      ? `${firstName} ${lastName}` 
      : firstName || lastName || host.name || host.username || 'Host';
      
    hostInfo = `<p><strong>Host:</strong> ${hostName}</p>`;
  }
  
  // Render place details
  placeContainer.innerHTML = `
    <h1 class="place-title">${place.title || 'Unnamed Place'}</h1>
    <div class="place-card">
      <div class="place-info">
        <div class="host-price">
          ${hostInfo}
          <p><strong>Price per night:</strong> $${place.price || 'Not specified'}</p>
        </div>
        
        <div class="description">
          <p><strong>Description:</strong> ${place.description || 'No description available for this place.'}</p>
        </div>
        
        <div class="amenities">
          <p><strong>Amenities:</strong> ${amenities.length > 0 
            ? amenities.map(amenity => amenity.name || amenity).join(', ')
            : 'No amenities information available.'}
          </p>
        </div>
      </div>
    </div>
  `;
}

// Review functionality
async function loadPlaceSummary(placeId) {
  try {
    const response = await fetch(`${API_URL}/places/${placeId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      mode: 'cors',
      credentials: 'omit'
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch place details');
    }
    
    const place = await response.json();
    
    // Update page title and header
    const placeNameElement = document.getElementById('place-name');
    if (placeNameElement) {
      placeNameElement.textContent = place.title || place.name || 'Place Details';
    }
    
    document.title = `Add Review: ${place.title || place.name || 'Place'} - HBNB`;
    
    // Set up review form submission
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
      reviewForm.addEventListener('submit', (event) => {
        submitReview(event, placeId);
      });
    }
  } catch (error) {
    console.error('Error loading place summary:', error);
    showMessage('Failed to load place information. Please try again later.');
  }
}

async function submitReview(event, placeId) {
  event.preventDefault();
  
  const reviewForm = document.getElementById('review-form');
  const reviewText = document.getElementById('review').value.trim();
  const rating = document.getElementById('rating').value;
  
  // Clear previous error messages
  document.querySelectorAll('.error-text').forEach(el => el.remove());
  
  // Validate inputs
  let hasError = false;
  
  if (!reviewText) {
    showInputError('review', 'Please enter your review');
    hasError = true;
  }
  
  if (!rating) {
    showInputError('rating', 'Please select a rating');
    hasError = true;
  }
  
  if (hasError) return;
  
  try {
    // Update form UI to show submission in progress
    if (reviewForm) {
      reviewForm.classList.add('form-submitted');
    }
    
    // Update button state with proper styling
    const submitButton = document.querySelector('#review-form button[type="submit"]');
    const originalButtonContent = submitButton ? submitButton.innerHTML : '';
    
    if (submitButton) {
      submitButton.disabled = true;
      submitButton.innerHTML = `
        <span class="button-with-loader">
          <span class="button-spinner"></span>
          <span>Submitting...</span>
        </span>
      `;
    }
    
    const authToken = getAuthToken();
    
    // Extract user ID from token
    let userId = null;
    try {
      const tokenParts = authToken.split('.');
      if (tokenParts.length === 3) {
        const payload = JSON.parse(atob(tokenParts[1]));
        userId = payload.sub;
      }
    } catch (e) {
      console.error('Could not extract user ID from token:', e);
    }
    
    // Submit review
    const response = await fetch(`${API_URL}/reviews`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
        'Accept': 'application/json'
      },
      body: JSON.stringify({ 
        text: reviewText,
        rating: parseInt(rating),
        place_id: placeId,
        user_id: userId
      }),
      mode: 'cors',
      credentials: 'omit'
    });
    
    // Reset form UI
    if (reviewForm) {
      reviewForm.classList.remove('form-submitted');
    }
    
    if (submitButton) {
      submitButton.disabled = false;
      submitButton.innerHTML = originalButtonContent || 'Submit Review';
    }
    
    if (!response.ok) {
      const errorData = await response.json();
      
      let errorMessage = errorData.message || errorData.error || 'Failed to submit review';
      
      // Handle specific error cases
      if (errorData.error) {
        if (errorData.error.includes("You cannot review your own place")) {
          errorMessage = "You cannot review your own place.";
        } else if (errorData.error.includes("You have already reviewed this place")) {
          errorMessage = "You have already submitted a review for this place.";
        }
        
        // Clear form for these specific cases
        document.getElementById('review').value = '';
        document.getElementById('rating').value = '';
      }
      
      showPopupMessage(errorMessage, 'error');
      throw new Error(errorMessage);
    }
    
    const newReview = await response.json();
    
    showPopupMessage('Review submitted successfully!', 'success');
    
    // Clear form
    document.getElementById('review').value = '';
    document.getElementById('rating').value = '';
    
    // Update UI
    addNewReviewToUI(newReview);
    
  } catch (error) {
    console.error('Error submitting review:', error);
    showMessage(error.message || 'Failed to submit review. Please try again.');
    
    // Reset form UI even on error
    if (reviewForm) {
      reviewForm.classList.remove('form-submitted');
    }
    
    // Reset button to original state
    const submitButton = document.querySelector('#review-form button[type="submit"]');
    if (submitButton) {
      submitButton.disabled = false;
      submitButton.innerHTML = 'Submit Review';
    }
  }
}

function displayPlaceReviews(reviews) {
  const reviewsContainer = document.getElementById('place-reviews');
  if (!reviewsContainer) return;
  
  reviewsContainer.innerHTML = '<h2>Reviews</h2>';
  
  if (!reviews || reviews.length === 0) {
    reviewsContainer.innerHTML += '<p class="no-reviews">No reviews yet. Be the first to leave a review!</p>';
    return;
  }
  
  const reviewsList = document.createElement('div');
  reviewsList.className = 'reviews-container';
  
  const reviewsArray = Array.isArray(reviews) ? reviews : reviews.reviews || [];
  
  reviewsArray.forEach(review => {
    renderSingleReview(review, reviewsList);
  });
  
  reviewsContainer.appendChild(reviewsList);
}

function renderSingleReview(review, container) {
  const reviewDate = review.created_at ? new Date(review.created_at).toLocaleDateString() : 'Unknown date';
  
  const filledStars = '★'.repeat(review.rating || 0);
  const emptyStars = '☆'.repeat(5 - (review.rating || 0));
  const stars = `<span style="color: gold;">${filledStars}${emptyStars}</span>`;
  
  // Get reviewer name
  let displayName = 'Anonymous';
  
  if (review.user) {
    if (review.user.first_name || review.user.last_name) {
      displayName = `${review.user.first_name || ''} ${review.user.last_name || ''}`.trim();
    } else if (review.user.name) {
      displayName = review.user.name;
    } else if (review.user.username) {
      displayName = review.user.username;
    } else if (review.user.email) {
      displayName = review.user.email.split('@')[0];
    }
  } else if (review.user_id) {
    const reviewElement = document.createElement('div');
    reviewElement.className = 'review-card';
    
    fetchUserInfo(review.user_id)
      .then(userData => {
        if (userData && (userData.first_name || userData.last_name)) {
          const nameEl = reviewElement.querySelector('.reviewer-name');
          if (nameEl) {
            nameEl.textContent = `${userData.first_name || ''} ${userData.last_name || ''}`.trim() + ':';
          }
        }
      })
      .catch(() => {});
    
    displayName = 'Loading user info...';
    
    reviewElement.innerHTML = `
      <p class="reviewer-name">${displayName}:</p>
      <p class="review-rating">${stars}</p>
      <p class="review-text">${review.text || 'No review text'}</p>
      <p class="date">${reviewDate}</p>
    `;
    
    container.appendChild(reviewElement);
    return;
  }
  
  const reviewElement = document.createElement('div');
  reviewElement.className = 'review-card';
  reviewElement.innerHTML = `
    <p class="reviewer-name">${displayName}:</p>
    <p class="review-rating">${stars}</p>
    <p class="review-text">${review.text || 'No review text'}</p>
    <p class="date">${reviewDate}</p>
  `;
  
  container.appendChild(reviewElement);
}

function addNewReviewToUI(newReview) {
  const reviewsContainer = document.getElementById('place-reviews');
  if (!reviewsContainer) return;
  
  // Remove "no reviews" message if it exists
  const noReviewsMsg = reviewsContainer.querySelector('.no-reviews');
  if (noReviewsMsg) {
    noReviewsMsg.remove();
  }
  
  // Create reviews container if it doesn't exist
  let reviewsList = reviewsContainer.querySelector('.reviews-container');
  if (!reviewsList) {
    if (!reviewsContainer.querySelector('h2')) {
      reviewsContainer.innerHTML = '<h2>Reviews</h2>';
    }
    
    reviewsList = document.createElement('div');
    reviewsList.className = 'reviews-container';
    reviewsContainer.appendChild(reviewsList);
  }
  
  // Format review date
  const reviewDate = newReview.created_at ? new Date(newReview.created_at).toLocaleDateString() : 'Just now';
  
  // Generate star rating
  const filledStars = '★'.repeat(newReview.rating || 0);
  const emptyStars = '☆'.repeat(5 - (newReview.rating || 0));
  const stars = `<span style="color: gold;">${filledStars}${emptyStars}</span>`;
  
  // Get user info from token
  let userInfo = {};
  try {
    const token = getAuthToken();
    if (token) {
      const tokenParts = token.split('.');
      if (tokenParts.length === 3) {
        const payload = JSON.parse(atob(tokenParts[1]));
        userInfo = {
          first_name: payload.first_name || '',
          last_name: payload.last_name || '',
          email: payload.email || ''
        };
      }
    }
  } catch (e) {
    console.error('Error getting user info from token:', e);
  }
  
  // Create display name
  const displayName = userInfo.first_name || userInfo.last_name 
    ? `${userInfo.first_name || ''} ${userInfo.last_name || ''}`.trim()
    : 'You';
  
  // Create and insert review element with enhanced animation
  const reviewElement = document.createElement('div');
  reviewElement.className = 'review-card';
  reviewElement.style.opacity = '0';
  reviewElement.style.transform = 'translateY(20px)';
  reviewElement.innerHTML = `
    <p class="reviewer-name">${displayName}:</p>
    <p class="review-rating">${stars}</p>
    <p class="review-text">${newReview.text || ''}</p>
    <p class="date">${reviewDate}</p>
  `;
  
  // Add review to top of list with smooth transition
  reviewsList.insertBefore(reviewElement, reviewsList.firstChild);
  
  // Force a reflow before starting the animation
  reviewElement.offsetHeight;
  
  // Start animation
  reviewElement.style.transition = 'all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1)';
  reviewElement.style.opacity = '1';
  reviewElement.style.transform = 'translateY(0)';
  reviewElement.style.animation = 'highlightNewReview 2s ease 0.5s';
  
  // Scroll to the new review
  setTimeout(() => {
    reviewElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }, 500);
}

/**
 * ===========================
 * UTILITY FUNCTIONS
 * ===========================
 */

async function fetchUserInfo(userId) {
  try {
    const response = await fetch(`${API_URL}/users/${userId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`,
        'Content-Type': 'application/json'
      },
      mode: 'cors',
      credentials: 'omit'
    });
    
    if (!response.ok) {
      throw new Error(`Failed to fetch user details: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`Error fetching user info for ID ${userId}:`, error);
    return null;
  }
}

function initializeAddReviewPage() {
  if (!isAuthenticated()) {
    window.location.href = 'index.html';
    return;
  }
  
  const urlParams = new URLSearchParams(window.location.search);
  const placeId = urlParams.get('id');
  
  if (!placeId) {
    showMessage('Place ID not provided');
    return;
  }
  
  loadPlaceSummary(placeId);
}

/**
 * ===========================
 * INITIALIZATION
 * ===========================
 */

document.addEventListener('DOMContentLoaded', () => {
  updateAuthUI();
  
  // Set up login/logout handlers
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
  }
  
  const logoutLink = document.getElementById('logout-link');
  if (logoutLink) {
    logoutLink.addEventListener('click', handleLogout);
  }
  
  // Redirect if already logged in
  if (window.location.pathname.includes('login.html') && isAuthenticated()) {
    window.location.href = 'index.html';
    return;
  }
  
  // Page-specific initialization
  const isIndexPage = window.location.pathname.includes('index.html') || 
                      window.location.pathname.endsWith('/') || 
                      window.location.pathname.endsWith('/hbnb/');
  
  if (isIndexPage) {
    loadPlaces();
    setupFilters();
  } else if (window.location.pathname.includes('place.html')) {
    loadPlaceDetails();
    
    // Show review form only for authenticated users
    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection) {
      if (isAuthenticated()) {
        addReviewSection.style.display = 'block';
        
        const reviewForm = document.getElementById('review-form');
        if (reviewForm) {
          reviewForm.addEventListener('submit', function(event) {
            const urlParams = new URLSearchParams(window.location.search);
            const placeId = urlParams.get('id');
            submitReview(event, placeId);
          });
        }
      } else {
        addReviewSection.style.display = 'none';
      }
    }
  } else if (window.location.pathname.includes('add_review.html')) {
    if (isAuthenticated()) {
      initializeAddReviewPage();
    } else {
      window.location.href = 'login.html';
    }
  }
});
