import mysql.connector
import datetime
class DB_Handler():
    def __init__(self):  
        pass
   
    def data_retriever(self,user_data):        
        self.user_data = user_data
        #dat_for_fetching = determine_data_for_fetching(user_data)
        
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="akira",
                password="dounimonarannZ78",)    
            self.cursor = self.conn.cursor()  
        except Exception as e:
            print(f"エラー1が発生: {e}")
            
        try: 
            result = None           
            self.cursor.execute("use r_materialism")               
            if 'command' in self.user_data:               
                if self.user_data['command'] == 'create_tb':
                    self.cursor.execute(self.user_data['sql_statement'])  
                elif self.user_data['command']=='show_tb':
                    # 全てのテーブル名を取得
                    self.cursor.execute("SHOW TABLES")
                    table_names = self.cursor.fetchall()
                    tables = [table[0] for table in self.cursor.fetchall()]
                    table_name0 = self.user_data['tb_name'] 
                    existing = False
                    for  table_name in tables:
                        print(f"テーブル '{table_name}' は存在します。")
                elif self.user_data['command'] == 'delete_table':
                    sql = "DROP TABLE IF EXISTS" + \
                    self.user_data['tb_name']
                    self.cursor.execute(sql)  
                    ''' 既存のテーブルの内容を
                    広い意味で変える。
                    data['sql_statement']は
                    sql文を表す
                    '''     
                elif self.user_data['command'] == 'column_rename' \
                        or self.user_data['command'] == 'drop_column' \
                        or self.user_data['command'] == 'modify_column' \
                        :\
                    self.cursor.execute(self.user_data['sql_statement'])
                else:
                    #data_dicのcommand項目は必要
                    result = self.crud_data()
                    if not result:
                        return None
                # 変更を確定
                self.conn.commit()
                # SHOW TABLESを実行
                self.cursor.execute("SHOW TABLES")
                # 結果を取得
                tables = self.cursor.fetchall()
                # テーブル名を表示
                print("データベースのテーブル一覧:")
                for table in tables:
                    print(table[0])
                return result
        except Exception as e:
            print(f"エラー2が発生: {e}")
        finally:
        # 接続を閉じる
            self.cursor.close()
            self.conn.close()
    def crud_data(self):
        try:        
        # テーブルの内容を追加、変更する
    #   先ずはレコード一つの取得
            if self.data_dic['command'] == 'fetch_one':
             # データ取得のクエリ、再編集
                select_one_data_query =\
                "SELECT * FROM " + \
                self.user_data['tb_name'] + \
                self.user_data['sql_statement'] 
                self.cursor.execute(select_one_data_query, (self.user_data['key_val']))
                # 結果を取得
                result = self.cursor.fetchone()
                # 全レコードを取得
            elif self.user_data['command'] == 'fetch_all':
        # データ取得のクエリ
                select_all_data_query = \
                "SELECT * FROM "+ self.user_data['tb_name']+ " " + \
                self.user_data['sql_statement']        
                # データ取得
                self.cursor.execute(select_all_data_query)
                result = self.cursor.fetchall()
                return result
            elif self.data_dic['command'] == 'update_a_record':
                 # データ更新のクエリ
                update_query = "UPDATE " + \
                self.user_data['tb_name'] + \
                self.user_data['sql_statement']

                # データ更新
                self.cursor.execute(update_query, self.user_data['record_data'])
    
            # レコード一つの挿入
            elif self.user_data['command'] == 'insert_a_record':
            # データ挿入のクエリ
                one_record_query = " \
                INSERT INTO " + self.data_dic['tb_name']  \
                + data_dic['sql_statement']
                self.cursor.execute(one_record_query, self.user_data['record_data'])
            # 複数のレコードの挿入
            elif self.user_data['command'] == 'insert_records':
            # データ挿入のクエリ
                multiple_records_query = " \
                INSERT INTO " + self.data_dic['tb_name']  \
                 + self.user_data['sql_statement']
                self.cursor.execute(multiple_records_query, self.user_data['record_data'])
    
            # 変更を確定
                self.conn.commit()
        except Exception as e:
            return_val = "テーブル操作中にエラーが発生: {e}"
        else:
            return_val = 'テーブル操作が完了しました。'
        finally:
            return return_val
