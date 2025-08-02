from flask import render_template, request, redirect, url_for, flash
from . import app
import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data.json')

def load_entries():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_entries(entries):
    with open(DATA_FILE, 'w') as f:
        json.dump(entries, f, indent=2)

def get_monthly_summary(entries, year, month):
    earnings = 0
    costs = 0
    for entry in entries:
        entry_date = datetime.strptime(entry['date'], "%Y-%m-%d")
        if entry_date.year == year and entry_date.month == month:
            amount = float(entry['amount'])
            if amount >= 0:
                earnings += amount
            else:
                costs += amount
    total = earnings + costs
    month_name = datetime(year, month, 1).strftime("%B %Y")
    return {
        'earnings': earnings,
        'costs': costs,
        'total': total,
        'month': month_name
    }

def filter_month(entries, year, month):
    filtered = []
    for entry in entries:
        entry_date = datetime.strptime(entry['date'], "%Y-%m-%d")
        if entry_date.year == year and entry_date.month == month:
            filtered.append(entry)
    return filtered

def get_yearly_summary(entries, year):
    earnings = 0
    costs = 0
    for entry in entries:
        entry_date = datetime.strptime(entry['date'], "%Y-%m-%d")
        if entry_date.year == year:
            amount = float(entry['amount'])
            if amount >= 0:
                earnings += amount
            else:
                costs += amount
    total = earnings + costs
    year_name = str(year)
    return {
        'earnings': earnings,
        'costs': costs,
        'total': total,
        'month': year_name  # reuse 'month' key for display
    }

def filter_year(entries, year):
    filtered = []
    for entry in entries:
        entry_date = datetime.strptime(entry['date'], "%Y-%m-%d")
        if entry_date.year == year:
            filtered.append(entry)
    return filtered

@app.route('/', methods=['GET'])
def index():
    entries = load_entries()
    now = datetime.now()
    year = int(request.args.get('year', now.year))
    month = int(request.args.get('month', now.month))
    view = request.args.get('view', 'month')
    if view == 'year':
        summary = get_yearly_summary(entries, year)
        filtered_entries = filter_year(entries, year)
    else:
        summary = get_monthly_summary(entries, year, month)
        filtered_entries = filter_month(entries, year, month)
    # Sort entries by date descending (most recent first)
    filtered_entries.sort(key=lambda e: e['date'], reverse=True)
    return render_template('index.html', entries=filtered_entries, summary=summary, year=year, month=month, view=view)

@app.route('/add', methods=['POST'])
def add_entry():
    dates = request.form.getlist('date[]')
    amounts = request.form.getlist('amount[]')
    comments = request.form.getlist('comments[]')
    entries = load_entries()
    for date, amount, comment in zip(dates, amounts, comments):
        new_entry = {
            'date': date,
            'amount': float(amount),
            'comments': comment
        }
        entries.append(new_entry)
    save_entries(entries)
    return redirect(url_for('index'))

@app.route('/edit/<int:idx>', methods=['GET', 'POST'])
def edit_entry(idx):
    entries = load_entries()
    if idx < 0 or idx >= len(entries):
        flash("Entry not found.")
        return redirect(url_for('index'))
    entry = entries[idx]
    if request.method == 'POST':
        entry['date'] = request.form['date']
        entry['amount'] = float(request.form['amount'])
        entry['comments'] = request.form['comments']
        save_entries(entries)
        return redirect(url_for('index'))
    return render_template('edit.html', entry=entry, idx=idx)

@app.route('/delete/<int:idx>', methods=['POST'])
def delete_entry(idx):
    entries = load_entries()
    if 0 <= idx < len(entries):
        entries.pop(idx)
        save_entries(entries)
    return redirect(url_for('index'))