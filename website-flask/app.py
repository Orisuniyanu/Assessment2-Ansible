from flask import Flask, render_template, render_template_string
import socket
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    app_start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Upstream Health</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #eef2f7; margin: 40px; }
            h1 { color: #1a5276; font-size: 36px; text-align: center; }
            .section { background: #fff; padding: 20px; margin-top: 30px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
            p { font-size: 16px; }
        </style>
    </head>
    <body>
        <h1>Upstream Health</h1>
        <div class="section">
            <p><strong>🖥️ Hostname:</strong> {{ hostname }}</p>
            <p><strong>🌐 IP Address:</strong> {{ ip }}</p>
            <p><strong>🚦 Status:</strong> ✅ OK</p>
            <p><strong>⏰ App Started At:</strong> {{ app_start }}</p>
        </div>
    </body>
    </html>
    """

    return render_template_string(
        html_template,
        hostname=hostname,
        ip=ip_address,
        app_start=app_start_time
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
