# ER-диаграмма AccessEvent

```mermaid
erDiagram
    USERS ||--o{ EVENTS : "организует"
    USERS ||--o{ REGISTRATIONS : "записывается"
    EVENTS ||--o{ REGISTRATIONS : "содержит"

    USERS {
        int id PK
        string username
        string email
        string password_hash
        string role
        boolean is_deaf
        text accessibility_needs
        datetime created_at
    }

    EVENTS {
        int id PK
        string title
        text description
        datetime event_date
        string location
        int organizer_id FK
        boolean is_inclusive
        boolean sign_language
        boolean visual_alerts
        datetime created_at
    }

    REGISTRATIONS {
        int id PK
        int user_id FK
        int event_id FK
        string status
        text accessibility_request
        datetime registered_at
    }
```

**Связи:**
- User → Event (1:N) — организатор создаёт мероприятия
- User → Registration (1:N) — пользователь делает записи
- Event → Registration (1:N) — на мероприятии много записей