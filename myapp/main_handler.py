import os
import sys
import re
import database #このファイルを直接実行する場合に使う
#from . import  database #他のプログラム　views.py等から起動する場合
import data_list #このファイルを直接実行する場合に使う
#from . import  data_list #他のプログラム　views.py等から起動する場合
import each_family_dealer
#from . import  each_family_dealer #他のプログラム　views.py等から起動する場合
#input_area内の一桁目のfnu値に対応するデータを取得しやすいように、
#data_listから、リスト化されたデータを取得しておく
#table_list = data_list.table_list

#input_area内の2桁目のfnu値に対応するコマンド名を取得する
#command_list = data_list.command_list

class Main_Handler():
    def __init__(self):
        #user_data = {'page_num':0,'login':False}
        #self.main_handler(user_data)
        pass
    def main_handler(self,user_data): 
        # login していない場合は、初期ページを表示する
        if user_data['user_name'] == ''  :
            user_data = initial_page(user_data)
            print(user_data)        
        user_data['error'] = ''
        user_data['adm'] = False
        # 言語の変更があるか否かをチェック。グループに「ja」と「en」という名前を付与
        pattern = r':1:\s*lang\:2:(?:\s*(?P<ja>日本語)|\s*(?P<en>English))'
        text = user_data['input_area_data']
        #text_ja = ":1: lang:2:日本語"

        match = re.search(pattern, text)
        if match:
    # 名前で直接値を取得できる
            #print(match.group('ja'))  # 出力: 日本語
            #print(match.group('en'))  # 出力: None
            if match.group('ja'):
                user_data['lang'] = match.group('ja')
            elif match.group('en'):
                user_data['lang'] = match.group('en') 
    # マッチしたグループ名と値の辞書をまとめて取得することも可能
            #print(match.groupdict(),";",user_data['lang'])  # 出力: {'ja': '日本語', 'en': None}
            #print()   
        if user_data['lang'] =='日本語':
            user_data['error_message_list']=data_list.error_message_list_J
            user_data['option_dic'] = data_list.option_dic_J
        else: 
            user_data['error_message_list']=data_list.error_message_list_E 
            user_data['option_dic'] = data_list.option_dic_E         
        #input_area_dataの中身を調べ、然るべきkeyとその値を保存する
        user_data = input_area_analyser(user_data)
        print(user_data)
        if user_data['error'] != '':
            return user_data
        else:
            #input_areaの処理が終わったので、各familyグループ毎の処理に移る。
            handler =each_family_dealer.Whole_Family()
            
            user_data = handler.preparation(user_data)
        return user_data
        '''
        # errorがない場合、input_areaの資料を元にして、データベースから、必要な情報を得る。
        else:
            import db_handler
            handler = db_handler.DB_handler
            user_data = handler(user_data)
        # userに返すページの作成に入る
        # show_page()
        #---------
        return user_data
    # database.pyとのやり取りをして、ページの表示までの処理
    # を完了する
    '''
def initial_page(user_data):
    try:
        user_data['page_num'] = 0
        user_data['select_area_data'] = 'Home'
        user_data['input_area_data'] ='''
        :fnu:1001 <br>
        :com:<br> 
        :1:lang:2: English <br>
        :oth:   
        '''
        return user_data
    except Exception as e:
        pass
    
    return
def input_area_analyser(user_data):
    try:        
    # 先ず、input_areaを取り上げ、:com:の後ろに :2:（辞書型データの
    # keyとvalを仕分ける:記号の代替記号）があるかどうかをチェックする
    # これが無ければ、:fna:の後ろの値に応じた初期画面を表示する    
        content = user_data['input_area_data']   
        pattern = r'\s*:fnu:\s*(-?\d{,20})\s*' + \
          r':com:([\s\S]*?)' + \
          r':oth:([\s\S]*)'
        # input_areaのデータをuser_dataの中に納める        
        result =  matching_handler(content,pattern)
        # :com:の後ろに具体的なデータが在るとみられる場合
        # listの形で user_data['com']　に収納しておく
        #user_data['com'] = {k: v for k, v in pairs}
        com = []
        
        if result:
            fnu = result.group(1)
            oth = result.group(3).strip()   
                
            user_data = fnu_analyser(fnu,user_data)
            if  user_data['error'] != '' :
                return user_data
            user_data['com'] = result.group(2)
            if  not user_data['com'] or user_data['com'] != '':
                user_data = com_analyser(user_data)
        else:
            user_data['error'] = user_data['error_message_list'][5]        
        return user_data
    
    except Exception as e:
        user_data['error'] = user_data['error_message_list'][4]
        return user_data   

