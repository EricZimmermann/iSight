import base64
import datetime
import io
import json
import os

import requests
from PIL import Image
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
from inference import infer
# from socket import gethostname

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = 'static/uploads'
# SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://implementai2020t:Helloworld1!@implementai2020triage.mysql.pythonanywhere-services.com/implementai2020t$implementai2020triage'
# app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.root_path + '/db_implementai2020triage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])


class Triage(db.Model):
    __tablename__ = 'triages'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(1024), nullable=False)
    name = db.Column(db.String(1024), nullable=False)
    description = db.Column(db.String(1024))
    image_url = db.Column(db.String(1024), nullable=False, default='')
    disease = db.Column(db.String(1024), nullable=True)
    prob = db.Column(db.Float, nullable=True)
    conf = db.Column(db.String(1024), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"<Email: {self.email}, Name: {self.name}, Description: {self.description}, Image URL: {self.image_url}, Disease: {self.disease}, Prob: {self.prob}, Confidence: {self.conf}, Timestamp: {self.timestamp}>"


@app.route('/')
def default():
    return render_template('base.html')


@app.route('/new-triage', methods=['GET', 'POST'])
def new_triage_request():
    if request.method == 'POST':
        email = request.json['email']
        name = request.json['name']
        description = request.json['description']
        image_base64 = request.json['image_base64']
        decoded_image = base64.b64decode(image_base64.encode('utf-8'))
        image = Image.open(io.BytesIO(decoded_image))
        primarykey_index = Triage.query.count() + 1
        filename = secure_filename(str(primarykey_index) + '.jpg')
        image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
        results = infer(img_path=app.config["IMAGE_UPLOADS"] + "/" + filename, ensemble_path='static/balanced_ensembles')
        disease = results['disease']
        prob = results['prob']
        conf = results['conf']
        new_triage = Triage(email=str(email), name=str(name), description=str(description),
                            image_url=request.url_root + 'static/uploads/' + filename, disease=str(disease), prob=float(prob), conf=str(conf))
        db.session.add(new_triage)
        db.session.commit()
        return jsonify({'disease': str(disease), 'prob': float(prob), 'conf': str(conf), })
    return render_template('new-triage.html')


@app.route('/get-triages', methods=['GET', 'POST'])
def get_triages():
    if request.method == 'GET':
        email = str(request.args.get('email'))
        connection = engine.raw_connection()
        cur = connection.cursor()
        cur.execute('SELECT * FROM triages WHERE email = "{0}"'.format(email))
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return jsonify(requests=json_data)
        # return json.dumps(json_data)
    return render_template('get-triages.html')


@app.route('/dummy')
def dummy_request():
    # url = 'http://implementai2020triage.pythonanywhere.com/new-triage'
    url = 'http://127.0.0.1:5000/new-triage'
    email = 'test@gmail.com'
    name = 'Left Arm Birthmark'
    description = 'Dark brown birthmark on left arm'
    with open('static/lenna.png', 'rb') as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    triage_request_json = {'email': email, 'name': name, 'description': description, 'image_base64': image_base64}
    response = requests.post(url=url, json=triage_request_json)
    print(response.status_code, response.reason, response.text)
    return render_template('dummy.html')


if __name__ == '__main__':
    db.create_all()
    app.run()
