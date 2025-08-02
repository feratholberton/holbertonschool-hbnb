document.addEventListener('DOMContentLoaded', () => {
    const placeDetailsSection = document.getElementById('place-details');
    const addReviewSection = document.getElementById('add-review');
    const reviewForm = document.getElementById('review-form');
    const ratingSelect = document.getElementById('rating');
    const API_BASE = 'http://127.0.0.1:5000/api/v1';

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    function getPlaceIdFromURL() {
        const params = new URLSearchParams(window.location.search);
        return params.get('id');
    }

    function populateRatingOptions() {
        for (let i = 1; i <= 5; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = `${i} Star${i > 1 ? 's' : ''}`;
            ratingSelect.appendChild(option);
        }
    }

    async function fetchPlaceDetails(placeId, token) {
        try {
            const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
            const res = await fetch(`${API_BASE}/places/${placeId}`, { headers });
            if (!res.ok) throw new Error('Could not load place details.');
            const place = await res.json();
            displayPlaceDetails(place);
        } catch (err) {
            placeDetailsSection.innerHTML = `<p>${err.message}</p>`;
        }
    }

    function displayPlaceDetails(place) {
        placeDetailsSection.innerHTML = `
            <article class="place-details">
                <h1>${place.title}</h1>
                <div class="card   card--place">
                    <p><strong>Host:</strong> ${place.owner.first_name} ${place.owner.last_name}</p>
                    <p><strong>Price per night:</strong> $${place.price}</p>
                    <p><strong>Description:</strong> ${place.description}</p>
                    <div class="place-details-amenities">
                        <h2>Amenities: </h2>
                        <ul>${place.amenities.map(a => `<li>${a.name}</li>`).join('')}</ul>
                    </div>
                </div>
                <h3>Reviews</h3>
                ${place.reviews.length > 0 ? place.reviews.map(r => `
                    <div class="card review-card">
                        <p><strong>${r.user.first_name} ${r.user.last_name}:</strong></p>
                        <p>${r.text}</p>
                        <p>Rating: ${r.rating}</p>
                    </div>
                `).join('') : '<p>No reviews yet.</p>'}
            </article>
        `;
    }

    async function submitReview(event, placeId, token) {
        event.preventDefault();

        const reviewText = document.getElementById('review').value.trim();
        const rating = parseInt(document.getElementById('rating').value);

        if (!reviewText || !rating) {
            alert("Please enter review text and select a rating.");
            return;
        }

        try {
            const res = await fetch(`${API_BASE}/reviews/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    text: reviewText,
                    rating: rating,
                    place_id: placeId
                })
            });

            if (res.status === 201) {
                alert('Review submitted successfully!');
                reviewForm.reset();
                fetchPlaceDetails(placeId, token);
            } else {
                const error = await res.json();
                alert(`Error: ${error.error}`);
            }
        } catch (err) {
            alert('Error submitting review: ' + err.message);
        }
    }

    // === Main ===
    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        placeDetailsSection.innerHTML = '<p>Invalid place ID.</p>';
        return;
    }

    const token = getCookie('HBnBToken');
    if (token) {
        addReviewSection.style.display = 'block';

        reviewForm.addEventListener('submit', (event) => {
            submitReview(event, placeId, token);
        });
    } else {
        addReviewSection.style.display = 'none';
    }

    populateRatingOptions();
    fetchPlaceDetails(placeId, token);
});
