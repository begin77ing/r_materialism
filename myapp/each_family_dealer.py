import os
import sys
import re
#from . import data_list
import data_list
import database #このファイルを直接実行する場合に使う
#from . import  database #他のプログラム　views.py等から起動する場合



#optionタグの選択が何番目であるかによって、main}_handlerから呼び出される
# ファミリークラスが変わる。呼び出されたクラスは、リクエストに応じて、
# メンバー毎の処理文が表示又は実行されるように準備し、それをデータベースとの
# やり取りやエラーの有無に応じて、ud['error']、
# ud['display_data']又は、ud['sql_statement']として、返す。

class Whole_Family():
    def __init__(self):
        pass
    '''ud['family_number']の第一要素が1の
    場合はトップページの表示、2はそれ以外の表示、3は
    権限がある場合の新規の書き込み、4は権限がある
    場合の削除を含むデータの変更、6はakiraによる
    トップページの作成、7はデータの変更(新規の書き
    込み、削除を含む変更）
    )'''
    def common_treatment(self,ud):   
        print('')     
        ud['command_list'] = data_list.command_list
        ud['handler'] = database.DB_Handler()
        ud = preparation(ud)    
        if ud['error'] != '':
            return ud
        if len(ud['com'] ) != 0:                
            '''sql ステートメントを作る為のデータのペア
            を作る'''  
            ud = get_data_pair(ud) 
            if ud['error'] != '':
                return ud            
            ud = make_sql_statement(ud) 
            if ud['error'] != '':
                return ud
        else:
            '''作成が終われば、ud['family_name']の
            トップページを表示する。'''
            #ud = show_top_page(ud)
        return ud

def preparation(ud,index=0):  
    print(ud['com'])   
    match ud['select_area_num']:
        case 1 | 11:
            handler = Family_1(ud)
            handler.dealer_1(ud)
        case 2 | 12:
            handler = Family_2(ud)
            handler.dealer_2(ud)
        case 3 | 13:
            handler = Family_3()
            handler.dealer_3(ud)
        case 4 | 14:
            handler = Family_4()
            handler.dealer_4(ud)
        case 5 | 15:
            handler = Family_5()
            handler.dealer_5(ud)
        case 6 | 16:
            handler = Family_6()
            handler.dealer_6(ud)
        case 7 | 17:
            handler = Family_7()
            handler.dealer_7(ud)
        case 8 | 18:
            handler = Family_8()
            handler.dealer_8(ud)
        case 9 | 19:
            handler = Family_9()
            handler.dealer_9(ud)
        case _:
                pass  
    return ud  
def check_data_existence(ud):      
    if ud['stage'] == 'start': 
    #データの存否を確認する。
        ud['data_exist'] = False
        ud['tb_name']  = 'option_info'  
        ud['command']  = 'fetch_one'
        ud['sql_statement'] =(
        f"  WHERE family_name = "
        f"{ud['family_name']} AND "
        f"family_number = {ud['family_number']}"
            )
        print(ud['sql_statement'])
        ud = ud['handler']\
            .data_manager(ud)  
        if ud['error'] != '':
                return ud
        if  ud['data_exist']:
            ud['data_exist']= True
        # family_nameとfamily_numberの両方が一致する
        # ものがある場合は、続行の有無の確認を取る。
        if ud['data_exist'] == 'yes':
            ud['stage'] =(f'confirmation'
               f' requested')
            ud['error'] = 'nothing'
        return ud
def show_top_page(ud):
    print('deal_top')
    if ud['command_option'] == 11 or 12 :
        #この場合、書き込みを実行するが、これは
        # ud['i_name'] == 'akira'
        # の場合にのみ許される。
        if ud['i_name'] != 'akira':
            ud['error'] = \
            ud['error_message_list'][6]   
            return ud        
        # ud['command_option'] == 1 or 
        # 2の場合はこの時点で、書き込み内容を
        # 打ち出して、確認を求めるので、データ
        # ベースへの書き込みは実行しないで、只
        # 最終的なsqlステートメントだけを得る。
        ud ['stage'] = 'unconfirmed'   
        ud['tb_name'] = 'option_info'  
          
        ud = \
           do_database_request(ud)
        # 本来、akiraにこのデータを書き込んで良い
        # かとoutput_area に表示し、確認を求める
        # が、当面は此処に'command_check' ==
        # 'select_all_data_query'データを表示
        # するだけにする。
        
        print('このデータをdbに書き込んで良いですか？')
        # 止める。
        #データベースへ要請のあった条件に合う
        # de
        # するが、その前にakiraに確認する。従って、
        # ud['stage']は
        # 
    elif ud['command_option'] == 2:
        
        # 削除はしないで、追加書き込みを実行する
        pass
    else:
        # データを削除する
        pass
    return ud
