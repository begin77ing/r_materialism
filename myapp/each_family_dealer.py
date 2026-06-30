import os
import sys
import data_list

#optionタグの選択が何番目であるかによって、main}_handlerから呼び出される
# ファミリークラスが変わる。呼び出されたクラスは、リクエストに応じて、
# メンバー毎の処理文が表示又は実行されるように準備し、それをデータベースとの
# やり取りやエラーの有無に応じて、user_data['error']、
# user_data['display_data']又は、user_data['sql_statement']として、返す。
class Whole_Family():
    def __init__(self):
        com_asisting_dic = \
        data_list.com_asisting_dic          
    def family_dealer(self,user_data) :        
        match user_data['select_area_data']: 
            case "Home" | "ホーム" :  
                the_family = Family_1()
                user_data = the_family.dealer(user_data)
            case "Login" | "ログイン":
                the_family = Family_2()
                user_data = the_family.dealer(user_data)
            case "R_materialism" | "繋がりの唯物観":
                the_family = Family_3()
                user_data = the_family.dealer(user_data)
            case "Blog" | "ブログ" :
                the_family = Family_4()
                user_data = the_family.dealer(user_data)
            case "Opinion Plaza" | "意見の広場":
                the_family = Family_5()
                user_data = the_family.dealer(user_data)
            case "Notification" | "お知らせ": 
                the_family = Family_6()
                user_data = the_family.dealer(user_data)
            case "Sell" | "販売" :
                the_family = Family_7()
                user_data = the_family.dealer(user_data)
            case "Contact" | "コンタクト":
                the_family = Family_8()
                user_data = the_family.dealer(user_data)
            case "ForAdmin" | "管理者用":
                the_family = Family_9()
                user_data = the_family.dealer(user_data)
            case _:               
            # この場合、エラーコードを返すだけにする
                user_data['error'] = user_data['error_message_list'][4]
                return user_data  
        return user_data
class Whole_Family():
    def __init__(self):
        self.taget_list = data_list.target_list
    
    def common_treatment():
        '''user_data['family_number']の違いに関わらず、共通する
        部分を此処で処理する。先ず、その第一要素
        1は、ユーザによる単純な読み出しへ飛ぶ、
        2は、もし権限が在れば新規の書き込みへ飛ぶ、
        3は、もし権限が在れば削除を含むデータの変更へ飛ぶ
        4は、akiraによる単純な読み出しへ飛ぶ、
        5は、書き込みへ飛ぶ、
        6は削除を含むデータの変更へ飛ぶ
        但し、5で、処理の対象がdisplay_dataの場合,コマンドは
        insertで同じ筈なので、一括処理としたい。そこで、comデータ
        は全て、一旦ダブルコロン,,でリストの形とする。
        '''
        print('此処はどこ？')
        
        pass    
    def preparation(self,user_data):
        print(user_data['select_area_num'])
        match user_data['select_area_num']:
            case 1:
                handler = Family_1()
            case 2:
                handler = Family_2()
            case 3:
                handler = Family_3()
            case 4:
                handler = Family_4()
            case 5:
                handler = Family_5()
            case 6:
                handler = Family_6()
            case 7:
                handler = Family_7()
            case 8:
                handler = Family_8()
            case 9:
                handler = Family_9()
            case _:
                pass        
        user_data = handler.dealer(user_data)
        return user_data   

class Family_1(Whole_Family):
    def dealer(self,user_data):
        print('get here finally')
        pass    
class Family_2(Whole_Family):
    def dealer(self,user_data):
        pass
class Family_3(Whole_Family):
    def dealer(self,user_data):
        pass
class Family_4(Whole_Family):
    def dealer(self,user_data):
        pass    
class Family_5(Whole_Family):
    def dealer(self,user_data):
        pass
class Family_6(Whole_Family):
    def dealer(self,user_data):
        pass       
class Family_7(Whole_Family):
    def dealer(self,user_data):
        pass
class Family_8(Whole_Family):
    def dealer(self,user_data):
        pass   

class Family_9(Whole_Family):
    def dealer(self,user_data):
        '''input_areaの :fnu:の入力値が
        -9y00x(yは、1<=,<=9の数字で、ターゲットとなる9個のファミリー
        メンバーを表すが、この場合は9）又、(xはサブグループ番号で、0以外の数字
        よりなり)、>=1でなければならない。このぺージで
        はっきりしているのは、1 は 管理者用ページの表示、
        2は 管理者用ページの変更、3は他のファミリーグループに
        関するデータの登録や削除を表す。     
        '''
        print('get here')
        
        return
        pass
           
           
           
def make_sql_statement(user_data):
    print('get here')
    return user_data
    pass
def make_display_data(user_data):
    print('get here')
    return user_data
    pass

