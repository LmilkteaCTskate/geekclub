
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'  # 在生产环境中使用强随机密钥
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///geek.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化扩展
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# 定义模型
class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100))
    max_participants = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    registrations = db.relationship('Registration', backref='activity', lazy=True, cascade='all, delete-orphan')

    @property
    def participant_count(self):
        return len(self.registrations)

    @property
    def is_active(self):
        return self.date > datetime.utcnow()

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(20), nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    class_name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('请先登录')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# 路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/activities')
def activities():
    activities = Activity.query.order_by(Activity.date.desc()).all()
    return render_template('activities.html', 
                         activities=activities,
                         page_title='活动列表',
                         page_icon='calendar-alt')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 处理报名表单
        registration = Registration(
            name=request.form['name'],
            student_id=request.form['student_id'],
            grade=request.form['grade'],
            class_name=request.form['class_name'],
            phone=request.form['phone'],
            email=request.form['email'],
            activity_id=request.form['activity_id']
        )
        db.session.add(registration)
        db.session.commit()
        flash('报名成功！')
        return redirect(url_for('register'))
    
    activities = Activity.query.filter(Activity.date > datetime.utcnow()).all()
    return render_template('register.html', 
                         activities=activities,
                         page_title='加入我们',
                         page_icon='user-plus')

@app.route('/about')
def about():
    return render_template('about.html',
                         page_title='关于我们',
                         page_icon='info-circle')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            flash('登录成功！')
            return redirect(url_for('admin_dashboard'))
        flash('用户名或密码错误')
    return render_template('admin/login.html')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # 获取统计数据
    total_registrations = Registration.query.count()
    active_activities = Activity.query.filter(Activity.date > datetime.utcnow()).count()
    recent_activities = Activity.query.order_by(Activity.date.desc()).limit(5).all()
    recent_registrations = Registration.query.order_by(Registration.created_at.desc()).limit(5).all()
    
    # 计算增长率（示例数据）
    registration_growth = 15
    activity_growth = 10
    monthly_activity_rate = 85
    completion_rate = 75
    upcoming_activities = 3

    # 如果是AJAX请求，返回JSON数据
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'success': True,
            'message': '数据已刷新'
        })

    return render_template('admin/dashboard.html',
                         total_registrations=total_registrations,
                         active_activities=active_activities,
                         recent_activities=recent_activities,
                         recent_registrations=recent_registrations,
                         registration_growth=registration_growth,
                         activity_growth=activity_growth,
                         monthly_activity_rate=monthly_activity_rate,
                         completion_rate=completion_rate,
                         upcoming_activities=upcoming_activities)

@app.route('/admin/activities')
@login_required
def admin_activities():
    activities = Activity.query.order_by(Activity.date.desc()).all()
    return render_template('admin/activities.html', activities=activities)

@app.route('/admin/activities/<int:id>', methods=['DELETE'])
@login_required
def admin_delete_activity(id):
    activity = Activity.query.get_or_404(id)
    db.session.delete(activity)
    db.session.commit()
    return jsonify({'success': True, 'message': '活动已删除'})

@app.route('/admin/registrations')
@login_required
def admin_registrations():
    registrations = Registration.query.order_by(Registration.created_at.desc()).all()
    return render_template('admin/registrations.html', registrations=registrations)

@app.route('/admin/registrations/<int:id>', methods=['GET', 'DELETE'])
@login_required
def admin_registration(id):
    registration = Registration.query.get_or_404(id)
    if request.method == 'DELETE':
        db.session.delete(registration)
        db.session.commit()
        return jsonify({'success': True, 'message': '报名记录已删除'})
    return render_template('admin/registration_details.html', registration=registration)

@app.route('/admin/activities/new', methods=['GET', 'POST'])
@login_required
def admin_new_activity():
    if request.method == 'POST':
        activity = Activity(
            title=request.form['title'],
            description=request.form['description'],
            date=datetime.strptime(request.form['date'], '%Y-%m-%dT%H:%M'),
            location=request.form['location'],
            max_participants=int(request.form['max_participants'])
        )
        db.session.add(activity)
        db.session.commit()
        flash('活动创建成功！')
        return redirect(url_for('admin_activities'))
    return render_template('admin/new_activity.html')

@app.route('/admin/activities/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_activity(id):
    activity = Activity.query.get_or_404(id)
    if request.method == 'POST':
        activity.title = request.form['title']
        activity.description = request.form['description']
        activity.date = datetime.strptime(request.form['date'], '%Y-%m-%dT%H:%M')
        activity.location = request.form['location']
        activity.max_participants = int(request.form['max_participants'])
        db.session.commit()
        flash('活动更新成功！')
        return redirect(url_for('admin_activities'))
    return render_template('admin/edit_activity.html', activity=activity)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    flash('已退出登录')
    return redirect(url_for('admin_login'))

# 错误处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# 初始化数据库
def init_db():
    with app.app_context():
        db.create_all()
        # 创建默认管理员账户
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(username='admin')
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
