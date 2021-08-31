import flask
from flask import render_template, request, Response
from flask_login import current_user, login_required
from werkzeug.utils import redirect
from data import db_session
from data.test import Test
from forms.test import TestForm, Ready
import functions as funcs
from Timer import RepeatedTimer
from main import camera, face_cascade

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
    return Response(funcs.generate_frames(camera, face_cascade),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@blueprint.route("/check")
def test_func():
    return render_template('check.html')


@blueprint.route("/testing/<int:test_id>", methods=['GET', 'POST'])
def testing(test_id):
    form = Ready()
    session = db_session.create_session()
    test = session.query(Test).filter(Test.id == f'{test_id}').first()
    if request.method == "POST":

        if form.submit_ready.data:
            test.is_finished = 1
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

# @blueprint.route('/addjob/<int:job_id>', methods=['GET', 'POST'])
# @login_required
# def edit_job(job_id):
#     form = JobsForm()
#     session = db_session.create_session()
#     job = session.query(Jobs).filter(Jobs.id == job_id, Jobs.employer == current_user.id).first()
#     if request.method == "GET":
#         if job:
#             form.description.data = job.description
#             form.address.data = job.address
#             form.date.data = job.date
#             form.info.data = job.info
#             form.is_finished.data = job.is_finished
#         else:
#             abort(404)
#     if form.validate_on_submit():
#         if job:
#             job.description = form.description.data
#             job.address = form.address.data
#             job.date = form.date.data
#             job.info = form.info.data
#             job.is_finished = form.is_finished.data
#
#             address = form.address.data
#             geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
#             geocoder_params = {
#                 "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
#                 "geocode": address,
#                 "format": "json"}
#             response = requests.get(geocoder_api_server, params=geocoder_params)
#             if response:
#                 json_response = response.json()
#                 toponym = json_response["response"]["GeoObjectCollection"][
#                     "featureMember"][0]["GeoObject"]
#                 job.coords = toponym["Point"]["pos"]
#
#             session.commit()
#             return redirect('/myjobs')
#         else:
#             abort(404)
#     return render_template('edit_job.html', title='Редактирование обращения', form=form)
#
#
# @blueprint.route('/job_delete/<int:job_id>', methods=['GET', 'POST'])
# @login_required
# def job_delete(job_id):
#     session = db_session.create_session()
#     job = session.query(Jobs).filter(Jobs.id == job_id, Jobs.employer == current_user.id).first()
#     if job:
#         session.delete(job)
#         session.commit()
#     else:
#         abort(404)
#     return redirect('/myjobs')
#
#
