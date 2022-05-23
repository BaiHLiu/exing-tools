from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import uuid
import os
import check

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['UPLOAD_FOLDER'] = 'upload/'


@app.route('/upload', methods=['POST'])
def upload():
    params = {}
    for key in request.args:
        params[key] = request.args.get(key)

    f = request.files['file']
    print(f.filename)
    filename = str(uuid.uuid4()) + '.' + f.filename.split('.')[-1]

    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return str(filename)


@app.route('/make', methods=['GET'])
def make():
    params = {}
    for key in request.args:
        params[key] = request.args.get(key)

    db = check.make_db(app.config['UPLOAD_FOLDER'] + params['hospital_filename'])
    ret = check.write_ret(app.config['UPLOAD_FOLDER'] + params['school_filename'], db)

    result = {
        'err_code': 0,
        'filename': params['school_filename'],
        'not_in_db': ret[0],
        'error_record': ret[1],
        'success_count': ret[2],
        'err_count': ret[3]

    }

    return jsonify(result)


@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_from_directory('./upload', filename)


if __name__ == '__main__':
    app.run(port=5001, debug=False)
