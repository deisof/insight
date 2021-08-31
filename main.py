from flask import Flask
from flask import make_response, jsonify
from flask_login import LoginManager
from flask_restful import Api
from data import db_session
from data import test_api, user_api
from data.users import User
import cv2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)
camera = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('data_cam/haarcascades/haarcascade_frontalface_alt.xml')


def main():
    db_session.global_init("db/proctoring.db")

    @login_manager.user_loader
    def load_user(user_id):
        session = db_session.create_session()
        return session.query(User).get(user_id)

    app.register_blueprint(test_api.blueprint)
    app.register_blueprint(user_api.blueprint)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    app.run()


if __name__ == '__main__':
    main()
