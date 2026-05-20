from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)
DB_NAME = "database.db"
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/')
def index():
    conn = get_db_connection()
    players = conn.execute('''
        SELECT p.player_id, p.ign, p.role, t.team_name, t.team_id
        FROM Players p
        JOIN Teams t ON p.team_id = t.team_id
    ''').fetchall()
    teams = conn.execute('SELECT * FROM Teams').fetchall()
    conn.close()
    
    return render_template('index.html', players=players, teams=teams)
@app.route('/add', methods=['POST'])
def add_player():
    ign = request.form['ign']
    role = request.form['role']
    team_id = request.form['team_id']
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO Players (ign, role, team_id) VALUES (?, ?, ?)', 
                     (ign, role, team_id))
        conn.commit()
    except sqlite3.IntegrityError:
        pass 
    conn.close()
    return redirect(url_for('index'))
@app.route('/edit/<int:id>', methods=['POST'])
def edit_player(id):
    ign = request.form['ign']
    role = request.form['role']
    team_id = request.form['team_id']
    conn = get_db_connection()
    conn.execute('''
        UPDATE Players 
        SET ign = ?, role = ?, team_id = ? 
        WHERE player_id = ?
    ''', (ign, role, team_id, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
@app.route('/delete/<int:id>')
def delete_player(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Players WHERE player_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)