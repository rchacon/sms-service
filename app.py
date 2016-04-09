from flask import abort, Flask, jsonify, request

from db import Mongo


app = Flask(__name__)

mongo = Mongo(app)


@app.errorhandler(400)
def bad_request(e):
    resp = jsonify({'error': str(e)})
    resp.status_code = 400

    return resp


@app.route('/api/sms', methods=['GET'])
def get_sms():
    phone = request.args.get('phone')

    if phone is None:
        abort(400)

    messages = list(mongo.db.messages.find({'phone': phone}, {'_id': 0}))

    return jsonify({
        'results': messages,
        'count': len(messages)
    })


if __name__ == '__main__':
    app.run(debug=True)
