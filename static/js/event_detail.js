const eventId = window.location.pathname.split('/').pop();

async function loadChat() {
    const msgs = await api('/api/events/' + eventId + '/messages');
    document.getElementById('chat').innerHTML = msgs.map(m => '<div class="chat-msg"><span class="chat-user">Пользователь #' + m.user_id + '</span>: ' + m.message + '</div>').join('');
}
document.getElementById('chat-form').addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const input = document.getElementById('chat-input');
    try {
        await api('/api/events/' + eventId + '/messages', { method: 'POST', body: JSON.stringify({ message: input.value }) });
        input.value = '';
        loadChat();
    } catch (err) {
        document.getElementById('reg-result').textContent = err.message;
    }
});
document.getElementById('register-btn').addEventListener('click', async () => {
    try {
        const data = await api('/api/events/' + eventId + '/register', { method: 'POST' });
        const banner = document.getElementById('status-banner');
        banner.className = 'status-banner status-' + data.status;
        banner.textContent = data.status === 'pending' ? 'Заявка на рассмотрении' : data.status;
    } catch (err) {
        document.getElementById('reg-result').textContent = err.message;
    }
});
document.getElementById('review-form').addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const form = ev.target;
    try {
        await api('/api/events/' + eventId + '/reviews', {
            method: 'POST',
            body: JSON.stringify({ rating: form.rating.value, comment: form.comment ? form.comment.value : '' }),
        });
        loadReviews();
    } catch (err) {
        document.getElementById('reg-result').textContent = err.message;
    }
});
async function loadReviews() {
    const reviews = await api('/api/events/' + eventId + '/reviews');
    document.getElementById('reviews').innerHTML = reviews.map(r => '<div class="event-card">Оценка ' + r.rating + '/5 — ' + (r.comment || '') + '</div>').join('');
}
loadChat(); setInterval(loadChat, 5000); loadReviews();
