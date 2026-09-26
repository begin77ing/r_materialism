'''プログラムの流れ：
views.pyでは、一人の訪問者に対して、一つの
sessionが作られ、その後プログラムは個々別々に
並行的に進行する。先ずud['session']の値は
'start'に設定されるが、ログインが完了すると1になり、
そのごsubmit ボタンが押され、求められていた処理が
終わる毎に、1ずつ加算される。又、プログラムの進行
が始まると、先ずud['input_area_data']の
:lang:の後に、 en 、又は :lang:jaが在るかを
確認し、ある場合には、言語を変えて、main_handler
でその他のデータを解析する。それが終わると、処理の主役
はeach_family_dealeになるが、処理を出来るだけ簡単に
する為に、option_infoテーブルのfamily_numberカラム
の値がud['family_number']に一致する
フィールドに記載の、command_stringから取得する。
詳細は決まっていないが、その後は、
ud['com']の値によって、処理が決まる流れ
にしたい。
次に、ud['select_area_num']が1の
場合のトップページに表示されるデータを
option_infoテーブルに登録するのに使われる
テンプレートについて考える 。
:fnu: <> :com::1:<> :2:<> :oth:<>  
を基本パターンとするが、:2:<>の<>の中に
複数の項目がある場合は;;で区切る。
例：option_infoにこのテンプレートを少し
修正した文字列を登録する
:fnu: <10102> 
:com::1:<'title'> 
:2:<relational_materialism/繋がりの唯物観>
:1:<> :2:<> 
        
:oth:<> 
                  
'''
#index.htmlに渡すol用のリスト
select_area_default_list = ['Home','Login',
'R_materialism','Blog','Opinion_Plaza',
'Notification','Contact','Author Intro',
'Sell']
select_area_num_list = {'Home':1,'ホーム':19,
'Login': 2,'ログイン':12 ,
'R_materialism':3 ,'繋がりの唯物観':13 ,
'Blog':4 ,'ブログ':14 ,
'Opinion_Plaza': 5,'意見の広場':15 ,
'Notification': 6,'お知らせ': 16,
'Contact':7,'コンタクト': 17,
'Author Intro':8,'著者紹介':18 , 
'Sell':9,'販売':19}


info_list= ['','title','select_area_data',
             'input_area_data','output_area_data',
             'announce_area_data','footer_area_data']
#　テーブル数は今のところは３つだが、4つに増やす予定。
table_list=['','option_info','user_data','display_data']
'''
〇option_info テーブルの仕様 
command_string       | text         |YES  |  
family_chord          | int         |YES  |  
family_number        | int         |YES  |  
explanation          | varchar(255)        |YES  |  
sentence       | text         |YES  | 
========= 
command_stringはtitle,select_area,input_area,
output_area,annoucement_area,footer_areaに表示
される文字列を収める。これらの項目名とその値はそれぞれ
:x1:と:x2:の後ろで<と>に挟まれる形で置かれる。例えば、
:x1:<title>:x2:<ホーム>....のように。
コマンドテンプレート。explanationはその使用説明文
rw_permissionは対応するcommand_stringの表示の対象を
表す為のもの。仕様と:x1:の値はcommand_stringと同じで、
:x2:に後続するその値は、all,user.self,又はakiraの
何れか
〇ud テーブルの仕様
i_name               | varchar(30)         |YES  |  
pas                  | varchar(30)         |YES  |  
email                | varchar(50)         |YES  |  
f_name               | varchar(30)         |YES  |  
login_history        | text         |YES  |  
rw_history           | text        |YES  |  
permission           | varchar(30)         |YES  |  
=========
f_nameはi_nameに代わるもので、i_nameを使いたくない時に
使われる。rw_historyはread,writeの記録だが、具体的
には、r又はw:family_chord+family_number+Goボタンを
押した時間;の連鎖の形とする。permissionは当面使う予定が
ないものだが、このままにしておく。
〇　display_data テーブルの仕様  
writer_name          | varchar(30)         |YES  |  
sentence             | text         |YES  |  
photo_address        | varchar(50)         |YES  |  
family_chord          | int        |YES  |  
display_destination  | varchar(30)         |YES  |  
rw_permission        | varchar(30)         |YES  |  
family_number        | int         |YES  |  
=========
rw_permissionは記事の作成者
が他のユーザ（akiraを除く）を念頭に置いて設定するもので、
値は当面、None又は''、self（自分自身だけ）,
all（全てのユーザ）だけとするが、None又は''の場合は
selfと同じと見做す。
'''
# database.pyのscrud関数で使われるコマンド識別名のリスト
scrud_command_list=['','fetch_one','fetch_all',
    'update_a_record','insert_a_record',
    'insert_records','delete_a_record',
    'delete_records','','confirm']
