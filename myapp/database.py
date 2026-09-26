import datetime
import pymysql

class DB_Handler():
    def __init__(self):  
        pass
   
    def data_manager(self, ud):            
        conn = None
        cursor = None
        try:
            # ★ pymysql.connect に変更（auth_pluginは不要になります）
            conn = pymysql.connect(
                host="localhost",
                user="akira",      # 正しいユーザー名
                password="dounimonarannZ78",  # 正しいパスワード
                database="r_materialism"
            )    
            cursor = conn.cursor()  
            print("データベース接続に成功しました。")

            # 2. コマンド処理（ここは前回提示した内容のままでOKです）
            if 'command' in ud :               
                if ud['command'] == 'create_tb':
                    cursor.execute(ud['sql_statement'])  
                
                elif ud['command'] == 'show_tb':
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()
                    for table in tables:
                        print(f"テーブル '{table}' は存在します。")
                                 
                elif ud['command'] in ['delete_table','rename_table',
                    'RENAME COLUMN','DROP COLUMN',
                    'MODIFY','add_column']:
                    cursor.execute(ud['sql_statement'])
                
                elif ud['command'] == 'describe':
                    cursor.execute(ud['sql_statement'])
                    columns = cursor.fetchall()
                #此処ではターミナルに出力している 
                #が、将来はoutput_areaに変える                  
                    for col in columns:                    
                        print(f"{col[0]:<20} | {col[1]:<20}|{col[2]:<5}|{col[3]:<20}")
                    print("=========")
                else:
                    ud = crud_data(conn, cursor, ud)
                    return ud
                
                conn.commit()
                
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print("データベースのテーブル一覧:")
                for table in tables:
                    print(table)
                return ud
            else:
                return ud

        except Exception as e:
            print(f"データベース処理中にエラーが発生しました: {e}")
            if conn:
                conn.rollback()
            return ud
            
        finally:            
            if cursor:
                cursor.close()
            if conn:
                conn.close()      
            return ud          
            
def crud_data(conn,cursor,ud):
    try:        
    # テーブルの内容を追加、変更する
    #   先ずはレコード一つの取得
        if ud['command'] == 'confirm':
    # f-string で正しく変数展開するように修正
            query = f"SELECT EXISTS(SELECT 1 FROM {ud['tb_name']}{ud['sql_statement']} LIMIT 1)"
    
            cursor.execute(query, ud['params'])
            exists_flag = cursor.fetchone()[0]  # 0 または 1
            ud['result'] = bool(exists_flag)
            return ud

        if ud['command'] == 'fetch_one':
            select_one_data_query = (
            "SELECT * FROM " + 
            ud['tb_name'] + 
            ud['sql_statement']
            )
            print()
        # タプル形式 (val,) で渡す
            #cursor.execute(select_one_data_query, (ud['key_val'],))    
            cursor.execute(select_one_data_query)
            ud['db_result'] = cursor.fetchone()
            return ud
        elif ud['command'] == 'fetch_all':
        # データ取得のクエリ
                select_all_data_query = \
                "SELECT * FROM "+ ud['tb_name']+ " " + \
                ud['sql_statement']        
                # データ取得
                cursor.execute(select_all_data_query)
                result = cursor.fetchall()
                return ud
        elif ud['command'] == 'update_a_record':
                 # データ更新のクエリ
                update_query = "UPDATE " + \
                ud['tb_name'] + \
                ud['sql_statement']

                # データ更新
                cursor.execute(update_query)
    
            # レコードを挿入
        elif ud['command'] == 'insert_record':
            try:
                cursor.execute(ud['sql_statement'], ud['sql_data'])
                conn.commit()        
            except Exception as e:
                # ★エラーの理由をターミナルに出力させる
                print("❌ 失敗理由:", e, flush=True)
        elif ud['command'] == 'delete_record':            
            multiple_records_query = " \
            DELETE FROM " + ud['tb_name']  \
            + ud['sql_statement']
            cursor.execute(multiple_records_query)
        
        conn.commit()
        print('successfully executed!')
    except Exception as e:
            ud['return_val'] = "テーブル操作中にエラーが発生: {e}"
    else:
            ud['return_val'] = 'テーブル操作が完了しました。'
    finally:
        print('all done')
        return ud
