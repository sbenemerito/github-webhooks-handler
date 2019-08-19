import os
from flask import Flask, request

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
    data = request.get_json()
    # run deploy scripts here

    return (data, 200, None)  # temporarily just return received data


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
