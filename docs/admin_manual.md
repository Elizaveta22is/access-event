# Руководство администратора AccessEvent

## 1. Системные требования
- Python 3.11+
- PostgreSQL 15+ (или SQLite для отладки)
- Docker 24+ (опционально)

## 2. Развёртывание
Локально:
1. python -m venv venv; активировать
2. pip install -r requirements.txt
3. Настроить .env
4. python app.py

Контейнерно:
- docker compose up -d
- docker compose down

## 3. Переменные окружения
| Переменная | Назначение | Пример |
| DATABASE_URL | Подключение к БД | sqlite:///accessevent.db |
| SECRET_KEY | Подпись JWT | длинная строка |
| TESTING | Тестовая SQLite | 1 |

## 4. Роли
| Роль | Права |
| user | регистрация на мероприятия |
| organizer | всё user + создание мероприятий |
| admin | всё organizer + удаление любых |

## 5. Резервное копирование
pg_dump -U postgres accessevent > backup.sql

## 6. Типовые проблемы
1. Password authentication failed — неверный пароль в .env
2. Connection refused — не запущен PostgreSQL
3. Address already in use — старый процесс на порту 5000
4. Таблицы не создаются — проверьте db.create_all()