if __name__ == "__main__":
    print('main start') 
    ud = {}
    ud['tb_name']='display_data'    
    #ud['command'] = 'RENAME COLUMN'
    ud['command'] = 'describe'
    #ud['command'] = 'MODIFY'
   
    #ud['sql_statement'] = (
    #    f"ALTER TABLE {ud['tb_name']} {ud['command']} family_name to family_chord;")
    #ud['sql_statement'] = (f"ALTER TABLE display_data MODIFY family_chord INT")
    ud['sql_statement'] = (f"DESCRIBE display_data ")
    
    '''
    handler = DB_Handler()
    ud = handler.data_manager(ud)  
    print('result = ', ud
          )
    '''   
    
    '''insert文の具体例：
    sql = ("
        INSERT INTO student 
            (first_name, last_name, birthday, gender)
        VALUES 
            (%s, %s, %s, %s)
        ")
    
        data = [
            ('Shota', 'Sato', '2001-03-12', 'M'),
            ('Hiroki', 'Takagi', '2000-04-05', 'M'),
            ('Yuka', 'Kimura', '2001-03-27', 'F')
        ]
    
        cursor.executemany(sql, data)
        
            '''
    '''    
    # 登録用データ
    ud = {
        'tb_name': 'option_info',
        'command': 'describe'
    }
    ---------------------
    ud = {
        'command': 'insert_record',
        'tb_name': 'ud',
        # 7つのカラムに対して %s を正しく7個指定
        'sql_statement': '(i_name, pas, email, f_name, login_history, rw_history, permission) VALUES (%s, %s, %s, %s, %s, %s, %s)',
        # 値はタプル形式で7要素渡す（NullはPythonのNoneを使う）
        'record_data': (
            'akira',
            'aKIRAMEnai_78',
            'bioture2025@gmail.com',
            'potato salad',
            None,
            None,
            'admin'
        )
    }
    handler = DB_Handler()
    result = handler.data_retriever(ud)     
    print('result = ', result)
    ----------------------------
    print('main start')    
    ud = {}  
    ud['tb_name'] = 'ud'     
    ud['command'] = 'fetch_one'
    ud['sql_statement'] = ' WHERE i_name = %s;'
    ud['key_val'] = 'akira'  # 値をセット
    
    handler = DB_Handler()
    result = handler.data_retriever(ud) 
    print('result = ', result)
    '''
'''
if __name__ == "__main__":
    print('main start')    
    ud = {}  
    ud['tb_name'] = 'ud'     
    ud['command'] = 'fetch_one'
    ud['sql_statement'] = \
    f' WHERE i_name = "akira";'
    
    handler = DB_Handler()
    result = handler.data_retriever(ud) 
    print('result = ',result)
    '''
'''
    
    ud['command'] = 'RENAME COLUMN'
    ud['tb_name'] = 'ud'
    ud['sql_statement'] = (
            f'ALTER TABLE {ud['tb_name']} RENAME COLUMN rw_histroy to rw_history;')
     ----------------
    ud['command'] = 'modify_column'
    ud['tb_name'] = 'ud'
    ud['sql_statement'] = (
        f'ALTER TABLE {ud['tb_name']} MODIFY rw_history TEXT;')
    ------------------
    ud['tb_name'] = 'display_data' 
    ud['command'] = 'describe'
    ------------------
    ud['command'] = 'add_column'
    ud['sql_statement'] = (
    f"ALTER TABLE {ud['tb_name']} "
    f"ADD COLUMN id INT PRIMARY KEY AUTO_INCREMENT, "
    f"ADD COLUMN i_name VARCHAR(30);"
)
    ud['tb_name'] = 'ud' 
    ud['command'] = 'describe'
    handler = DB_Handler()
    handler.data_retriever(ud) 
'''



