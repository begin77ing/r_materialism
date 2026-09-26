
#from flask import render_template, jsonify, Flask, request  # 追加jsonify
from flask import render_template, request, session  # sessionをインポート
import json
import random
from datetime import datetime # datetimeをインポート
from .main_handler  import Main_Handler
# ユーザのアクセス時には、start_sign をTrueにしておく
#import data_list #このファイルを直接実行する場合に使う
from . import  data_list  #他のプログラムから起動する場合
from myapp import app

ud = {'page_num':0,'i_name':'',
             'lang':'English'}
@app.route('/')
def index():   
    # Accept-Language を活用  ユーザが使う言語をそのまま使う為の仕掛けのようだ
    lang = request.headers.get('Accept-Language', '')
    user_lang = 'ja' if 'ja' in lang.lower() else 'en'

    # 3. セッションの辞書を全体ごと新しく代入
    session['ud'] = {'session': 'start','lang': user_lang}
    handler = Main_Handler()
    ud = handler.main_handler(session['ud'])
    return render_template('myapp/index.html', **ud)
    #session['ud'] =\
        #data_list.default_value_dic   
    #ud = data_list.default_value_dic
    #data = get_all_view_data(session['ud'])
    # 呼び出し側
    #return render_template('myapp/index.html', **data)
    
@app.route('/submit_data', methods=['POST'])
def submit_data():    
    
    # 2回目以降（Submitボタン押下時）の処理
    # 1. 既存の session['ud'] を安全に取得
    ud_data = session.get('ud', {})
    if 'session' in ud :
        pass
    else:
    # index.htmlのセレクトタグ及びinput_areaからのデータを受け取る
    # 直下のinput_areaの初期値は後程書き込む予定
        ud['input_area_data'] = request.form.get('input_area','')
        ud['select_area_data'] = request.form.get('select_area','')
    #上記データをmain_handlerに処理してもらい、udを更新する
    handler = Main_Handler()
    ud = handler.main(ud) 
    session['ud'] = ud
    # 必要な６つのデータをindex.htmlに返す
    # ud['footer_area_data'] = 'これはおもしろい'
    # 呼び出し側
    #data = get_all_view_data(ud)
    data = ud
    return render_template('myapp/index.html', **data)

# テスト用にわざとエラー（0での割り算）を起こすページ
@app.route('/error-test')
def error_test():
    result = 1 / 0  # ここで必ずエラーが発生します
    return str(result)
'''
def get_all_view_data(ud):
    #初めてアクセスした時点とそれ以降で、render_template
    #の内容を変える。
    if ud['page_num'] == 0:
        dv = data_list.default_value_dic
        for key, value in dv.items():
            ud[key]= value
    #言語に応じた、セレクトタグの項目のリストとエラーメッセージの辞書
    #をudに収容する
    if ud['lang'] == 'E':
       ud['op_list'] = data_list.option_list_E
       ud['error_message_dic'] = data_list.error_message_dic_E
    else: 
        ud['op_list'] = data_list.option_list_J
        ud['error_message_dic'] = data_list.error_message_dic_J
    data = {
        'title_area_data': ud['title_area_data'],
        'input_area_data': ud['input_area_data'],
        'output_area_data' : ud['output_area_data'],
        'select_area_data' : ud['select_area_data'],
        'announce_area_data' : ud['announce_area_data'],
        'footer_area_data': ud['footer_area_data'],
        'op_list': ud['op_list'],
        'current_select': ud.get('select_area_data', '') # 現在の選択値を渡す
         }    
    return data
'''
     
    