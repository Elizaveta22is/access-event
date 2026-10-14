def format_event_response(event):
    """Форматирование ответа с инклюзивными полями."""
    response = {
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'event_date': event.event_date.isoformat() if event.event_date else None,
        'location': event.location,
        'organizer': event.organizer.username if event.organizer else None,
    }
    if event.is_inclusive:
        response['accessibility'] = {
            'inclusive': True,
            'sign_language': event.sign_language,
            'visual_alerts': event.visual_alerts,
            'description': build_accessibility_description(event)
        }
    else:
        response['accessibility'] = {'inclusive': False}
    return response

def build_accessibility_description(event):
    """Генерация текстового описания доступности."""
    features = []
    if event.sign_language:
        features.append('Сурдоперевод')
    if event.visual_alerts:
        features.append('Визуальные уведомления')
    if features:
        return 'Доступно: ' + ', '.join(features)
    return 'Мероприятие отмечено как инклюзивное'
