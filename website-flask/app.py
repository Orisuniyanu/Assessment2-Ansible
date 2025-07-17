from flask import Flask, render_template_string
import socket
import os
import requests
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get all available servers from ENV
    servers_env = os.getenv("ALL_SERVERS", "")
    all_servers = servers_env.split(",") if servers_env else []

    # Check which servers are online
    online_servers = []
    for server in all_servers:
        try:
            r = requests.get(f"http://{server}/health", timeout=2)
            if r.status_code == 200:
                online_servers.append(server)
        except requests.exceptions.RequestException:
            continue

    # HTML template
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask Server Status</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            h1 { color: #2c3e50; }
            .section { background: #fff; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
            ul { list-style: none; padding-left: 0; }
            li { padding: 5px 0; }
        </style>
    </head>
    <body>
        <div class="section">
            <h1>Hello from: {{ hostname }}</h1>
            <p>This server is online and responding to traffic.</p>
            <p><strong>Container IP Address:</strong> {{ ip }}</p>
            <p><strong>Timestamp:</strong> {{ timestamp }}</p>
        </div>

        <div class="section">
            <h2>Online Servers</h2>
            {% if online_servers %}
                <ul>
                    {% for srv in online_servers %}
                        <li>🟢 {{ srv }}</li>
                    {% endfor %}
                </ul>
            {% else %}
                <p>No servers are currently online.</p>
            {% endif %}
        </div>
    </body>
    </html>
    """

    return render_template_string(
        html_template,
        hostname=hostname,
        ip=ip_address,
        timestamp=timestamp,
        online_servers=online_servers
    )

@app.route('/health')
def health():
    return "OK", 200

@app.route('/status')
def status():
    return f"This request was served by container: {socket.gethostname()}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
