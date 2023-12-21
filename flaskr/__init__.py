import os

from flask import Flask

from . import auth
from . import blog
from . import db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    """
    SECRET_KEY 是被 Flask 和扩展用于保证数据安全的。在开 发过程中，为了方便可以设置为 'dev' ，但是在发布的时候应当 使用一个随机值来重载它。
    DATABASE SQLite 数据库文件存放在路径。它位于 Flask 用于存 放实例的 app.instance_path 之内。
    """
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
