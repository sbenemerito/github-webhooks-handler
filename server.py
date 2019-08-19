import os
from flask import Flask, jsonify, request

from utils import verify_signature

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """
    Root route, just used to check that server is up and running
    """
    return ('The server is up and running', 200, None)


@app.route('/api/build', methods=['POST'])
def trigger_build():
    """
    Endpoint where GitHub will send a POST request to (payload URL), with
    details of a subscribed event.

    Events: https://developer.github.com/webhooks/#events
    """
    data = request.get_data()
    delivery_id = request.headers.get('X-Github-Delivery')
    event = request.headers.get('X-Github-Event')
    signature = request.headers.get('X-Hub-Signature')

    if event == 'push':
        if not verify_signature(data, signature):
            return (jsonify({ 'msg': 'Hash signatures do not match' }), 400)

        # run deploy scripts here

        return (jsonify({ 'msg': 'Build success' }), 200)

    return (jsonify({ 'msg': 'Payload received' }), 200)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
