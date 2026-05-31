from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html', entries=entries)