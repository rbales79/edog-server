import sqlite3

def create_db():
    conn = sqlite3.connect('servo_controller.db')
    c = conn.cursor()
    
    # Create table for server hosts
    c.execute('''CREATE TABLE IF NOT EXISTS server_hosts
                 (id INTEGER PRIMARY KEY, host TEXT, port INTEGER)''')
    
    # Create table for preset positions
    c.execute('''CREATE TABLE IF NOT EXISTS preset_positions
                 (id INTEGER PRIMARY KEY, name TEXT, command TEXT)''')
    
    # Save (commit) the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
    print("Database and tables created successfully.")
