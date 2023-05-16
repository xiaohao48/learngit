from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/watch_list?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型的监控

db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)


# 用户加载回调函数
@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'login'


# 模板上下文处理函数
@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)


from watchlist import views, errors, commands

# coverage run --source=watchlist test_watchlist.py
# coverage report
# coverage html
