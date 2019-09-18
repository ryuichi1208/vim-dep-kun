#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

from subprocess import check_output
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'


@app.route("/api/commands")
def exec_commands() -> str:
    cmd_info = {
        "git" : f"{check_output(['git', 'version'])}".rstrip('\n'),
        "python" : f"{check_output(['python3', '-V'])}".rstrip('\n')
    }
    return jsonify(cmd_info)


if __name__ == '__main__':
    app.run()
