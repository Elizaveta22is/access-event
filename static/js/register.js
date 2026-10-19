document.getElementById('reg-form').addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const form = ev.target;
    try {
        await api('/api/register', {
            method: 'POST',
            body: JSON.stringify({ username: form.username.value, email: form.email.value, password: form.password.value, role: form.role.value }),
        });
        document.getElementById('reg-msg').textContent = 'Регистрация успешна. Теперь войдите.';
    } catch (err) {
        document.getElementById('reg-msg').textContent = err.message;
    }
});
