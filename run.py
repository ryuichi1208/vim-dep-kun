#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

from subprocess import check_output
from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth, HTTPDigestAuth

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = "aaa"

auth = HTTPDigestAuth()


@auth.get_password
def do_basic_auth(id):
    id_list = {
        "admin": "admin"
    }

    if id in id_list:
        return id_list.get(id)
    return None


@app.route('/', methods=['GET'])
def index():
    return 'Hello World!'


@app.route("/api/git", methods=['GET'])
@auth.login_required
def git_push():
    out = check_output(["bash", "./script/deploy.sh"])
    print(out)
    result = {'push': 'success'}
    return jsonify(result), 201


@app.route("/api/commands", methods=['GET'])
@auth.login_required
def exec_commands() -> str:
    cmd_info = {
        "git" : f"{check_output(['git', 'version'])}".rstrip('\n'),
        "python" : f"{check_output(['python3', '-V'])}".rstrip('\n')
    }
    return jsonify(cmd_info)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', debug=True)
