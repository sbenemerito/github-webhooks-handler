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
    details of a subscribed event. For now, we only do something special when
    we get a 'push' event.

    Events: https://developer.github.com/webhooks/#events
    """
    delivery_id = request.headers.get('X-Github-Delivery')  # soon for logging
    event = request.headers.get('X-Github-Event')
    signature = request.headers.get('X-Hub-Signature')

    if event != 'push':
        return (jsonify({'msg': 'Payload received'}), 200)

    data = request.get_data()
    if not verify_signature(data, signature):
        return (jsonify({'msg': 'Hash signatures do not match'}), 400)

    payload = request.get_json()

    # This part is where we execute our deploy/build scripts, depending on how
    # we want it to be run.
    # For this case, we do the following:
    # 1) Check branch, only proceed if branch is `master`.
    # 2) Get project/repository name (for handling many repositories' webhooks)
    # 3) Check if there are npm dependency changes via commits' modified files
    # 4) If so, make sure we could tell the deploy script (using flags, etc.)
    # 5) Execute deploy script with the project name, and the above flag (#4)

    # only proceed if branch is master
    if payload.get('ref') == 'refs/heads/master':
        # get project name
        project_name = payload.get('repository').get('name')

        # check if there are npm dependency changes
        commits = payload.get('commits')
        dependency_change_commits = [commit for commit in commits
                                     if 'package.json' in commit['modified']]

        # if len(dependency_change_commits) > 0:
        #     ~/deploy -d <project_name>
        # else:
        #     ~/deploy <project_name>

        return (jsonify({'msg': 'Build success'}), 200)

    return (jsonify({'msg': 'Valid, but push not in master branch'}), 200)


if __name__ == '__main__':
    app.run()
