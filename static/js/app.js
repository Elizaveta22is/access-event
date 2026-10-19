const API = '';
function getToken() { return localStorage.getItem('token') || ''; }
function authHeaders() { const t = getToken(); return t ? { 'Authorization': 'Bearer ' + t } : {}; }
async function api(path, options = {}) {
    const resp = await fetch(API + path, {
        ...options,
        headers: { 'Content-Type': 'application/json', ...authHeaders(), ...(options.headers || {}) },
    });
    const data = await resp.json().catch(() => ({}));
    if (!resp.ok) throw new Error(data.error || ('Ошибка ' + resp.status));
    return data;
}
