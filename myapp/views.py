from myapp import app
#from flask import render_template, jsonify, Flask, request  # 追加jsonify
from flask import render_template, request, session  # sessionをインポート
import json
import random
from datetime import datetime # datetimeをインポート
from .main_handler  import Main_Handler
# ユーザのアクセス時には、start_sign をTrueにしておく
#import data_list #このファイルを直接実行する場合に使う
from . import  data_list  #他のプログラムから起動する場合


user_data = {'page_num':0,'user_name':'',
             'lang':'English'}
@app.route('/')
def index():    
    # sessionにデータを保存（ユーザーごとの専用の箱に入る）
    session['user_data'] =\
        data_list.default_value_dic   
    #user_data = data_list.default_value_dic
    data = get_all_view_data(session['user_data'])
    # 呼び出し側
    return render_template('myapp/index.html', **data)
    
@app.route('/submit_data', methods=['POST'])
def submit_data():    
    # sessionからその人のデータを取り出す
    user_data = session.get('user_data')
    if user_data['user_name'] != '':
        user_data['page_num'] += 1
    # index.htmlのセレクトタグ及びinput_areaからのデータを受け取る
    user_data['input_area_data'] = request.form['input_area']
    user_data['select_area_data'] = request.form['select_area']
    #上記データをmain_handlerに処理してもらい、user_dataを更新する
    handler = Main_Handler()
    user_data = handler.main(user_data)  
    # 不要になったデータuser_data['error']等は削除する 
    dl = data_list.deletable_data_list
    for key in dl:
        if key in user_data:
            # この場合は空文字にしておく
            user_data[key] = ''
            #del user_data[key]
           
        
    
    # 更新したデータをsessionに戻して保存
    session['user_data'] = user_data
    # 必要な６つのデータをindex.htmlに返す
    # user_data['footer_area_data'] = 'これはおもしろい'
    # 呼び出し側
    data = get_all_view_data(user_data)
    # 呼び出し側
    return render_template('myapp/index.html', **data)
def get_all_view_data(user_data):
    #初めてアクセスした時点とそれ以降で、render_template
    #の内容を変える。
    if user_data['page_num'] == 0:
        dv = data_list.default_value_dic
        for key, value in dv.items():
            user_data[key]= value
    #言語に応じた、セレクトタグの項目のリストとエラーメッセージの辞書
    #をuser_dataに収容する
    if user_data['lang'] == 'E':
       user_data['op_list'] = data_list.option_list_E
       user_data['error_message_dic'] = data_list.error_message_dic_E
    else: 
        user_data['op_list'] = data_list.option_list_J
        user_data['error_message_dic'] = data_list.error_message_dic_J
    data = {
        'title_area_data': user_data['title_area_data'],
        'input_area_data': user_data['input_area_data'],
        'output_area_data' : user_data['output_area_data'],
        'select_area_data' : user_data['select_area_data'],
        'announce_area_data' : user_data['announce_area_data'],
        'footer_area_data': user_data['footer_area_data'],
        'op_list': user_data['op_list'],
        'current_select': user_data.get('select_area_data', '') # 現在の選択値を渡す
         }    
    return data
    
     
    