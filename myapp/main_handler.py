import re
from .  import database
'''
user_data = {'title_area_data': 'Relational materialism/繋がりの唯物観'
    ,'select_area_data': 'Home'
    ,'input_area_data' : ''
    ,'output_area_data' : ''
    ,'footer_area_data':''
    ,'user_name' : None
    }
'''
class Main_Handler():
    def main(self,user_data): 
        user_data = process_handler(user_data) 
        return user_data
    # database.pyとのやり取りをして、ページの表示までの処理
    # を完了する
def process_handler(user_data): 
    print('this function must be revised in the future')
    return user_data
    '''
    if not user_data or (user_data and 'user_name' not in user_data):        
        #　user_nameがない場合は、ログインしていないので、
        # 英語又は日本語の初期画面を表示するだけ。以下の_string項目は他と性格が異なる事に注意する。
        user_data['family_number']=1
        # command項目に似た名前なので注意！！する事。初期画面では、コマンドの実行は、ユーザではなく、
        # プログラム自身が全てを取り仕切る。
        user_data['command_string']='' 
        user_data['command'] = 'fetch_one'
        user_data['tb_name'] = 'option_info'
        user_data['key_name'] = 'family_name'
        user_data['sql_statement'] = " SELECT * FROM" + user_data['tb_name'] + \
       "WHERE" +  user_data['key_name'] + " = %s"
        user_data['key_val'] = 'Home'
    '''
    # title_area_data,select_area_data.input_area_data,output_area_data,footerのそれぞれに
    # 表示するためのデータを取得するが、そのためには必要なデータ（sql_statement用）を作って
    #　渡さなければならない。
    

    user_data = make_sql_statement(user_data)
    data_handler =  database.DB_Handler()  
    user_data = data_handler.data_retriever(user_data)  
    return user_data    
def make_sql_statement(user_data):
    
    if user_data and 'user_name' in user_data and (user_data['user_name']=='akira'):
        # akiraがログインしている場合... (ここをifより深く下げる)
        pass 
    else:
        pass
'''
def analyse_input_area_data(user_data):
    # user_data['input__area_data']を解析し、data_retriever()が、処理できる形に変える
    pass
#selectタグの値が3(login又はログイン合の処理を行う
def analyse_input_area_data_for_select3(input_area_data):
    pass
#selectタグの値が4(ｒ＿materialism又は繋がりの唯物観）の場合の処理を行う
def analyse_input_area_data_for_select4(input_area_data):
    pass
#selectタグの値が5(opinion park又は意見の広場に対応）の場合の処理を行う
def analyse_input_area_data_for_select5(input_area_data):
    pass
#selectタグの値が6(blog又はブログに対応）の場合の処理を行う
def analyse_input_area_data_for_select6(input_area_data):
    pass
#selectタグの値が7(notify又はお知らせに対応）の場合の処理を行う
def analyse_input_area_data_for_select7(input_area_data):
    pass
#selectタグの値が8(sell又は販売に対応）の場合の処理を行う
def analyse_input_area_data_for_select8(input_area_data):

    # dataの読み込み、書き込みを判定し、仕分けをする
    # データベースからの読み込み用情報は<db> と/<db>の間、
    # 基本形は　==r or w==
    

    
    # それぞれを更に細かく仕分けする。
    
    # sqlステートメントの形にして返す。
    pass
# self.user_dataを使って、ページを表示する。必要項目は  
# i_name,page_title,input_area,output_area,footer
def show_page_handler(self):    
    pass
'''
'''
def remark_determination(user_data):
    global user_data_1
    user_data_1 = user_data
    # user_nameがない場合は、初期画面を表示する
    if  user_data_1['user_name'] == '':
        
        pass
    else:# user_nameがある場合は、select_areaとinput_areaのdataに基づいて、
         # 画面を表示する
        
        pass
'''


handler = Main_Handler()
user_data = {}
user_data['user_name']='akira'
user_data = handler.main(user_data)
print(user_data)
print('end')


if __name__ == "__main__":
    pass