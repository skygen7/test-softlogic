from . import app, ALLOWED_EXTENSIONS
from flask import render_template, request, jsonify, redirect, url_for, send_from_directory, abort
from main.database import Person, session
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename
import os
from .vector import create_vector, euclidean


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/persons', methods=['GET', 'POST', 'PUT'])
def persons():
    if request.method == 'GET':
        person = {}
        for row in session.query(Person).all():
            person[row.id] = row.name, row.surname, bool(row.vector)
        return jsonify(person)

    if request.method == 'POST':
        data = request.json
        if data and data.get('name') and data.get('surname'):
            session.add(Person(name=data['name'], surname=data['surname'], vector=None))
            session.commit()
            res = session.query(func.max(Person.id).label('id')).one()
            return jsonify(id=res[0])

        abort(400)

    if request.method == 'PUT':
        file = request.files.get('file')
        person_id = request.args.get('id')

        if file and allowed_file(file.filename) and person_id:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            vector = create_vector(file.filename)
            res = session.query(Person).get(person_id)

            if res:
                res.vector = vector
                session.commit()
            return redirect(url_for('uploaded_file', filename=filename))

        abort(400)


@app.route('/persons/<person_id>', methods=['GET', 'DELETE'])
def persons_id(person_id):
    if request.method == 'GET':
        if person_id.isdigit():
            res = session.query(Person).filter(Person.id == person_id).first()
            if res:
                return jsonify(id=res.id, name=res.name, surname=res.surname, vector=bool(res.vector))

        abort(404)

    if request.method == 'DELETE':
        if person_id.isdigit():
            res = session.query(Person).filter(Person.id == person_id).first()
            if res:
                session.delete(res)
                session.commit()
                return jsonify(message='Person was deleted')

        abort(404)


@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/persons/compare')
def compare():
    data = request.json
    if data and data.get('id_1') and data.get('id_2'):
        vector_1 = session.query(Person.vector).filter(Person.id == data['id_1']).first()
        vector_2 = session.query(Person.vector).filter(Person.id == data['id_2']).first()

        if vector_1.vector and vector_2.vector:
            dist = euclidean(vector_1.vector, vector_2.vector)
            return jsonify(euclidean_distance=dist)

    abort(400)
