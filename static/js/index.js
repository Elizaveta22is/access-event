async function loadEvents() {
    try {
        const only = document.getElementById('only-inclusive').checked;
        const events = await api('/api/events' + (only ? '?inclusive=1' : ''));
        const box = document.getElementById('events-list');
        box.innerHTML = '';
        events.forEach(e => {
            const card = document.createElement('div');
            card.className = 'event-card';
            const link = document.createElement('a');
            link.href = '/events/' + e.id;
            link.textContent = e.title;
            const meta = document.createElement('p');
            meta.textContent = (e.event_date || '') + ' ' + (e.location || '') + (e.is_inclusive ? ' [ИНКЛИЗИВНОЕ]' : '');
            card.append(link, meta);
            box.append(card);
        });
    } catch (err) {
        document.getElementById('error').textContent = err.message;
    }
}
document.getElementById('only-inclusive').addEventListener('change', loadEvents);
loadEvents();