'''
def determine_data_for_fetching(user_data):
    # データベースから情報を得る為に必要なデータ、即ち ata_dic['command_name']
    # ,data_dic['tb_name'],data_dic['sql_statement']等を要素とするリスト
    pass
'''    
# 以下は実行歴
#data_dic= {'this_database': 'r_materialism'}
#data_dic = {'db_name': 'r_materialism'}
"""
data_dic = {
    'command':'create_tb',\
    'tb_name': 'option_info',\
    'sql_statement':'''CREATE TABLE IF NOT EXISTS 
    option_info (id INT AUTO_INCREMENT PRIMARY KEY, 
    command_string TEXT,
    family_name TEXT,
    family_number INT
    )     
    '''}   
"""
"""
data_dic = {
    'command':'create_tb',
    'tb_name': 'user_data',
    'sql_statement':'''CREATE TABLE IF NOT EXISTS 
    user_data (id INT PRIMARY KEY AUTO_INCREMENT,
    i_name TEXT,
    pas TEXT,
    email TEXT,
    f_name TEXT,
    login_history DATE,
    rw_histroy DATE,
    permission TEXT,
    spare_data_dl TEXT DEFAULT NULL)     
    '''}
"""
'''
id:PRIMARY_KEY AUTO_INCREMENT,
    data_history DATE
    reader INT
    writter INT
'''
    
'''
data_dic={'this_database':'r_materialism',\
    'command':'create_tb'}
'''
"""
data_dic = {
    'command':'insert_a_record',
    'tb_name': 'user_data',
    'sql_statement':'''(i_name,
    pas,email,f_name,login_history,
    rw_histroy,permission) values 
    (%s,%s,%s,%s,%s,%s,%s,%s),
    'record_data':
    'akira','aKIRAMEnai_78',
    'bioture2025@gmail.com',
    'potato salad',
    ,Null,Null,'admin',Null
    '''}
"""
"""
data_dic = {
    'command':'column_rename',
    'tb_name': 'option_info',
    'sql_statement':'''
    ALTER TABLE option_info
    RENAME COLUMN display_name TO family_name '''
    }
"""
"""
data_dic = {
    'command':'column_drop',
    'tb_name': 'option_info',
    'sql_statement':'''
    ALTER TABLE option_info
    RENAME COLUMN display_name TO family_name '''
    }
"""
"""
data_dic = {'command':'drop_column',\
'tb_name':'user_data',\
'sql_statement':'''
ALTER TABLE option_info
  DROP spare_data_dl

'''}

"""
"""
data_dic = {
    'command':'column_rename',
    'tb_name': 'display_data',
    'sql_statement':'''
    ALTER TABLE display_data  
    RENAME COLUMN option_name TO family_name
    '''}
"""
"""
data_dic = {
    'command':'insert_a_record',
    'tb_name':'user_data',
    'sql_statement': '''
    
    '''}
"""

"""
data_dic = {
    'command':'modify column',
    'tb_name':'user_data',
    'sql_statement': '''
    ALTER TABLE user_data  MODIFY 
    rw_history TEXT
    '''}
"""
data_dic = {
    'command':'insert_a_record',
    'tb_name':'user_data',
    'sql_statement': '''
    INSERT INTO user_data (i_name, pas,
    email, f_name, login_history, 
    rw_history, permission) 
    VALUES (%s, %s ,%s, %s ,%s, %s ,%s)''',
    'record_data': '''("akira", 
    "bioture2025@gmail.com",
    "78sai_Kara_Yaritogerareruka”, 
    ”wakesann”,2025-12-10,’’,’all’)    
    ''' }
#handler = DB_Handler()
#result = handler.data_retriever(data_dic)



if __name__ == "__main__":
    pass