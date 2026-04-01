from myapp import app
from flask import render_template, jsonify, Flask, request  # 追加jsonify
import json
import random
from datetime import datetime # datetimeをインポート
from .main_handler  import Main_Handler
user_data = {}
@app.route('/')
def index():
    global user_data
    user_data = {'title_area_data': 'Relational materialism/繋がりの唯物観'
    ,'select_area_data':['Home','Login','R_materialism','Blog','Opinion Plaza','Notification','Sell&Support','Contact','ForAdmin']
    ,'input_area_data' : '\n \n If you want to see another content of this site,please login.\n 1: Select Login in the left box \n 2: Push Go button \n 3: Guide will show up in the right box '
    ,'output_area_data' : '日本語を選択する方は、左横の入力用テキスト欄の先頭に、ーー日本語を選択ーー（前後のハイフンを含む文字列）をコピペして、Goボタンを押して下さい.'
    ,'footer_area_data':''
    ,'user_name' : 'akira' #将来Noneに置き換える
    ,'lang':'English'
    }
    
     # startは初期画面に対応'
    handler = Main_Handler()
    user_data = handler.main(user_data)
    return render_template('./myapp/index.html',
    title_area_data = user_data['title_area_data'],
    select_area_data = user_data['select_area_data'],
    input_area_data = user_data['input_area_data'],
    output_area_data = user_data['output_area_data'],
    footer_arera_data = user_data['footer_area_data'])
    
@app.route('/submit_data', methods=['POST'])
def submit_data():
    global user_data
    # index.htmlのセレクトタグ及びinput_areaからのデータを受け取る
    user_data['input_area_data'] = request.form.get('input_area')
    user_data['output_area_data'] = request.form.get('output_area')
    user_data['select_area_data'] = request.form['select_area']
    user_data['footer_area_data'] = request.form.get('footer_area')
    #上記データをmain_handlerに処理してもらい、user_dataを更新する
    handler = Main_Handler()
    user_data = handler.main(user_data)  
    #user_data['lang'] ='Japanese'
    # 必要な４つのデータをindex.htmlに返すが、select_area_dataは元に戻しておく
    user_data['lang']='Japanese'
    if  user_data['lang']=='English'  :
        user_data['select_area_data'] = ['Home','Login','R_materialism','Blog','Opinion Plaza','Notification','Sell&Support','Contact','ForAdmin']
    else:
        user_data['select_area_data'] = ['ホーム','ログイン','繋がりの唯物観','ブログ','意見の広場','お知らせ','販売＆サポート','コンタクト','管理者用']
    return render_template(
        'myapp/index.html',
        input_area_data = user_data['input_area_data'],
        output_area_data = user_data['output_area_data'],
        select_area_data = user_data['select_area_data'],
        footer_area_data = user_data['footer_area_data']
    )
'''
class Main_Handler():
    def __init__(self):    
        pass
    def main(self,user_data_): 
        global user_data 
        user_data = process_handler(user_data_)
            #　ユーザがGoボタンを押した場合で、select_areaとinput_area
            #　の情報を基にして、self.user_data
            
        return user_data
    # database.pyとのやり取りをして、ページの表示までの処理
    # を完了する
def process_handler(user_data_):   
    global user_data
    user_data = user_data_
    if not user_data['user_name']=='':        
            #　user_nameが''の場合は、英語又は日本語の初期画面を表示するだけ
            # それ以外の場合、 user_data['select_area_data']の値と、
            # user_data['input__area_data']を参考にして、処理内容を
            # 決める。
        pass
        
    return user_data
'''
'''
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
        result = f"Fla sk received: {received_data}"
        # 処理結果をJSON形式で返す
        return jsonify({'result': result})
    else:
        return jsonify({'error': 'No data received'}), 400
'''
'''
@app.route('/receive_json', methods=['POST'])
def receive_json():
    data = request.get_json()
    message = data.get('message')
    print(f"受け取ったJSONメッセージ: {message}")
    return j
    
    
    
    
    
    
    sonify({"status": "success", "received_message": message})
'''