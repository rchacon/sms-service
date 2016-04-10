"""Web application."""

import json
import os

from flask import abort, Flask, jsonify, request
import pika

from db import Mongo


app = Flask(__name__)

mongo = Mongo(app)


@app.errorhandler(400)
def bad_request(e):
    """Jsonify 400 response."""
    resp = jsonify({'error': str(e)})
    resp.status_code = 400

    return resp


@app.route('/api/sms', methods=['GET', 'POST'])
def get_sms():
    """SMS endpoint for retrieving and sending messages."""
    if request.method == 'POST':
        data = request.get_json()
        if 'message' not in data or 'phone' not in data:
            abort(400)

        try:
            new_task(data)
            return jsonify({
                'status': 'success'
            })
        except Exception as ex:
            resp = jsonify({
                'message': str(ex)
            })
            resp.status_code = 500
            return resp

    phone = request.args.get('phone')

    if phone is None:
        abort(400)

    messages = list(mongo.db.messages.find({'phone': phone}, {'_id': 0}))

    return jsonify({
        'results': messages,
        'count': len(messages)
    })


def new_task(data):
    """Add task to rabbit."""
    rabbit_host = os.getenv('RABBIT_HOST', 'localhost')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(rabbit_host)
    )
    channel = connection.channel()
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
    )
    connection.close()


if __name__ == '__main__':
    app.run(debug=True)