#　ユーザがGoボタンを押すと行われる処理が終わった段階で、views.pyの中で
# 
#deletable_data_list = ['','error','fnu','com','oth'\
#    ,'']
# セレクトタグの各オプションの値を収容するリスト
option_dic_e = {'Home':1,'Login':2,'R_materialism':3,
'Blog':4,'Opinion Plaza':5,'Notification':6,'Sell':7,
'Contact':8,'ForAdmin':9}
option_dic_j = {'ホーム': 11,'ログイン':12,
    '繋がりの唯物観':13,'ブログ':14,
    '意見の広場':15,'お知らせ':16,'販売':17,
    'コンタクト':18,'管理者用':19}
error_message_list_j = ['',
'list 又は、dicの規定範囲を超えるデータは受け付けられません',
':fnu:の後ろの値が不正です',
'此処にマイナス符号は付けられません',
'input_areaの入力に問題があります',
'input_areaの基本構造が崩れています',
'この操作は制作者にのみ可能です',
':com:の値を見直してください',
'データは既に存在しています。']
error_message_list_e = ['',
'Data exceeding the specified range for the list or \
dic will not be accepted.',
'The value after :fnu: is invalid.',\
'A minus sign cannot be placed here.' 
'this operation can be executed only by the author'
'the :com: should have wrong value','']
# command_listは、fnuの２桁目の値に対応する
command_list = ['','fetch_all','fetch_one',
    'update_a_record','insert_a_record','insert_records','delete_records']

# column_data_listの中のカラム数が収容されるが、不要かも
#　知れない。
table_value_list = ['',"(%s, %s , %s, %s , %s)",
    "(%s, %s , %s, %s, %s , %s ,%s)",
    "(%s, %s , %s, %s, %s , %s ,%s)"]
table_key_list =[[],
['command_string', 'family_chord','family_number',
 'explanation','sentence'] ,
['i_name','pas','email', 'f_name', 'login_history', 
 'rw_history', 'permission' ],
['writer_name','sentence','photo_address',
 'family_chord','display_destination','rw_permission',
 'family_number']]
'''
◆fnu_info = :fnu:の後ろのデータはユーザがどの
データをどうして欲しいかを表すと考えるべきものである。
それらは0で区切られる一連の数字[1-9]の並びで表現される。
その第一グループの数字は、処理の対象となるファミリー
グループの番号で、実行プログラムでのud['family_chord']
はそのままデータベースのfamily_chordに対応する。
第二グループの数字はファミリー内に於ける分類、
あるいはメンバー番号を表すもので、プログラムでの
ud['family_number']が、そのままデータベースの
family_numberカラム値に対応する。この、第一桁目の数字
は、トップページの表示用が1、作成用が2、削除が3、それ以外
の表示は4、唯一性を求める作成は5、求めない作成は6、削除は
7とする。二桁目の数字は1-6で、書き込み先を表す。即ち、
1はtitle、2はselect_area、3はinput_area、4はoutput_area、
5はannounce_area、6はfooter_areaである。このように、
トップページとそれ以外を分ける理由は、前者の表示
は、option_infoのだけで賄うようにする事と関連している。
-------
注意!第一、第二グループの数字は操作の対象となるデータの所在を
指定する為のものだが、0を挟んで続く、第三番目以降の数字は
ユーザが現在、そのデータに対して、どんな操作をしようとしている
かを表すものとなる。
----
第三グループの数字について。
1は単純な読み込み、2は唯一性を求める書き込み、
3は追加的書き込み、4は削除とする。
第四グループ数字の数字は、実行コマンドの流れを表す
もので、複数桁が可能とする。数字とコマンドの対応関係
はcommand_list に書いてあり、プログラムでの登録先は
ud['command_option_list']。
第五グループの数字は、データベース処理のプロセスに
関わる、テーブル名に対応する、数字を時系列順に並べた
もの2になる。登録先はud['table_num_list']。
option_infoは1、user_dataは2、display_dataは3なので
13なら、先ずoption_info続いて、display_dataが処理の
対象になる。

◆option_infoのカラムcommand_stringの書き方:
此処は、:fnu:の後ろの<>の中を補助して、
sql_statementを完成させるのに役立つデータが記述
される。対象テーブルがuserの場合は分かり易い例で、
その場合、:1:の後ろにはi_nameとかpasが来るし、
:2:の後ろには、akira や パスワード が来る。
'''
'''fetch insert等のデータベースcommandを数字に対応
#させるlist 1から9まではcrud関数のコマンド、11から
19まではdata_retriever関数のコマンドである。
'''
command_list = ['','fetch_one','fetch_all',
    'update_a_record','insert_record',
    'delete_record','','','','','',
    'create_tb','show_tb ','delete_table',
    'rename_table' ,'rename_column','drop_column',
    'modify_column','add_column','describe',' ',' ']


