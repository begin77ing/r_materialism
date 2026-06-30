import numpy as np
#databaseへのアクセスと操作を容易にするためのデータを保存する
#それは、database.pyへ組み込まれるが、そこに於けるfnuの値の
#先頭の値が1の場合は、select_dataテーブルに関わるデータ、2の場合は、
# user_dataテーブル、3の場合はdisplay_dataテーブルが対応する。
# 4　も予備に用意しておく（下方を参照）input_areaのfnu入力値
#(二桁目の数字)はコマンドに対応するが、このファイルでは扱わず、
#対応付けは main_handler内のコードに委ねる。
#と言うのも、 それは、テーブルの違いに拠らず、共通して、
# database.pyのcrud_data関数の中に登場するcommandの値と対応するから。
# それと数字の関係は、（上から1,2,3...）である。
# テーブルを追加または削除したり、名前を変えたり、
# するコマンドについては、現時点では考えてないが、もし将来追加する場合
# には、上記した予備扱いとし、4を振って、そこにまとめる事にする。
# 又、無いとは思うが、万一テーブルのレコード処理のコマンドが増えて
# 10個を超える場合は、10はスキップし、11,12,13....を振る事にする。
# このファイルに収納されるデータは、input_areaの入力値のcom部分で、
# そのkey値とvalue値に対応するformがどんなものかを表すものとする。
for_admin ='''
input_area_data の基本テンプレートは、\n
:fnu:   :com:   :oth:   です。これらに値を入れる場合、\n
①:fnu:の後には数字が入りますが、その各桁(1-9)の一文字)はで区切らなければなりません。\n
そして、各桁の数字には意味があります。第一桁が1の場合、select_area_dataが\n
対応し、2の場青は、user_ddta、3の場合は、display_area_data が対応します。4 以降\n
は予備のテーブル用（将来の拡張に備えて）\n
二桁目は、データベースの操作コマンドを表す数字で、main_handlerのcrud_data関数\n
に対応します。その対応表は、今のところ、下記の通りです。\n
9 を超える場合は、11 からスタート\n
ところで、databafetch_onese.py の crud_data関数内に、\n
user_data['adr']を追加した方が良いかもしれません\n
https://techis.jp/guide/python/python_mysql_delete 参照\n

0 :  \n
1 : fetch_all \n
2 : update_a_record \n
3 : insert_a_record \n
4 : insert_records \n
5 : delete_records \n
6 : 


'''

# user_dataの初期値設定用の辞書
default_value_dic = {'user_name':'','page_num': 0,\
    'lang':'English',
    'title_area_data': 'Relational materialism/\
    繋がりの唯物観','select_area_data': 'Home',\
    'input_area_data':':fna: Home :fnu: 0 :com: ' + \
    '\n\nHello!\nIf you want '+
    '''to see another content of this site,please select Login '+
    in the left select box and then push Go button
    underneath.'''\
    ,'output_area_data':'''こんにちは！\n日本語を選択
    する方は、左のテキスト欄の :oth:の直ぐ後に、半角の強調文字
    &nbsp; change_Lang_to_  &nbsp;をコピペし、Goボタンを押して下さい。
    この操作は常に有効で、その都度、言語モードが切り替ります。 
    ''','announce_area_data':'','footer_area_data':''}
#target_dicはindex.htmlの表示箇所と数字を対応させるリスト
target_list= ['','title','select_area_data',
             'input_area_data','output_area_data',
             'announce_area_data','footer_area_data']
#　現時点でのテーブル数は３つ。将来も変えたくないが...
table_list=['','option_info','user_data','display_data']
# database.pyのscrud関数で使われるコマンド識別名のリスト
scrud_command_list=['','fetch_one','fetch_all',
    'update_a_record','insert_a_record','insert_records'
    ,'delete_a_record','delete_records']
#　ユーザがGoボタンを押すと行われる処理が終わった段階で、views.pyの中で
# 
#deletable_data_list = ['','error','fnu','com','oth'\
#    ,'']
# セレクトタグの各オプションの値を収容するリスト
option_dic_E = {'Home':1,'Login':2,'R_materialism':3,
'Blog':4,'Opinion Plaza':5,'Notification':6,'Sell':7,
'Contact':8,'ForAdmin':9}
option_dic_J = {'ホーム': 1,'ログイン':2,'繋がりの唯物観':3,
'ブログ':4,'意見の広場':5,'お知らせ':6,'販売':7,
'コンタクト':8,'管理者用':9}
error_message_list_J = ['','list 又は、dicの規定範囲を超えるデータは受け付けられません',
':fnu:の後ろの値が不正です','此処にマイナス符号は付けられません',
'input_areaの入力に問題があります','input_areaの基本構造が崩れています',
'このページは管理者用です',':com:の値をチェックしてください']
error_message_list_E = ['','Data exceeding the specified range for the list or \
    dic will not be accepted.','The value after :fnu: is invalid.',\
   'A minus sign cannot be placed here.' ,'the :com: should have wrong value','']
