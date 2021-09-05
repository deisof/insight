import flask
from flask import render_template, request, Response, abort
from flask_login import current_user, login_required
from werkzeug.utils import redirect
from data import db_session
from data.test import Test
from forms.test import TestForm, Ready
import functions as funcs
from main import camera
import cv2
from functions import s, write_file
import string
import secrets
from flask import send_file

blueprint = flask.Blueprint('test_api', __name__, template_folder='templates')


@blueprint.route("/", methods=['GET', 'POST'])
def welcome():
    return render_template("welcome.html")


@blueprint.route("/base", methods=['GET', 'POST'])
@login_required
def base():
    return render_template("base.html")


@blueprint.route("/video")
@login_required
def video():
    camera = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('data_cam/haarcascades/haarcascade_frontalface_alt.xml')
    return Response(funcs.generate_frames(camera, face_cascade),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@blueprint.route("/check")
def test_func():
    return render_template('check.html')


@blueprint.route("/testing/<int:test_id>", methods=['GET', 'POST'])
def testing(test_id):
    form = Ready()
    session = db_session.create_session()
    test = session.query(Test).filter(Test.id == test_id).first()

    if request.method == "POST":

        if form.submit_ready.data:
            camera.release()
            test.is_finished = 1
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in range(6))
            test.result = f'data_cam/{password}.txt'
            write_file(s, password)
            session.commit()

        return redirect('/history')
    return render_template('testing.html', form=form, test=test)


@blueprint.route("/about")
def about():
    return render_template('about.html')


@blueprint.route("/help")
def helper():
    return render_template('help.html')


@blueprint.route("/active")
def active():
    session = db_session.create_session()
    test_st = session.query(Test).filter(Test.login_student == current_user.login, Test.is_finished == 0).all()
    test_te = session.query(Test).filter(Test.login_teacher == current_user.login, Test.is_finished == 0).all()
    return render_template('active.html', test_st=test_st, test_te=test_te)


@blueprint.route("/history")
def history():
    session = db_session.create_session()
    test = session.query(Test).filter(Test.login_student == current_user.login, Test.is_finished == 1).all()
    test1 = session.query(Test).filter(Test.login_teacher == current_user.login, Test.is_finished == 1).all()
    test.extend(test1)

    return render_template('history.html', test=test)


@blueprint.route('/add_test', methods=['GET', 'POST'])
@login_required
def add_test():
    form = TestForm()
    session = db_session.create_session()
    test = Test()
    if form.validate_on_submit():
        test.login_student = form.login_student.data
        test.login_teacher = current_user.login
        test.description = form.description.data
        test.is_finished = 0

        session.add(test)
        session.commit()

        return redirect('/active')
    return render_template('add.html', form=form)


@blueprint.route('/edit_test/<int:test_id>', methods=['GET', 'POST'])
@login_required
def edit_job(test_id):
    form = TestForm()
    session = db_session.create_session()
    test = session.query(Test).filter(Test.id == test_id, Test.login_teacher == current_user.login).first()
    if request.method == "GET":
        if test:
            form.login_student.data = test.login_student
            form.description.data = test.description
        else:
            abort(404)
    if form.validate_on_submit():
        if test:
            test.login_student = form.login_student.data
            test.login_teacher = current_user.login
            test.description = form.description.data
            test.is_finished = 0

            session.commit()
            return redirect('/active')
        else:
            abort(404)
    return render_template('add.html', title='Редактирование тестирования', form=form)


@blueprint.route('/delete_test/<int:test_id>', methods=['GET', 'POST'])
@login_required
def test_delete(test_id):
    session = db_session.create_session()
    test = session.query(Test).filter(Test.id == test_id, Test.login_teacher == current_user.login).first()
    if test:
        session.delete(test)
        session.commit()
    else:
        abort(404)
    return redirect('/active')


@blueprint.route('/data_cam/<path:filename>', methods=['GET', 'POST'])
@login_required
def download(filename):
    return send_file(filename)
