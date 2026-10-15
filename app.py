from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, User, Event, Registration
from routes.auth import auth_bp
from routes.events import events_bp
from routes.registrations import reg_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(events_bp)
app.register_blueprint(reg_bp)


# ===== Страницы для шаблонов (frontend) =====

@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/events')
def events_page():
    inclusive_only = request.args.get('inclusive') in ('1', 'true')
    query = Event.query.order_by(Event.event_date)
    if inclusive_only:
        query = query.filter_by(is_inclusive=True)
    events = query.all()
    return render_template('events.html', events=events)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return redirect(url_for('profile_page', user_id=user.id))
        return render_template('login.html', error='Неверный email или пароль'), 401
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        role = request.form.get('role', 'user')
        is_deaf = request.form.get('is_deaf') == 'true'
        needs = request.form.get('accessibility_needs') or ''
        if not username or len(password) < 8 or '@' not in email:
            return render_template('register.html',
                                   error='Проверьте поля: имя, email, пароль минимум 8 символов'), 400
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email уже занят'), 400
        user = User(username=username, email=email, role=role,
                    is_deaf=is_deaf, accessibility_needs=needs)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login_page'))
    return render_template('register.html')


@app.route('/profile/<int:user_id>')
def profile_page(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return 'Пользователь не найден', 404
    registrations = Registration.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, registrations=registrations)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)