import os
import sys
#import .. data_list #このファイルを直接実行する場合に使う
from myapp import  data_list #他のプログラム　views.py等から起動する場合


class ForAdmin():
    def interfacer(self,user_data):        
        try:
            print('start')
            
            
            pass
        except Exception as e:
            print(e)        
                        
        return user_data   
    
if __name__ == "__main__":
    '''
    user_data = {'title_area_data': 
    'Relational materialism/繋がりの唯物観'
    ,'select_area_data': 'ForAdmin' 
    ,'lang':'English'
    ,'output_area_data' : 'こんにちは！\n日本語を選択する方は' + 
    '左のテキスト欄の :fna:の後の \'Home\' ' +
    'を \'ホーム\' に置き換え、Goボタンを押して下さい。\n\n'  
    ,'announce_area_data':''
    ,'footer_area_data':''
    ,'user_name' : 'akira',#将来は空白に戻す
    'tb_name' : 'display_data',
    'command': 'insert_a_record',
    'column_data_list': ['writer_name','sentence',
    'photo_address','family_name','diplay_destination',
    'rw_permission ','family_number']}
    '''
    pass