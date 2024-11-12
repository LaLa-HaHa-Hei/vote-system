from flask import Flask, render_template, send_from_directory, jsonify, request, g
import os
import sqlite3
import json

# 初始化数据库
conn = sqlite3.connect('vote-results.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS vote_results
             (id TEXT PRIMARY KEY, votes INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS fingerprints
             (fingerprint TEXT PRIMARY KEY)''')
conn.commit()
conn.close()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('vote-results.db')
        db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    db = get_db()
    cursor = db.execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    return (rv[0] if rv else None) if one else rv

app = Flask(
    __name__,
    template_folder='../frontend/dist',
    static_folder='../frontend/dist'
)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/get-vote-items')
def get_vote_items():
    with open('vote-items.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return jsonify(data)

@app.route('/api/submit-vote-result' , methods=['POST'])
def submit_vote_result():
    data = request.get_json()
    print(data)
    if has_voted(data['md5Fingerprint']):
        print('重复投票')
        return jsonify({'success': False, 'error': '重复投票'})
    else:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO fingerprints (fingerprint) VALUES (?)', (data['md5Fingerprint'],))
        for id, value in data['selectedItems'].items():
            if value:
                cursor.execute('''
                INSERT INTO vote_results (id, votes)
                VALUES (?, 1)
                ON CONFLICT(id) DO UPDATE SET votes = votes + 1
            ''', (id,))
        db.commit()
        cursor.close()
        print('投票成功')
        return jsonify({'success': True})

@app.route('/api/get-vote-results')
def get_vote_results():
    results = query_db('SELECT id, votes FROM vote_results')
    vote_results = {'voteResults': [{'id': row['id'], 'votes': row['votes']} for row in results]}
    return jsonify(vote_results)

@app.route('/api/does-have-voted', methods=['POST'])
def does_have_voted():
    data = request.get_json()
    print(data)
    fingerprint = data['md5Fingerprint']
    return jsonify({'hasVoted': has_voted(fingerprint)})

@app.route('/<path:path>')
def catch_all(path):
    # 如果请求的路径是静态文件，直接返回该文件
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    # 否则返回index.html，交给前端路由
    return render_template('index.html')


def has_voted(fingerprint):
    result = query_db('SELECT COUNT(*) FROM fingerprints WHERE fingerprint = ?', (fingerprint,), one=True)
    return result[0] > 0

if __name__ == '__main__':
    app.run(debug=True, port=8080)
