from datetime import datetime
from flask import Blueprint, jsonify, request
from models import db, Event
from utils.auth_helpers import token_required, role_required
from utils.accessibility import format_event_response

events_bp = Blueprint("events", __name__)


@events_bp.route("/api/events", methods=["GET"])
def list_events():
    query = Event.query
    if request.args.get("inclusive") in ("1", "true"):
        query = query.filter_by(is_inclusive=True)
    events = query.order_by(Event.event_date).all()
    return jsonify([format_event_response(e) for e in events]), 200


@events_bp.route("/api/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify(format_event_response(event)), 200


@events_bp.route("/api/events", methods=["POST"])
@token_required
@role_required("organizer", "admin")
def create_event(user):
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    event_date_raw = data.get("event_date")
    if not title or len(title) > 100:
        return jsonify({"message": "Название обязательно, до 100 символов"}), 400
    if not event_date_raw:
        return jsonify({"message": "Укажите дату и время"}), 400

    try:
        event_date = datetime.fromisoformat(str(event_date_raw).replace(" ", "T"))
    except ValueError:
        return jsonify({"message": "Неверный формат даты"}), 400

    event = Event(
        title=title,
        description=data.get("description"),
        event_date=event_date,
        location=data.get("location"),
        organizer_id=user.id,
        is_inclusive=bool(data.get("is_inclusive", False)),
        sign_language=bool(data.get("sign_language", False)),
        visual_alerts=bool(data.get("visual_alerts", False)),
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({"message": "Мероприятие создано", "id": event.id}), 201


@events_bp.route("/api/events/<int:event_id>", methods=["PUT"])
@token_required
@role_required("organizer", "admin")
def update_event(user, event_id):
    event = Event.query.get_or_404(event_id)
    if event.organizer_id != user.id and user.role != "admin":
        return jsonify({"message": "Можно редактировать только свои мероприятия"}), 403
    data = request.get_json(silent=True) or {}
    for field in ("title", "description", "location"):
        if field in data:
            setattr(event, field, data[field])
    if "event_date" in data:
        try:
            event.event_date = datetime.fromisoformat(str(data["event_date"]).replace(" ", "T"))
        except ValueError:
            return jsonify({"message": "Неверный формат даты"}), 400
    for field in ("is_inclusive", "sign_language", "visual_alerts"):
        if field in data:
            setattr(event, field, bool(data[field]))
    db.session.commit()
    return jsonify(format_event_response(event)), 200


@events_bp.route("/api/events/<int:event_id>", methods=["DELETE"])
@token_required
@role_required("organizer", "admin")
def delete_event(user, event_id):
    event = Event.query.get_or_404(event_id)
    if event.organizer_id != user.id and user.role != "admin":
        return jsonify({"message": "Можно удалять только свои мероприятия"}), 403
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Мероприятие удалено"}), 200
