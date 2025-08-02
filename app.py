from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_entries():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_entries(entries):
    with open(DATA_FILE, 'w') as f:
        json.dump(entries, f, indent=2)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        entry = {
            'date': request.form['date'],
            'amount': float(request.form['amount']),
            'comment': request.form['comment']
        }
        entries = load_entries()
        entries.append(entry)
        save_entries(entries)
        return redirect(url_for('index'))
    entries = load_entries()
    return render_template('index.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)