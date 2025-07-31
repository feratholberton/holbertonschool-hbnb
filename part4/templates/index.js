document.addEventListener('DOMContentLoaded', () => {
    const API_URL = 'http://127.0.0.1:5000/api/v1/places/';
    const loginLink = document.getElementById('login-link');
    const placesList = document.getElementById('places-list');
    const priceFilter = document.getElementById('price-filter');

    let allPlaces = [];

    // --- Helper to get JWT token from cookies ---
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    // --- Check authentication status and show/hide login ---
    function checkAuthentication() {
        const token = getCookie('HBnBToken');
        loginLink.style.display = token ? 'none' : 'block';
        return token;
    }

    // --- Fetch data from API ---
    async function fetchPlaces(token) {
        try {
            const headers = token ? { Authorization: `Bearer ${token}` } : {};
            const res = await fetch(API_URL, { headers });

            if (!res.ok) throw new Error('Failed to fetch places');
            allPlaces = await res.json();
            displayPlaces(allPlaces);
        } catch (err) {
            placesList.innerHTML = `<p>Error: ${err.message}</p>`;
        }
    }

    // --- Render cards ---
    function displayPlaces(places) {
        placesList.innerHTML = '';
        if (places.length === 0) {
            placesList.innerHTML = '<p>No places available.</p>';
            return;
        }

        places.forEach(place => {
            const card = document.createElement('article');
            card.classList.add('place-card', 'card', 'card--place');
            card.setAttribute('data-price', place.price);

            card.innerHTML = `
                <h2>${place.title}</h2>
                <p>Price per night <strong>$${place.price}</strong></p>
                <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            `;
            placesList.appendChild(card);
        });
    }

    // --- Setup price filter ---
    function setupPriceFilter() {
        const prices = [10, 50, 100, 'all'];
        priceFilter.innerHTML = '';
        prices.forEach(price => {
            const option = document.createElement('option');
            option.value = price;
            option.textContent = price === 'all' ? 'All' : `$${price}`;
            priceFilter.appendChild(option);
        });
        priceFilter.value = 'all';
    }

    // --- Handle price filter changes ---
    priceFilter.addEventListener('change', () => {
        const selected = priceFilter.value;
        const cards = document.querySelectorAll('.place-card');

        cards.forEach(card => {
            const cardPrice = parseFloat(card.getAttribute('data-price'));
            if (selected === 'all' || cardPrice <= parseFloat(selected)) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    });

    // === Run App ===
    const token = checkAuthentication();
    setupPriceFilter();
    fetchPlaces(token);
});