#table_listは、fnuの一桁目の値に対応する
table_list = ['','option_info','user_data','display_data']
# command_listは、fnuの２桁目の値に対応する
command_list = ['','fetch_all','fetch_one',
    'update_a_record','insert_a_record','insert_records','delete_records']
#:com:のcdlキーの値（以下のテーブルを1,2,3で区別）に対応する
#フィールドのカラム名を要素とするリストを要素とする。
#これを使えば、対応するvaluesの値も自動的に決める事が出来る。
column_data_list = ['',
['command_string','family_name','family_number'],
['i_name','pas','email','f_name','login_history',
    'rw_history','permission'],
['writer_name','sentence','photo_address','family_name',
 'diplay_destination','rw_permission ',' family_number'
]]
# column_data_listの中のカラム数が収容されるが、不要かも
#　知れない。
values_code_list = ['',"(%s, %s , %s)",
    "(%s, %s , %s, %s, %s , %s ,%s)",
    "(%s, %s , %s, %s, %s , %s ,%s)"]
fnu_info = ''':fnu:の後ろのデータについてーー0で区切られる[1-9]数字。
一番目はselectタグで選択されたfamily_nameに対応する番号か否かをチェックし、
処理する為の数字。（通常は一桁だが、akiraが管理者として振る舞う場合は、
9で始まる二桁の数字でマイナス符号が付くーーその後の処理で、前の9は除かれる）
数字は、user_data['select_area_data']との対応性をチェックされ、
もし結果がTrueなら、それが処理の対象のファミリーグループを表す数字となる。
二番目の数字は大まかな処理の区別、それ以降の数字のリスト、user_data['family_number']
は、ファミリーグループ、そのサブグループ、そのサブサブグループ...
を表すものだが、データベースでのfamily_numberに相応する--但し、それは
[1-9]の数字の間に0を挟んだ--もので、その最後の桁の数字は表示位置を示す
指標になる}
'''
''':com:の値を解析する上で役立つcom_asisting_dic は辞書の辞書で構成される
が、

'''
# 以下、:com:データを処理する際の参考資料
com_asisting_dic = {
    'i_name':{'min':2,'max':15,'uni':True,'rom':True},#romで半角英数字と
    'pas':{'min':8,'max':20,'uni':True,'rom':True},#ハイフン、アンダーバーを表す
    'email':{'uni':True,'em_con':True},
    'f_name':{'min':2,'max':30},'rom':True}
#fnu_third_num_list=['',1,2,2,2,]
'''
以下は各ファミリー毎のクラスの記述だが、それぞれには、所属するファミリーメンバー（数字で
表す）のリストfamily_num_listとその番号に対応するfnu文字列を格納する辞書（fnu_num_dic）
及び、その説明文（＝fnu_exp_dic：これはfnu_data_dicと同じkey）等、グループとして
一括される定数だけが定義される。これらを使えば、main_handlerのクラスオブジェクトは、
userやadminのリクエストに応じた、全ての処理が可能になると期待される
    display_data (id INT PRIMARY KEY AUTO_INCREMENT,
    writer_name TEXT,
    sentence TEXT,
    photo_address TEXT,
    family_name TEXT,
    diplay_destination TEXT,
    rw_permission TEXT,
    family_number TEXT DEFAULT NULL)     
    }

'''
class family_group_1():
    # このグループの所属メンバーを表す数字で、:fnu:の後の一番目の数字
    # インデックス1はデータの全面表示で全ユーザーに開かれている。
    # 2は変更でakiraにだけ、可能（np仕様で、部分的変更）
    fnu_second_num_list =['',1,2]
    #fnu_second_num_listの各要素（リスト）に対応するinput_areaのフォーム    second_num_statement_dic = {}
    # や説明で、これは、userがakiraの場合だけ実行されて、
    # output_area_dataに表示される
    second_num_exp_dic ={2:'family_numer 1 は、'+
        'ホーム画面に関するデータを全面表示させるコマンドの基本的フォームで'+
        '、全てのユーザに対して許可するが、それ以外は、'+
        'user_data[''adm'']= Trueの場合にだけ可能とする。その場合は、'+
        '以下のフォームを参考にして、適宜改変する。'}

class family_group_9():
    # このグループの所属メンバーを表す数字のリストのリスト
    # このグループの場合は、
    fnu_second_num_list =[]
    #fnu_second_num_listの各要素（リスト）に対応して、output_area_dataに表示する入力用文
    second_num_statement_dic = {}
    # fnu_second_num_listの各要素（リスト）に対応して、output_area_dataに表示する説明文
    second_num_exp_dic ={}
# data_dic = { 'command':'insert_a_record', 
# 'tb_name':'user_data', 'sql_statement':
# '''INSERT INTO user_data (i_name, pas, email,
# f_name, login_history, rw_history, permission)
# VALUES (%s, %s ,%s, %s ,%s, %s ,%s)''', 
# 'record_data': '''("akira", "bioture2025@gmail.com",
# "78sai_Kara_Yaritogerareruka”, ”wakesann”,2025-12-10,
# ’’,’all’)
# ''' }


