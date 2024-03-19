from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import socket

app = Flask(__name__)

DATABASE = 'servo_controller.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Enables column access by name: row['column_name']
    return conn

@app.route('/', methods=['GET', 'POST'])
def home():
    conn = get_db_connection()
    servers = conn.execute('SELECT * FROM server_hosts').fetchall()
    presets = conn.execute('SELECT * FROM preset_positions').fetchall()
    conn.close()

    message = ''
    if request.method == 'POST':
        if 'send_command' in request.form:
            host = request.form['host'].split(":")[0]
            port = int(request.form['host'].split(":")[1])
            command = request.form.get('preset_command', request.form['command'])
            try:
                response = send_command(host, port, command)
                message = f'Server response: {response}'
            except Exception as e:
                message = f'Failed to send command: {e}'
        elif 'add_server' in request.form:
            host = request.form['new_host']
            port = request.form['new_port']
            conn = get_db_connection()
            conn.execute('INSERT INTO server_hosts (host, port) VALUES (?, ?)', (host, port))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))
        elif 'add_preset' in request.form:
            name = request.form['preset_name']
            command = request.form['preset_command']
            conn = get_db_connection()
            conn.execute('INSERT INTO preset_positions (name, command) VALUES (?, ?)', (name, command))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))

    return render_template_string('''
<html>
    <head>
        <title>Servo Controller</title>
        <style>
            body { font-family: Arial, sans-serif; }
            .container { padding: 20px; }
            .form-group { margin-bottom: 10px; }
            label { margin-right: 10px; }
            input[type="text"], input[type="number"], select { margin-right: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Select Server and Send Command</h2>
            <form method="post">
                <input type="hidden" name="send_command">
                <div class="form-group">
                    <label for="host">Server:</label>
                    <select name="host" id="host">
                        {% for server in servers %}
                        <option value="{{ server['host'] }}:{{ server['port'] }}">{{ server['host'] }}:{{ server['port'] }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="form-group">
                    <label for="command">Command:</label>
                    <input type="text" id="command" name="command" placeholder="e.g., 0:45,90|1:30,60">
                    OR
                    <select name="preset_command">
                        <option value="">Select Preset</option>
                        {% for preset in presets %}
                        <option value="{{ preset['command'] }}">{{ preset['name'] }}</option>
                        {% endfor %}
                    </select>
                </div>
                <input type="submit" value="Send Command">
            </form>

            <h2>Add Server</h2>
            <form method="post">
                <input type="hidden" name="add_server">
                <div class="form-group">
                    <label for="new_host">Host:</label>
                    <input type="text" id="new_host" name="new_host" placeholder="Server IP">
                </div>
                <div class="form-group">
                    <label for="new_port">Port:</label>
                    <input type="number" id="new_port" name="new_port" placeholder="Port">
                </div>
                <input type="submit" value="Add Server">
            </form>

            <h2>Add Preset</h2>
            <form method="post">
                <input type="hidden" name="add_preset">
                <div class="form-group">
                    <label for="preset_name">Preset Name:</label>
                    <input type="text" id="preset_name" name="preset_name" placeholder="Name">
                </div>
                <div class="form-group">
                    <label for="preset_command">Preset Command:</label>
                    <input type="text" id="preset_command" name="preset_command" placeholder="e.g., 0:45,90|1:30,60">
                </div>
                <input type="submit" value="Add Preset">
            </form>

            {% if message %}
                <p><strong>{{ message }}</strong></p>
            {% endif %}
        </div>
    </body>
</html>
''', servers=servers, presets=presets, message=message)

def send_command(host, port, command):
    """Send a command to the server and return the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(command.encode())
        response = s.recv(1024)
        return response.decode()

if __name__ == '__main__':
    app.run(debug=True)