def fnu_analyser(fnu, user_data):  
    print(fnu)  
    if fnu == ''  :
        user_data['error'] = user_data['error_message_list[2]']
        return user_data  
    fnu = fnu.split('0')
    fnu = map(int, fnu)
    print(fnu)
    fnu = list(fnu)
    #fnu = list(map(int, fnu))
    print(len(fnu))
    user_data['adm'] = False
    if fnu[0] < 0 and (user_data['user_name'] != 'akira'):
        user_data['error'] = user_data['error_message_list[3]']
        return user_data
    else:
        fnu[0] = abs(fnu[0])
        # akiraによるアクセスの場合、この数字は二桁で、先頭はアドミンである事を
        # 表し、二番目の数字は、ターゲットである処理対象のグループ番号を表す。
        # 従って、一番目の数字を除いて、本来の目的を表す数字に替える必要がある。
        if fnu[0] < 90 or fnu[0] > 99:
            user_data['error'] = user_data['error_message_list[2]']
            return user_data
        fnu[0] = fnu[0] - 90
        print(fnu[0])
        user_data['adm'] = True
        # セレクトタグでの選択とfnu[0]を比較し、違っていれば、エラーを返す
        sad = user_data['select_area_data']
        od = user_data['option_dic']
        print('digit=',od[sad])
        print('digit=',user_data['option_dic'][user_data['select_area_data']])
        if fnu[0] != user_data['option_dic']\
            [user_data['select_area_data']]:
            user_data['error'] = user_data['error_message_list[2]']
            return user_data
        user_data['family_number'] = fnu[1:]
        user_data['select_area_num'] = fnu[0]
        return user_data
def com_analyser(user_data):    
    pairs = re.findall(r':1:\s*(\S+)\s*:2:\s*(\S+)'\
    , user_data['com'])
    print(pairs)
    com =  {k: v for k, v in pairs if k != 'lang'}            
            #com =  {k: v for k, v in pairs}
            #user_data['com'] = [{k: v} for k, v in pairs]
            #langの処理は不要なので除いておく            
            #print('com = ',com)
    com_dic = {k: v for k, v in pairs if k != 'lang'}
    com_len = len(com_dic)
    #　先ず、key毎のvalの値の長さとその一致性を調べ、valを
    # リスト化した辞書にかえる。
    k = 0
    val_len = 0
    i_val_list_len = 0
    for i in com_dic.keys():     
        i_val_list = com_dic[i].split(';;')
        com_dic[i] = i_val_list
        i_val_list_len = len(i_val_list)
        if k == 0:
            val_len = i_val_list_len
        if not (val_len == i_val_list_len):
            user_data['error']=\
            user_data['error_message_list'][7]
            return user_data
        k += 1
    # 以上でvalの長さの一致性を確認した。そこで、
    # 長さがval_lenのリストを作り、辞書をはめ込む
    com_dic_list = [{} for _ in range(val_len)]
    com_dic2 ={}
    for i in com_dic.keys():  
        val_list = com_dic[i]
        for j in range(len(val_list)):
            com_dic_list[j][i]  = val_list.pop(0) 
            print('j=',j,':',com_dic_list[j][i])
            print()    
    user_data['com'] = com_dic_list   
    print('user_data = ',user_data)                          
    return user_data
def show_option_menu(fna):# この引数で、family_name (fna)が分かるので
    # selectタグで選択されたオプションのファミリーグループに帰属するメニューを表示する。
    pass

        
def matching_handler(oontent,pattern):
    repatter = re.compile(pattern)
    result = repatter.match(oontent)
    return result
   

if __name__ == "__main__":
    
    handler = Main_Handler()
    forJlang = ':fnu:1:com::oth:'
    user_data = {'title_area_data': 
    '管理者用ページ'
    ,'select_area_data': '管理者用' 
    ,'lang':'日本語'
    ,'output_area_data' : ''  
    ,'announce_area_data':''
    ,'footer_area_data':''
    ,'user_name' : 'akira'
    }
    '''以下は、akiraがadmin（初めの9)として
    ホーム(二番目の1)を
    表示させる(1)
    場合のコマンド'''
    user_data['select_area_data'] = 'ホーム'
    user_data['input_area_data'] ='''
    :fnu:-910201 :com::1:destination:2:
        output_area;;output_area 
    :1:permission:2:all;;akira:oth:
    '''
    
    '''
     <br>
    '''
    user_data = handler.main_handler(user_data)
    #handler.__init__()
    #print(user_data)
    #print('end')    