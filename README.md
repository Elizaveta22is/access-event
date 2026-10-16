# AccessEvent — инклюзивная платформа мероприятий

Веб-платформа для организации мероприятий, доступная людям с нарушениями слуха: визуальные уведомления вместо звуковых, читаемая цветовая индикация статусов.

## Стек технологий

| Слой | Технология |
|---|---|
| Backend | Python 3.11, Flask |
| База данных | SQLAlchemy ORM (SQLite локально, PostgreSQL в продакшене) |
| Frontend | HTML5, CSS3, JavaScript, Jinja2 |
| Тестирование | pytest |
| CI/CD | GitHub Actions |
| Контейнеризация | Docker, docker compose |

## Как запустить

### Локально

1. Скопировать .env.example в .env и заполнить SECRET_KEY и DATABASE_URL.
2. Установить зависимости: pip install -r requirements.txt
3. Запустить: python app.py
4. Открыть: http://127.0.0.1:5000

## Тесты

python -m pytest -v

Ожидаемый результат: 14 passed.

## Структура проекта

- app.py — точка входа
- models.py — SQLAlchemy-модели
- config.py — конфигурация
- routes/ — API-эндпоинты
- utils/ — JWT, хеширование, инклюзивные поля
- templates/ — Jinja2-шаблоны
- static/css, static/js — стили и скрипты
- tests/ — тесты pytest
- docs/ — документация

## Документация

- docs/test_cases.md — 12 тест-кейсов
- docs/bug_reports.md — 3 баг-репорта
- docs/user_manual.md — руководство пользователя
- docs/admin_manual.md — руководство администратора
- docs/api.md — описание API
- docs/assessment.md — SWOT-анализ и направления развития
- docs/speech.md — тезисы выступления
- docs/defense_answers.md — ответы на вопросы защиты

## Инклюзивность

- Визуальные уведомления вместо звуковых (aria-live)
- ARIA-атрибуты на навигации и формах
- Цветовая индикация статусов регистрации (pending/confirmed/cancelled)
- Поля инклюзивности: is_deaf, is_inclusive, sign_language, visual_alerts

## Автор

Возняк Максим, учебная практика ПМ.05, 3 семестр.