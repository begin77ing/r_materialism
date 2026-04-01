from myapp import app
from flask import render_template, jsonify, Flask, request  # 追加jsonify
import json
import random
from datetime import datetime # datetimeをインポート

@app.route('/')
def index():
   return render_template('./myapp/index.html')
@app.route('/api', methods=['POST'])
@app.route('/api/data', methods=['GET','POST'])
def get_data():
    #output_data = request.form['input_area']
    random_value = random.randint(1, 100)
    server_data = {'value': random_value, 'status': 'OK', 'timestamp': datetime.now().isoformat()}
    #server_data = {'output_data': output_data,'value': random_value, 'status': 'OK', 'timestamp': datetime.now().isoformat()}
    print(f"APIリクエスト受信: {server_data}")
    return jsonify(server_data) 
 
@app.route('/receive_data', methods=['POST'])
def receive_data():
    data_from_js = request.json
    print('Data from JavaScript:', data_from_js)
    return jsonify({'message': 'Data received by Python'})

@app.route('/sampleform-post', methods=['POST'])
def sample_form_temp():
    print('POSTデータ受け取ったので処理します')
    req1 = request.form['data1']

    return f'POST受け取ったよ: {req1}'
@app.route('/api/data2', methods=['POST'])
def receive_data2():
    data = request.get_json()
    if data:
        # データの処理
        received_data = data.get('message')
        result = f"Flask received: {received_data}"
        # 処理結果をJSON形式で返す
        return jsonify({'result': result})
    else:
        return jsonify({'error': 'No data received'}), 400

@app.route('/submit_data', methods=['POST'])
def submit_data():
    data = request.form['my_data']
    print(f"受け取ったデータ: {data}")
    return "データを受信しました！"   