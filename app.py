from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Реализуйте функции работы с JSON
def load_entries():
    if not os.path.exists('entries.json'):
        return []
    with open('entries.json', 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_entries(entries_list):
    with open('entries.json', 'w', encoding='utf-8') as f:
        json.dump(entries_list, f, ensure_ascii=False, indent=4)

entries = load_entries()


# Реализуйте маршрут главной страницы
@app.route('/')
def index():
    return render_template('index.html', entries=entries)
 

# Реализуйте маршрут просмотра записи
@app.route('/entry/<int:entry_id>')
def detail_entry(entry_id):
    entry = next((e for e in entries if e['id'] == entry_id), None)
    if entry:
        return render_template('detail.html', entry=entry)
    return "Запись не найдена", 404


# Реализуйте маршрут добавления записи
@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        new_id = max([e['id'] for e in entries], default=0) + 1
        
        new_entry = {
            "id": new_id,
            "title": title,
            "content": content,
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        entries.append(new_entry)
        save_entries(entries)
        return redirect(url_for('index'))
        
    return render_template('add.html')


# Реализуйте маршрут редактирования записи
@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    entry = next((e for e in entries if e['id'] == entry_id), None)
    if not entry:
        return "Запись не найдена", 404
        
    if request.method == 'POST':
        entry['title'] = request.form.get('title')
        entry['content'] = request.form.get('content')
        save_entries(entries)
        return redirect(url_for('index'))
        
    return render_template('edit.html', entry=entry)


# Реализуйте маршрут удаления записи
@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    global entries
    entries = [e for e in entries if e['id'] != entry_id]
    save_entries(entries)
    return redirect(url_for('index'))


# Реализуйте маршрут поиска
@app.route('/search')
def search():
    q = request.args.get('q', '').lower()
    filtered = [e for e in entries if q in e['title'].lower()]
    return render_template('index.html', entries=filtered)


# Реализуйте маршрут фильтра по дате
@app.route('/filter/week')
def filter_week():
    now = datetime.now()
    seven_days_ago = now - timedelta(days=7)
    filtered = []
    for e in entries:
        try:
            entry_date = datetime.strptime(e['date'], '%Y-%m-%d %H:%M:%S')
            if entry_date >= seven_days_ago:
                filtered.append(e)
        except ValueError:
            continue
    return render_template('index.html', entries=filtered)


#Добавьте запуск приложения
if __name__ == '__main__':
    app.run(debug=True)