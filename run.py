#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import datetime
import json
import os
import random
import sys
import urllib.request

from subprocess import check_output
from flask import Flask, jsonify, Response, render_template, request, abort
from flask_httpauth import HTTPBasicAuth, HTTPDigestAuth

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["SECRET_KEY"] = random.randint()
auth = HTTPDigestAuth()
ACCEPTED_IP = ["127.0.0.1", "192.168.1.1/24"]

line_bot_api = LineBotApi(os.environ["LINE_BOT_API"])
handler = WebhookHandler(os.environ["LINE_BOT_CHANNNEL_TOKEN"])


@auth.get_password
def do_digest_auth(id):
    """
    A function that performs Digest authentication by comparing the
    requested user name and password name with its own DB.
    """
    id_list = {"admin": "admin", "testUser01": "testUser01"}

    if id in id_list:
        return id_list.get(id)
    return None


@app.route("/", methods=["GET"])
def index():
    """
    Minimum function for operation check.
    During the test, it is guaranteed to work by tapping here.
    """
    resp = Response("Hello world")
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


@app.route("/api/repos/vim", methods=["GET"])
def get_vim_latest_tag(num=1) -> str:
    """
    Get the latest tag from vim repository on GitHub.
    """
    if request.args.get(num):
        try:
            num = request.args.get("num", type=int)
        except RuntimeError as e:
            print(e)

    url = "https://api.github.com/repos/vim/vim/tags"
    req = urllib.request.Request(url)

    if num == 1:
        with urllib.request.urlopen(req) as res:
            latest_tag = json.load(res)[0]["name"]
        return latest_tag + "\n"
    elif num > 1:
        latest_tags = ""
        with urllib.request.urlopen(req) as res:
            latest_tag = json.load(res)
            for i in range(num):
                latest_tags += latest_tag[i]["name"] + "\n"
        return latest_tags


@app.route("/api/deploy/git", methods=["GET"])
@auth.login_required
def git_push():
    """
    API endpoint for kicking off deployment to GitHub.
    Deployment starts from here
    """
    out = check_output(["bash", "./script/deploy.sh"])
    print(out)
    result = {"push": "success"}

    return jsonify(result), 201


@app.route("/api/__commands", methods=["GET"])
@auth.login_required
def exec_commands() -> str:
    """
    An endpoint for displaying different versions of commands such
    as pip and git on each server.
    If the operation is unstable, tap here to check.
    """
    cmd_info = {
        "git": f"{check_output(['git', 'version'])}".rstrip("\n"),
        "python": f"{check_output(['python3', '-V'])}".rstrip("\n"),
    }

    resp = Response(cmd_info)

    resp.headers["X-APP-VERSION"] = "1.0.0"
    resp.headers["X-APP-NAME"] = "vim-dep-kun"
    resp.headers["X-APP-BUILD-DATE"] = datetime.date.today()

    return resp


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@app.route("/__callback/user", methods=["GET"])
def get_users():
    return "Metrics versions"


@app.errorhandler(404)
@app.errorhandler(500)
def page_not_found(error):
    """
    Error pages handler
    """
    response = jsonify({"error": {"type": error.name, "message": error.description}})
    return response, error.code


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=get_vim_latest_tag(10))
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", debug=True)
