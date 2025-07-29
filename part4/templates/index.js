/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

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

    // --- Check authentication status ---
    function checkAuthentication() {
        const token = getCookie('HBnBToken');
        if (!token) {
            loginLink.style.display = 'block';
            placesList.innerHTML = '<p>Please login to view places.</p>';
            return null;
        } else {
            loginLink.style.display = 'none';
            return token;
        }
    }

    // --- Fetch data from API ---
    async function fetchPlaces(token) {
        try {
            const res = await fetch(API_URL, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

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
            const card = document.createElement('div');
            card.classList.add('place-card');
            card.setAttribute('data-price', place.price);

            card.innerHTML = `
                <h2>${place.title}</h2>
                <p>${place.description}</p>
                <p><strong>$${place.price}</strong> / night</p>
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
    if (token) {
        setupPriceFilter();
        fetchPlaces(token);
    }
});
