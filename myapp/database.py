import mysql.connector
import datetime
class DB_Handler():
    def __init__(self):  
        pass
   
    def data_retriever(self,user_data):            
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="akira",
                password="dounimonarannZ78",)    
            cursor = conn.cursor()  
        except Exception as e:
            print(f"エラー1が発生: {e}")
            
        try:          
            cursor.execute("use r_materialism")               
            if 'command' in user_data:               
                if user_data['command'] == 'create_tb':
                    cursor.execute(user_data['sql_statement'])  
                elif user_data['command']=='show_tb':
                    # 全てのテーブル名を取得
                    cursor.execute("SHOW TABLES")
                    table_names = cursor.fetchall()
                    tables = [table[0] for table in cursor.fetchall()]
                    table_name0 = user_data['tb_name'] 
                    existing = False
                    for  table_name in tables:
                        print(f"テーブル '{table_name}' は存在します。")
                elif user_data['command'] == 'delete_table':
                    sql = "DROP TABLE IF EXISTS" + \
                    user_data['tb_name']
                    cursor.execute(sql)  
                    ''' 既存のテーブルの内容を
                    広い意味で変える。
                    data['sql_statement']は
                    sql文を表す
                    '''     
                elif user_data['command'] == 'column_rename' \
                        or user_data['command'] == 'drop_column' \
                        or user_data['command'] == 'modify_column' \
                        :\
                    cursor.execute(user_data['sql_statement'])
                else:
                    #data_dicのcommand項目は必要
                   user_data = crud_data(conn,cursor,user_data)
                   return user_data
                # 変更を確定
                conn.commit()
                # SHOW TABLESを実行
                cursor.execute("SHOW TABLES")
                # 結果を取得
                tables = cursor.fetchall()
                # テーブル名を表示
                print("データベースのテーブル一覧:")
                for table in tables:
                    print(table[0])
                return user_data
            else:
                return user_data
        except Exception as e:
            print(f"エラー2が発生: {e}")
        finally:            
            return user_data
        # 接続を閉じる
            cursor.close()
            conn.close()
def crud_data(conn,cursor,user_data):
    try:        
    # テーブルの内容を追加、変更する
    #   先ずはレコード一つの取得
        if user_data['command'] == 'fetch_one':
             # データ取得のクエリ、再編集
                select_one_data_query =\
                "SELECT * FROM " + \
                user_data['tb_name'] + \
                user_data['sql_statement'] 
                cursor.execute(select_one_data_query, (user_data['key_val']))
                # 結果を取得
                result = cursor.fetchone()
                # 全レコードを取得
        elif user_data['command'] == 'fetch_all':
        # データ取得のクエリ
                select_all_data_query = \
                "SELECT * FROM "+ user_data['tb_name']+ " " + \
                user_data['sql_statement']        
                # データ取得
                cursor.execute(select_all_data_query)
                result = cursor.fetchall()
                return result
        elif user_data['command'] == 'update_a_record':
                 # データ更新のクエリ
                update_query = "UPDATE " + \
                user_data['tb_name'] + \
                user_data['sql_statement']

                # データ更新
                cursor.execute(update_query)
    
            # レコード一つの挿入
        elif user_data['command'] == 'insert_a_record':
            # データ挿入のクエリ
                one_record_query = " \
                INSERT INTO " + user_data['tb_name']  \
                + user_data['sql_statement']
                cursor.execute(one_record_query)
            # 複数のレコードの挿入
        elif user_data['command'] == 'insert_records':
            # データ挿入のクエリ
                multiple_records_query = " \
                INSERT INTO " + user_data['tb_name']  \
                 + user_data['sql_statement']
                cursor.execute(multiple_records_query)
        elif user_data['command'] == 'delete_record':            
                multiple_records_query = " \
                DELETE FROM " + user_data['tb_name']  \
                 + user_data['sql_statement']
                cursor.execute(multiple_records_query)
    
            # 変更を確定
        conn.commit()
    except Exception as e:
            user_data['return_val'] = "テーブル操作中にエラーが発生: {e}"
    else:
            user_data['return_val'] = 'テーブル操作が完了しました。'
    finally:
            return user_data

if __name__ == "__main__":
    pass