'''〇覚書
◆each_family_dealerに於けるプログラムの流れ
ud['select_area_num']の値に従って各family
に処理を区分けする。そこでは、userの
リクエストがreadの場合、または無くて、かつuserの
リクエストが新規writeの場合は、databaseからの読み込み
又はdatabaseへの削除しての書き込みのプロセスに入る。
それ以外の場合は、userに対して、データがないとのエラー
メッセージを返すか、又は確認を求めるメッセージを返す。
これ以降は

'''
'''以下は、トップページの表示の際に参照されるデータ。
当初はデータベースに登録する予定だったが、ここだけで
良いかも知れない。その場合、option_infoテーブルは
削除する事になる。
'''
class family_group_1():
    pass
    top_page_info_j = {
    'tiltle':'繋がりの唯物観',
    'select_area':'',
    'input_area':''':lang:< > :fnu:<11011010101>:com:< >
    :oth:< >''',
    'output_area':'''左側のテキスト欄の記号や数字の意味と
    他のパーツの役割について説明します。<br>
    最上部にあるのはページのタイトルです。このサイトの
    タイトルは全部で８つですが、このページの繋がりの唯物観とい
    タイトルはこのサイトの中心テーマを表すなので、サイトに
    アクセスした時点でも表示されるようにしています。
    ''',
    'annoucement_area':'',
    'footer_area':'''よいこそ、このサイトへ。
    <br>
    ''',}
class family_group_9():    
    '''各family_groupのトップページ表示の作成コマンド
    これらは、option_infoテーブルに収められる。その、
    データの内訳は、
    ==family_chord==
    19
    ==family_number==
    12
    ==command_string==
    :fnu:<a0102014011>:com:< > :oth:< > 
    ==explanation==
    初めのaは処理対象とするファミリーグループの番号
    なので、場合によって変わるーーー日本語の
    ファミリーグループの場合は、二桁の数字になる。
    次の1はトップページ関連のメンバーである事を示す。
    次の2は唯一性を求める作成である事を表し、
    次の14は処理コマンドで、1はfetch_oneを表し、
    それが見つからない（Noneでない）場合に実行される
    4は、insert_recordを表す。
    次の11は処理の対象が一回目、二回目共に、option_info
    である事を表す。
    '''
# data_dic = { 'command':'insert_a_record', 
# 'tb_name':'ud', 'sql_statement':
# '''INSERT INTO ud (i_name, pas, email,
# f_name, login_history, rw_history, permission)
# VALUES (%s, %s ,%s, %s ,%s, %s ,%s)''', 
# 'record_data': '''("akira", "bioture2025@gmail.com",
# "78sai_Kara_Yaritogerareruka”, ”wakesann”,2025-12-10,
# ’’,’all’)
# ''' }
'''◆input_areaに表示するコマンド文字列の最も基本的な
パターンを以下に示す。
:lang:<'space or ja or en ' >:fnu:<
'select_area_num' 0 'family_number' 0 
'command_sequence' 0 'table_sequence' >
:com::1:<'key1'>:2:<'val1;...'>:1:< >:2:<>
:oth:<  >
但し、これは、管理者用である。
実際の表示画面では、' と ' で囲まれた文字列はなく、
その代わりに具体的な数字を入っていて、ユーザが入力
するのは、:com:以下に限られるからである。
◆input_areaに表示する、コマンドテンプレートについて
以下では、プログラムの進行がFamily_9のdealerまで来たものと
仮定する。
◆各ファミリーに共通する、family_number の数字の
仕分け方、特に、その先頭の数字について：
1：トップページの表示コマンドを意味する：
2:それ以外の処理の実行文コマンドを意味する：
3：トップページの作成と変更コマンドを意味する：
＊ユーザのリクエストはoption_infoにあるテンプレート
の何れかに基本パターンが合致する筈なので、先ず、
それを作成する必要があり、その為の処理の実行文
が必要となる。
〇トップページの作成の具体例（
:lang:<ja >:fnu:< 9010401 >


    :com: 
        :1:<key1 >:2:<val11; val12>        
        :1:<key2 >:2:<val21; val22>
        :1:<key3 >:2:<val31; val32>
    
    :oth:<  >
family_chord(19）のinput_area
に表示される、option_infoテーブル（番号は最後の1）
に対して、insert_record（番号は三番目の4）を使うコマンド、データを書き込む。
'''