def deal_top_page(ud):    
    try:            
        if ud['kind_of_request'] == 1 :
            ud = show_toppage(ud) 
        elif ud['kind_of_request'] == 2:            
            ud = make_toppage(ud) 
                         
        if ud['error'] != '':
            return ud
        '''続いて、表示コマンドの作成を実行する。
        family_chord別(±10は同じ扱いなので、
        全部で9個）に、トップページのoutput_areaで表示
        されるコマンドテンプレートを、必要となる時期に
        応じて作成する。'''
        
        '''続いて、family別に、表示コマンドで使われる
        データをtitleから順に整理し、display_dataに登録
        して行く。'''
        
        '''登録されたデータの内、family_chordが11で始まる
        ものは全て初期ページに表示される事に注意する。その結果、
        output_areaやfooter_areaには沢山のデータが表示されて
        見にくくなる可能性があるが、ユーザが求めれば、その後の
        コマンド入力で、一部に絞って見る事も可能なので、問題は
        ないだろう。'''
        
        handler = database.DB_handler()
        handler.data_manager
        print('')
    
    
    except Exception as e: 
        ud['error'] = e        
    finally:
        return ud
    return
def make_toppage(ud):
    if ud['i_name'] != 'akira':
        ud['error'] = ud['error_message'][6]    
        return ud    
    '''以下、データベースとどうやり取りするかを
    決めて行く。具体的には、どういう順番でどのテーブルに
    どのコマンド(command)を発し、それに与えるパラメータ
    (sql)は何か？、あるいはそれら全体（sql)は何か？の4点
    だが、先ず第一に、データの唯一性を確認する。'''
    ud['tb_name'] = 'option_info'
    ud['command'] = 'confirm'
    ud['params'] = (ud['family_chord'], ud['family_number'])
    ud['sql_statement'] = " WHERE family_chord = %s AND family_number = %s"
    ud = ud['handler'].data_manager(ud)
    if ud['result'] != False:#データが存在=>エラー
        ud['error']= ud['error_message'][8]
        return
    print()
    '''未登録を確認したので、option_infoにデータを
    追加する。index.html内の6つの表示箇所の内、
    select_area_dataはmain_handlerで定義するので、
    不要、title_area_dataは:fnu:由来のデータを使い、
    それ以外は、ud['com']で定義されている値を使う。 '''  
    data = [
    ('Shota', 'Sato', '2001-03-12', 'M'),
    ('Hiroki', 'Takagi', '2000-04-05', 'M'),
    ('Yuka', 'Kimura', '2001-03-27', 'F')]
    for i in range(1,7):  
        #title_area_data を得る為に逆引き辞書を用意する
        rev_dict = data_list.select_area_num_list
        title_dict = {v: k for k, v in rev_dict.items()}     
        title =  title_dict[ud['family_chord']]
        '''select_area_dataの値を得るにはud['ol']等を使う
        '''
        
        
        sql = '''INSERT INTO option_info (family_chord,
        family_number,commmand_string,sentence,explanation)   
         VALUES (%s, %s, %s, %s ,%s)'''
        
    
            
    
def show_toppage(ud):
    ud['tb_name']='option_info'
    ud['command'] = 'fetch_one'
    ud['sql_statement'] = (
    " WHERE family_number = "
    f"{ud['family_number']}"
)
    ud = ud['handler'].data_manager(ud)
    if 'db_result' in ud and ud['db_result']:
        ud['error'] = ud['error_message_list'][8]
        return ud
    '''
    ud['command'] = 'insert_record'
    #ud['com']が持つデータを元にしてud['sql_statement']を作る
    ud= make_sql_statement_from_com(ud)
    '''
def deal_another_page(ud):
    print('deal_another')
    return ud
# databaseから、データを取得する窓口。
def do_database_request(ud):
    #databaseに対するリクエストを作成する。
    pass
