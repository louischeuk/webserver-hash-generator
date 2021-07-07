import concurrent.futures
import time
from datetime import datetime
import os
import sys

from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from hashing import md_5, sha_1, sha_256
from apscheduler.schedulers.background import BackgroundScheduler

expire_time = float(sys.argv[1])  # seconds
num_of_threads = 4
refresh_time = 0.5


def delete_if_beyond_time():
    db.session\
        .query(File)\
        .filter(time.mktime(datetime.today().timetuple()) - File.time > expire_time)\
        .delete()
    db.session.commit()


def sensor():
    delete_if_beyond_time()


schedule = BackgroundScheduler(daemon=True)
schedule.add_job(sensor, 'interval', minutes=refresh_time)
schedule.start()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hash.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret key"
db = SQLAlchemy(app)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    hash_md5 = db.Column(db.Text)
    hash_sha1 = db.Column(db.Text)
    hash_sha256 = db.Column(db.Text)
    time = db.Column(db.Float, default=time.mktime(datetime.today().timetuple()))


db.create_all()


@app.route("/")
def hello():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file.filename == '':
        return "No file uploaded", 400

    filename = secure_filename(file.filename)
    file.save(filename)
    path = os.path.realpath(filename)

    hash_md5 = md_5(path)
    hash_sha1 = sha_1(path)
    hash_256 = sha_256(path)

    file = File(file=file.read(), name=filename,
                hash_md5=hash_md5, hash_sha1=hash_sha1, hash_sha256=hash_256)
    db.session.add(file)
    db.session.commit()

    os.remove(path)

    return "Upload is successful. Token of the file [" + str(file.name) + "]:  " \
           + str(file.id), 200


@app.route('/<int:id>/<string:hash_type>', methods=['GET'])
def get_img(id, hash_type):
    file = File.query.filter_by(id=id).first()
    if not file:
        return "No img with that id", 404

    s = "Hash of the file [" + str(file.name) + "]:  "

    if hash_type == 'md5':
        return "md5sum " + s + file.hash_md5, 200
    elif hash_type == 'sha1':
        return "SHA-1 " + s + file.hash_sha1, 200
    elif hash_type == 'sha256':
        return "SHA-256 " + s + file.hash_sha256, 200
    else:
        return "hash type not available", 404


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(app.run(debug=True)) for _ in range(num_of_threads)]
        print(results)

