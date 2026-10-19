async function refresh() {
    try {
        const notifs = await api('/api/notifications');
        document.getElementById('notifications').innerHTML = notifs.map(n => '<div class="event-card ' + (n.is_read ? '' : 'unread') + '">[' + n.type + '] ' + n.message + '</div>').join('');
        const regs = await api('/api/my/registrations');
        document.getElementById('my-registrations').innerHTML = regs.map(r => '<div class="event-card">Мероприятие #' + r.event_id + ' — <span class="status-' + r.status + '">' + ({ pending: 'На рассмотрении', confirmed: 'Подтверждена', cancelled: 'Отменена' }[r.status] || r.status) + '</span></div>').join('');
    } catch (err) {
        localStorage.removeItem('token');
        window.location.href = '/login';
    }
}
document.getElementById('event-form').addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const form = ev.target;
    try {
        const data = await api('/api/events', {
            method: 'POST',
            body: JSON.stringify({ title: form.title.value, event_date: form.event_date.value, location: form.location.value, description: form.description.value, is_inclusive: form.is_inclusive.checked }),
        });
        document.getElementById('event-msg').textContent = 'Мероприятие создано, id=' + data.event_id;
        form.reset();
    } catch (err) {
        document.getElementById('event-msg').textContent = err.message;
    }
});
document.getElementById('mark-read').addEventListener('click', async () => {
    await api('/api/notifications/read', { method: 'POST' });
    refresh();
});
refresh();
