document.getElementById('login-form').addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const form = ev.target;
    try {
        const data = await api('/api/login', {
            method: 'POST',
            body: JSON.stringify({ email: form.email.value, password: form.password.value }),
        });
        localStorage.setItem('token', data.token);
        window.location.href = '/dashboard';
    } catch (err) {
        document.getElementById('login-msg').textContent = err.message;
    }
});
