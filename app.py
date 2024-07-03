from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('calories.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            calories_consumed INTEGER,
            calories_burned INTEGER,    
            weight_change REAL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        calories_consumed = int(request.form['caloriesConsumed'])
        calories_burned = int(request.form['caloriesBurned'])
        net_calories = calories_consumed - calories_burned
        weight_change_in_pounds = round(net_calories / 3500, 2)
        print("Route /calculate has been called")

        return render_template('results.html', 
                               date=datetime.now().strftime("%A %B %d, %Y - %I:%M %p"),
                               calories_consumed=calories_consumed,
                               calories_burned=calories_burned,
                               weight_change=weight_change_in_pounds) 
    except ValueError:
        return "Invalid input. Please enter valid numbers.", 400

@app.route('/save', methods=['POST'])
def save():
    print("Route /save has been called")
    date = request.form['date']
    calories_consumed = request.form['caloriesConsumed']
    calories_burned = request.form['caloriesBurned']
    weight_change = request.form['weightChange']

    print(f"Data received: {date}, {calories_consumed}, {calories_burned}, {weight_change}")
    
    conn = sqlite3.connect('calories.db')
    c = conn.cursor()
    c.execute('INSERT INTO entries (date, calories_consumed, calories_burned, weight_change) VALUES (?, ?, ?, ?)',
              (date, calories_consumed, calories_burned, weight_change))
    conn.commit()
    conn.close()
    
    return redirect(url_for('entries'))  # Redirect to the entries page

@app.route('/entries')
def entries():
    conn = sqlite3.connect('calories.db')
    c = conn.cursor()
    c.execute('SELECT id, date, calories_consumed, calories_burned, weight_change FROM entries')
    entries = c.fetchall()
    conn.close()
    
    # Calculate the total weight change
    total_weight_change = sum(entry[4] for entry in entries)
    total_weight_change = round(total_weight_change, 2)
    weight_change_type = "lost" if total_weight_change < 0 else "gained"
    
    print(f"Total Weight Change: {total_weight_change}")  # Debug print
    
    if not entries:
        print("No entries to display.")  # Debug print
    else:
        print(entries)  # Debug print
    
    return render_template('entries.html', entries=entries, total_weight_change=total_weight_change, weight_change_type=weight_change_type)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = sqlite3.connect('calories.db')
    c = conn.cursor()
    c.execute('DELETE FROM entries WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('entries'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
