def _mk_user(client, username, email, role="user"):
    return client.post("/api/register", json={"username": username, "email": email, "password": "Passw0rd!", "role": role})

def _token(client, email):
    return client.post("/api/login", json={"email": email, "password": "Passw0rd!"}).get_json()["token"]

def test_register_success(client):
    assert _mk_user(client, "anna", "anna@mail.ru").status_code == 201

def test_register_invalid_email_rejected(client):
    assert _mk_user(client, "bob", "not-an-email").status_code == 400

def test_register_duplicate_email_rejected(client):
    _mk_user(client, "a", "dup@mail.ru")
    assert _mk_user(client, "b", "dup@mail.ru").status_code == 400

def test_register_short_password_rejected(client):
    assert client.post("/api/register", json={"username": "s", "email": "s@mail.ru", "password": "123"}).status_code == 400

def test_login_returns_token(client):
    _mk_user(client, "org", "org@mail.ru", role="organizer")
    resp = client.post("/api/login", json={"email": "org@mail.ru", "password": "Passw0rd!"})
    assert resp.status_code == 200 and "token" in resp.get_json()

def test_login_wrong_password(client):
    _mk_user(client, "x", "x@mail.ru")
    assert client.post("/api/login", json={"email": "x@mail.ru", "password": "WrongPass1!"}).status_code == 401

def test_create_event_requires_organizer_token(client):
    assert client.post("/api/events", json={"title": "Лекция"}).status_code == 401

def test_create_event_with_organizer_token(client):
    _mk_user(client, "org", "org@mail.ru", role="organizer")
    token = _token(client, "org@mail.ru")
    resp = client.post("/api/events", json={"title": "Лекция о доступной среде", "event_date": "2026-12-01 12:00", "is_inclusive": True}, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201

def test_create_event_forbidden_for_user_role(client):
    _mk_user(client, "u", "u@mail.ru")
    token = _token(client, "u@mail.ru")
    assert client.post("/api/events", json={"title": "Лекция", "event_date": "2026-12-01 12:00"}, headers={"Authorization": f"Bearer {token}"}).status_code == 403

def test_events_list_public(client):
    assert client.get("/api/events").status_code == 200

def test_events_filter_inclusive(client):
    _mk_user(client, "org", "org@mail.ru", role="organizer")
    token = _token(client, "org@mail.ru")
    client.post("/api/events", json={"title": "Обычное", "event_date": "2026-12-01 12:00"}, headers={"Authorization": f"Bearer {token}"})
    client.post("/api/events", json={"title": "Инклюзивное", "event_date": "2026-12-02 12:00", "is_inclusive": True}, headers={"Authorization": f"Bearer {token}"})
    titles = [e["title"] for e in client.get("/api/events?inclusive=1").get_json()]
    assert titles == ["Инклюзивное"]

def test_register_on_event_flow(client):
    _mk_user(client, "org", "org@mail.ru", role="organizer")
    ev = client.post("/api/events", json={"title": "Кинопросмотр", "event_date": "2026-12-01 12:00"}, headers={"Authorization": f"Bearer {_token(client, 'org@mail.ru')}"}).get_json()
    _mk_user(client, "anna", "anna@mail.ru")
    resp = client.post(f"/api/events/{ev['event_id']}/register", headers={"Authorization": f"Bearer {_token(client, 'anna@mail.ru')}"})
    assert resp.status_code == 201 and resp.get_json()["status"] == "pending"

def test_duplicate_registration_rejected(client):
    _mk_user(client, "org", "org@mail.ru", role="organizer")
    ev = client.post("/api/events", json={"title": "Прогулка", "event_date": "2026-12-01 12:00"}, headers={"Authorization": f"Bearer {_token(client, 'org@mail.ru')}"}).get_json()
    _mk_user(client, "p", "p@mail.ru")
    pt = _token(client, "p@mail.ru")
    client.post(f"/api/events/{ev['event_id']}/register", headers={"Authorization": f"Bearer {pt}"})
    assert client.post(f"/api/events/{ev['event_id']}/register", headers={"Authorization": f"Bearer {pt}"}).status_code == 400

def test_my_registrations_lists(client):
    _mk_user(client, "org", "org@mail.ru", role="organizer")
    ev = client.post("/api/events", json={"title": "Мастер-класс", "event_date": "2026-12-01 12:00"}, headers={"Authorization": f"Bearer {_token(client, 'org@mail.ru')}"}).get_json()
    _mk_user(client, "p", "p@mail.ru")
    pt = _token(client, "p@mail.ru")
    client.post(f"/api/events/{ev['event_id']}/register", headers={"Authorization": f"Bearer {pt}"})
    assert len(client.get("/api/my/registrations", headers={"Authorization": f"Bearer {pt}"}).get_json()) == 1

def test_chat_post_and_get(client):
    _mk_user(client, "org", "org@mail.ru", role="organizer")
    ot = _token(client, "org@mail.ru")
    ev = client.post("/api/events", json={"title": "Чат-тест", "event_date": "2026-12-01 12:00"}, headers={"Authorization": f"Bearer {ot}"}).get_json()
    client.post(f"/api/events/{ev['event_id']}/messages", json={"message": "Здравствуйте!"}, headers={"Authorization": f"Bearer {ot}"})
    assert any(m["message"] == "Здравствуйте!" for m in client.get(f"/api/events/{ev['event_id']}/messages").get_json())

def test_confirm_registration_notifies_participant(client):
    _mk_user(client, "org", "org@mail.ru", role="organizer")
    ot = _token(client, "org@mail.ru")
    ev = client.post("/api/events", json={"title": "Экскурсия", "event_date": "2026-12-01 12:00"}, headers={"Authorization": f"Bearer {ot}"}).get_json()
    _mk_user(client, "anna", "anna@mail.ru")
    at = _token(client, "anna@mail.ru")
    reg = client.post(f"/api/events/{ev['event_id']}/register", headers={"Authorization": f"Bearer {at}"}).get_json()
    client.patch(f"/api/registrations/{reg['registration_id']}", json={"status": "confirmed"}, headers={"Authorization": f"Bearer {ot}"})
    notifs = client.get("/api/notifications", headers={"Authorization": f"Bearer {at}"}).get_json()
    assert any("подтверждена" in n["message"] for n in notifs)
