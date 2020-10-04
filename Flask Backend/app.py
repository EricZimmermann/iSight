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
# from socket import gethostname

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = 'static/uploads'
# SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://hubjon:hubjon-mysql@hubjon.mysql.pythonanywhere-services.com/hubjon$db_hubjon'
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
    confidence = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"<Email: {self.email}, Name: {self.name}, Description: {self.description}, Image URL: {self.image_url}, Confidence: {self.confidence}, Timestamp: {self.timestamp}>"


@app.route('/', methods=['GET', 'POST'])
def default():
    return render_template('base.html')


@app.route('/new-triage', methods=['GET', 'POST'])
def new_triage_request():
    if request.method == 'POST':
        email = request.json['email']
        name = request.json['name']
        description = request.json['description']
        image_base64 = request.json['image_base64']
        # confidence = SCRIPT RETURN
        confidence = 42.69
        decoded_image = base64.b64decode(image_base64.encode('utf-8'))
        image = Image.open(io.BytesIO(decoded_image))
        # image_np = np.array(image)
        primarykey_index = Triage.query.count() + 1
        filename = secure_filename(str(primarykey_index) + '.jpg')
        image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
        new_triage = Triage(email=str(email), name=str(name), description=str(description),
                            image_url=request.url_root + 'static/uploads/' + filename, confidence=confidence)
        db.session.add(new_triage)
        db.session.commit()
        return jsonify({'confidence': float(confidence)})
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