def make_sql_statement_from_com(ud) : 
    #各topページで表示されるコマンド文字列を作成する
    # コマンドの中の不要な部分を削除  
    ud['com']['command_string'] = \
        ud['com']['command_string'].replace(":com-",":com")
    ud['com']['command_string'] = \
        ud['com']['command_string'].replace(":oth-",":oth")
    ud['sql_statement'] = (
    f"INSERT INTO {ud['tb_name']} "
    "(family_chord, family_number, command_string, explanation) "
    "VALUES (%s, %s, %s, %s)"
    )
    ud['sql_data'] = (ud['com']['family_chord'],ud['com']['family_number'],
                     ud['com']['command_string'],ud['com']['explanation']) 
    print('ok')
    ud = ud['handler'].data_manager(ud)
    pass

class Family_1(Whole_Family):
    def dealer_1(self,ud,index = 0):
        print('f1')
        if index == 'make_top':            
            return ud
class Family_2(Whole_Family):
    def dealer_2(self,ud):
        return ud
        pass
class Family_3(Whole_Family):
    def dealer_3(self,ud):
        return ud
        pass
class Family_4(Whole_Family):
    def dealer_4(self,ud):
        return ud
        pass    
class Family_5(Whole_Family):
    def dealer_5(self,ud):
        return ud
        pass
class Family_6(Whole_Family):
    def dealer_6(self,ud):        
        return ud
        pass       
class Family_7(Whole_Family):
    def dealer_7(self,ud):
        return ud
        pass
class Family_8(Whole_Family):
    def dealer_8(self,ud):
        return ud
        pass   

class Family_9(Whole_Family):
    def dealer_9(self,ud):  
        print('')
        if ud['i_name'] != 'akira' :
            ud['error'] = \
             ud['error_message_list'][6]   
            return ud 
        try:
            ud = deal_top_page(ud)
            if ud['error'] != '':
                return ud
            pass
            
        except  Exception as e:
            pass
            
        finally:
            return ud
        '''先ず、処理がトップページの作成かどうかを区別し、
        続いて、処理の対象familyと所属num1によって
        振り分ける
        '''                  
        print('get here 9')  
           
        '''family_chordは19、
        family_numberは12、command_stringは
        ”:lang:<ja> :fnu:<a0102014011>:com: :oth:<>で、
        explanationは、”以下は、各ファミリーグループの
        トップページを作成するコマンドの作成用テンプレート。
        ＊注意 :fnu:の<>の中には、aの代わりに処理対象の
        ファミリーグループのud['select_area_num']を入れる”'''       
        return ud

'''ud['command_option']とud['target']のデータと元
にして、そのペア（２要素の辞書を要素とするリスト
を作る）'''
def get_data_pair(ud):
    try:
        leng = len(ud['command_option_list'])
        command_list = ['']     
        tb_name_list= ['']
        for i in range(leng):
            print(i)
            command_list.append(\
            ud['command_list']\
            [ud['command_option_list'][i]] )
            tb_name_list.append(\
            ud['table_list'][ud['table_num_list'][i]])  
        ud['db_data_pair'] = [{}]       
        for i in range(leng):
            ud['db_data_pair'].append({
            'command':command_list[i+1],
            'tb_name':tb_name_list[i+1]})
            print(i)
        print('owari')
        del_key = ['table_num_list','command_option_list',
               'table_list','command_list' ]
        # 不要なキーを直接削除する
        del_key = ['table_num_list', 'command_option_list', 'table_list', 'command_list']
        for key in del_key:
            ud.pop(key, None)  # キーが存在しなくてもエラーにならない安全な削除
        print(ud)
    except Exception as e:
        print(e)
    finally:
        return ud           
           
           
def make_sql_statement(ud):
    print('make_sql_statement')
    ''' ud['family_number'] = int(fnu[0])#  fnu[1:]
        ud['command_option'] = int(fnu[1])#  
        ud['table_num'] = int(fnu[2])# '''
    ud['values_code_list'] = []
    # この関数内での最大繰り返し処理回数を決める
    com_len = len(ud['command_option_list'])
    for i in range(com_len):        
        dv = data_list.values_code_list
    for i in dt:        
        dt = data_list.table_list[ud['table_num_list']]
        ud['table_value_list'].append(dv[dt[i]])
    
    return ud
    pass
def make_display_data(ud):
    print('get here')
    return ud
    pass

