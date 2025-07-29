document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            const errorMsg = document.getElementById('login-error');

            try {
                const res = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (!res.ok) {
                    const error = await res.json();
                    throw new Error(error.error || 'Login failed');
                }

                const data = await res.json();
                document.cookie = `HBnBToken=${data.access_token}; path=/`;
                window.location.href = 'index.html';
            } catch (err) {
                errorMsg.textContent = err.message;
            }
        });
    }
});
