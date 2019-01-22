from flask import Flask
from flask_migrate import Migrate

from error_handlers import method_not_allowed
from models import db
from views import views

app = Flask(__name__)
app.config.from_pyfile('settings.py', silent=True)
app.register_blueprint(views)
app.register_error_handler(405, method_not_allowed)
db.init_app(app)
migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run(debug=True)
