/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    const API_URL = 'http://127.0.0.1:5000/api/v1/places/';
    const placesList = document.getElementById('places-list');
    const priceFilter = document.getElementById('price-filter');

    let allPlaces = [];

    // Fetch places from the API
    async function fetchPlaces() {
        try {
            const res = await fetch(API_URL);
            if (!res.ok) throw new Error('Failed to fetch places');
            allPlaces = await res.json();
            populatePriceFilter(allPlaces);
            displayPlaces(allPlaces);
        } catch (err) {
            console.error(err);
            placesList.innerHTML = '<p>Error loading places.</p>';
        }
    }

    // Display places in the DOM
    function displayPlaces(places) {
        placesList.innerHTML = ''; // Clear previous
        if (places.length === 0) {
            placesList.innerHTML = '<p>No places found.</p>';
            return;
        }

        places.forEach(place => {
            const card = document.createElement('div');
            card.classList.add('place-card');
            card.innerHTML = `
                <h2>${place.title}</h2>
                <p>${place.description}</p>
                <p><strong>$${place.price}</strong> / night</p>
                <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            `;
            placesList.appendChild(card);
        });
    }

    // Populate the filter dropdown based on unique price thresholds
    function populatePriceFilter(places) {
        const priceOptions = [10, 50, 100]; // fixed thresholds
        const select = priceFilter;

        // Add fixed options
        select.innerHTML = '';
        priceOptions.forEach(price => {
            const option = document.createElement('option');
            option.value = price;
            option.textContent = `$${price}`;
            select.appendChild(option);
        });

        // Add 'All' option
        const allOption = document.createElement('option');
        allOption.value = 'all';
        allOption.textContent = 'All';
        select.appendChild(allOption);

        // Set default
        select.value = 'all';
    }

    // Filter places by max price
    priceFilter.addEventListener('change', (event) => {
        const selected = event.target.value;

        if (selected === 'all') {
            displayPlaces(allPlaces);
        } else {
            const maxPrice = parseFloat(selected);
            const filtered = allPlaces.filter(p => p.price <= maxPrice);
            displayPlaces(filtered);
        }
    });

    // Load places on startup
    fetchPlaces();
  });