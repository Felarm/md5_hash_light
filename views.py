from rq import Queue, Connection
from flask import jsonify, request, current_app
from flask import Flask
from worker import conn

from tasks import count_md5

app = Flask(__name__)


@app.route('/submit', methods=['POST'])
def submit():
    if request.is_json:
        json = request.get_json()
        email = json.get('email')
        url = json.get('url')
    else:
        email = request.values.get('email')
        url = request.values.get('url')
    q = Queue(connection=conn, result_ttl=60*60)
    task = q.enqueue(count_md5, url, email)
    response = {
        'task_id': task.get_id()
    }
    return jsonify(response), 202


@app.route('/check', methods=['GET'])
def check_status():
    task_id = request.args.get('id')
    q = Queue(connection=conn)
    result = q.fetch_job(task_id)
    if result:
        task_status = result.get_status()
        response_object = {'task_status': task_status}
        if task_status == 'failed':
            return jsonify(response_object), 500
        if task_status == 'started':
            return jsonify(response_object), 202
        if task_status == 'finished':
            url = result.result[1]
            hash = result.result[0]
            response_object['task_url'] = url
            response_object['task_hash'] = hash
            return jsonify(response_object), 201
    else:
        response_object = {'status': 'Task not found'}
        return jsonify(response_object), 404
