from flask import Flask, render_template_string, request
import socket
import os
import requests
import datetime

app = Flask(__name__)
uptime_history = {}
app_start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@app.route('/monitor')
def monitor():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    servers_env = os.getenv("ALL_SERVERS", "")
    all_servers = servers_env.split(",") if servers_env else []

    server_status = {}
    server_identity = {}
    for server in all_servers:
        try:
            r = requests.get(f"http://{server}/health", timeout=2)
            is_online = r.status_code == 200
            identity = r.text if is_online else "No response"
        except requests.exceptions.RequestException:
            is_online = False
            identity = "Unreachable"

        server_status[server] = is_online
        server_identity[server] = identity

        if server not in uptime_history:
            uptime_history[server] = {
                "last_online": None,
                "last_offline": None,
                "previous_status": None
            }

        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        previous_status = uptime_history[server]["previous_status"]
        if is_online and previous_status != True:
            uptime_history[server]["last_online"] = now_time
        elif not is_online and previous_status != False:
            uptime_history[server]["last_offline"] = now_time

        uptime_history[server]["previous_status"] = is_online

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Iyanu Dashboard LoadBalancer</title>
        <meta http-equiv="refresh" content="10">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #eef2f7; }
            h1 { color: #1a5276; font-size: 36px; text-align: center; margin-bottom: 40px; }
            .section { background: #fff; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
            ul { list-style: none; padding-left: 0; }
            li { padding: 5px 0; }
            .online { color: green; }
            .offline { color: red; }
            .refresh-btn { padding: 10px 20px; background-color: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; }
            .refresh-btn:hover { background-color: #2980b9; }
            .history { font-size: 12px; color: #666; margin-left: 20px; }
        </style>
    </head>
    <body>
        <h1>Iyanu Dashboard LoadBalancer</h1>

        <div class="section">
            <h2>Hello from: {{ hostname }}</h2>
            <p>This server is online and responding to traffic.</p>
            <p><strong>Container IP Address:</strong> {{ ip }}</p>
            <p><strong>App started at:</strong> {{ app_start }}</p>
            <form method="get" action="/monitor">
                <button class="refresh-btn" type="submit">🔄 Refresh Now</button>
            </form>
        </div>

        <div class="section">
            <h2>Server Status</h2>
            <ul>
                {% for srv in server_status %}
                    <li class="{{ 'online' if server_status[srv] else 'offline' }}">
                        {{ '🟢' if server_status[srv] else '🔴' }} {{ srv }}
                        <br><strong>{{ server_identity[srv] }}</strong>
                        <div class="history">
                            {% if uptime_history[srv]['last_online'] %}
                                Online since: {{ uptime_history[srv]['last_online'] }}
                            {% endif %}
                            {% if uptime_history[srv]['last_offline'] %}<br>
                                Last offline: {{ uptime_history[srv]['last_offline'] }}
                            {% endif %}
                        </div>
                    </li>
                {% endfor %}
            </ul>
        </div>
    </body>
    </html>
    """

    return render_template_string(
        html_template,
        hostname=hostname,
        ip=ip_address,
        app_start=app_start_time,
        server_status=server_status,
        uptime_history=uptime_history,
        server_identity=server_identity
    )

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
