# web/app.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License
from flask import Flask, render_template, request, redirect, url_for
from config import Meta

app = Flask(__name__)

# TODO:
# - Better Interface
# - More Meta Variables
# - Login (for security)
# - More settings in the WebApp
# - - User list
# - - Role list
# - - Channel and Folders

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # update Meta variables dynamically
        Meta.log = request.form.get("log") == "on"
        Meta.print_console = request.form.get("print_console") == "on"
        Meta.output = request.form.get("output") == "on"
        Meta.admin_role = request.form.get("admin_role")
        Meta.ai_model = request.form.get("ai_model")
        return redirect(url_for("index"))
    meta_vars = {
        "log": Meta.log,
        "print_console": Meta.print_console,
        "output": Meta.output,
        "admin_role": Meta.admin_role,
        "ai_model": Meta.ai_model
    }
    return render_template("index.html", meta=meta_vars)

def start_web():
    if not Meta.web_active:
        if Meta.print_console:
            print("[WEB] Web server is disabled in config.")
        return

    host = "127.0.0.1" if Meta.only_localhost else "0.0.0.0"
    if Meta.print_console:
        print(f"[WEB] Starting Flask web server on {host}:5000...")
    app.run(host=host, port=5000, debug=Meta.web_debug) # Start WebApp