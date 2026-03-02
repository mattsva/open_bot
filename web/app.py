from flask import Flask, render_template, request, redirect, url_for
from config import Meta
import threading
import time
from werkzeug.serving import make_server

app = Flask(__name__)

server = None
server_thread = None
monitor_thread = None
lock = threading.Lock()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        Meta.log = request.form.get("log") == "on"
        Meta.print_console = request.form.get("print_console") == "on"
        Meta.output = request.form.get("output") == "on"
        Meta.web_active = request.form.get("web_active") == "on"
        Meta.web_debug = request.form.get("web_debug") == "on"
        Meta.only_localhost = request.form.get("only_localhost") == "on"
        Meta.admin_role = request.form.get("admin_role")
        Meta.ai_model = request.form.get("ai_model")

        return redirect(url_for("index"))

    return render_template("index.html", meta=Meta.__dict__)

def run_server():
    global server

    host = "127.0.0.1" if Meta.only_localhost else "0.0.0.0"

    with lock:
        server = make_server(host, 5000, app)

    if Meta.print_console:
        print(f"[WEB] Server running on {host}:5000")

    try:
        server.serve_forever()
    finally:
        if Meta.print_console:
            print("[WEB] Server stopped")

        with lock:
            server = None


def start_server():
    global server_thread

    with lock:
        if server_thread and server_thread.is_alive():
            return # Already running

        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()


def stop_server():
    global server, server_thread

    with lock:
        if server:
            server.shutdown()

    if server_thread:
        server_thread.join(timeout=5)


def monitor_web_flag():
    while True:
        if Meta.web_active:
            start_server()
        else:
            stop_server()

        time.sleep(1)


def start_web():
    global monitor_thread

    if monitor_thread and monitor_thread.is_alive():
        return

    monitor_thread = threading.Thread(target=monitor_web_flag, daemon=True)
    monitor_thread.start()

    if Meta.print_console:
        print("[WEB] Monitor started")