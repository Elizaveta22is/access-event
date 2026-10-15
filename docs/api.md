# Описание API AccessEvent

| Метод | URL | Доступ | Вход (JSON) | Ответы |
| POST | /api/register | все | username, email, password, role | 201 user_id; 400 ошибки |
| POST | /api/login | все | email, password | 200 token; 401 неверные данные |
| GET | /api/events | все | — | 200 список с полем accessibility |
| POST | /api/events | organizer, admin | title, event_date, is_inclusive | 201 id; 401 без токена |
| POST | /api/registrations | user | event_id, accessibility_request | 201; 409 повторная |
| GET | /api/registrations | user | — | 200 список регистраций |

## Примеры

### POST /api/register
Запрос: {"username": "anna", "email": "anna@mail.ru", "password": "Passw0rd!", "role": "user"}
Ответ 201: {"user_id": 1, "message": "Пользователь создан"}

### POST /api/login
Запрос: {"email": "anna@mail.ru", "password": "Passw0rd!"}
Ответ 200: {"token": "eyJ...", "role": "user", "user_id": 1}

### POST /api/events
Запрос: {"title": "Тихий кинопросмотр", "event_date": "2026-11-03 19:00:00", "is_inclusive": true}
Ответ 201: {"id": 1, "message": "Мероприятие создано"}
