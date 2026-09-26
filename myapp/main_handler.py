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
        #ud = {'page_num':0,'login':False}
        #self.main_handler(ud)
        pass
    def main_handler(self,ud):  
        try:
            ud['error'] = ''
            if 'session' in ud:
                ud = initial_stage(ud)            
            ud = fnu_analyser(ud)
            if ud['error'] != '':
                return ud
            if 'com' in ud and ud['com'] != '':
                ud = com_analyser(ud)
            if ud['error'] != '':
                return ud
            
            #input_areaの処理が終わったので、各familyグループ毎の処理に移る。
            #import each_family_dealer
            print('before handler')
            ud['handler']=database.DB_Handler()
            efd = each_family_dealer.Whole_Family()
            ud = efd.common_treatment(ud)
            if ud['error'] != '':
                return ud
        except Exception as e: 
            ud['error'] = e
        finally:
            if ud['error'] != '':
                ''' 該当するトップページの表示に戻るが、
            それと共に、user_data関連を除く他のudデータ
            を初期化し、エラーをoutput_area_dataに入れる'''   
                pass            
            return ud
        
def initial_stage(ud):
    try:   
        #del ud['session'] 
        if ud['error'] != '':
            return ud  
        ud = lang_treatment(ud)
        content = ud['input_area_data']   
        pattern = (
    r'\s*:lang:<\s*(\S*)\s*>'
    r'\s*:fnu:<\s*(\d{1,20})\s*>'
    r'\s*:com:<([\s\S]*?)>'
    r'\s*:oth:<\s*(.*?)\s*>\s*'
) # 末尾に \s*
            # input_areaのデータをudの中に納める        
        result =  matching_handler(content,pattern)
            # :com:の後ろに具体的なデータが在るとみられる場合
            # listの形で ud['com']　に収納しておく
            #ud['com'] = {k: v for k, v in pairs}
        if result:            
            ud['new_lang'] = result.group(1)
            '''言語変更のリクエストが在った.場合の対応'''
            if ud['new_lang'] != ('' or ud['lang']):
                ud = lang_treatment(ud)                
                del ud['new_lang']           
            ud['fnu'] = result.group(2)
            ud['com'] = result.group(3)   
            ud['oth'] = result.group(4)
           
        
        #同じ処理をするデータに番号を付ける
        #ud['family_name'] = ud['select_area_data']
        print('here')
        ud['select_area_num'] = \
        ud['option_dic'][ud['select_area_data']]
        '''例えば、optionで’Home’が選ばれ、langが
        日本語の場合には、select_area_numを変えて、
        以下を、’ホーム’ のページの処理とする'''
            
    except Exception as e:
        ud['error'] = 'error in initial_stage'
    finally:        
        return ud
def lang_treatment(ud):
    '''ログイン済みであり、langの変更もなければ、リターン'''
    if 'i_name' in ud and ud['i_name'] != '' and \
        ('new_lang' not in ud):
        return ud  
    else:
        if 'new_lang' in ud:
            ud['lang'] = ud['new_lang']            
        if ud['lang'] == 'ja':
            ud['ol'] =['ホーム','ログイン','繋がりの唯物観',
               'ブログ','意見の広場','ページの紹介',
               'お知らせ','contact','sell']
            ud['current_select'] = 'ホーム'
            ud['error_message_list']=\
             data_list.error_message_list_j
            ud['select_area_num'] = \
             data_list.option_dic_j\
            [ud['select_area_data']]
            ud['option_dic'] = \
                data_list.option_dic_j
        else:       
            ud['ol'] =['home','login','r_materialim',
               'blog','opinion_plaza','page_intro',
               'notification','contact','sell']
            ud['current_select'] = 'home'
            ud['error_message_list']=\
                data_list.error_message_list_e 
            ud['select_area_num'] = \
                data_list.option_dic_e
            ud['option_dic'] = \
                data_list.option_dic_e 
        return ud
    

def fnu_analyser(ud):  
    fnu = ud['fnu']
    print(fnu)  
    #  int(x) に変換
    fnu = [int(x) \
        for x in fnu.split('0')]    
    if len(fnu) != 5 :
        ud['error'] = ud['error_message_list[2]']
        return ud  
    '''殆どの場合、ud['family_chord']とud['select_area_num']は
    一致するが、ud['select_area_num']が19の場合は例外'''
    ud['family_chord'] = int(fnu[0])# 処理の対象となるファミリー
    ud['family_number'] = int(fnu[1])#  処理の対象を詳細に表す
    ud['kind_of_request'] = int(fnu[2])#  処理の種類
    ud['command_option_list'] = int(fnu[3])#  処理の詳細
    ud['table_num_list'] = int(fnu[4])# 
    '''処理のコマンドとその対象となるテーブルを
    順序的な対応関係を持たせつつ、リスト化する。'''
    command_option_list = \
        list(map(int,str(ud['command_option_list'])))
    table_num_list = \
        list(map(int,str(ud['table_num_list'])))
    if len(command_option_list ) != \
        len(table_num_list):
        ud['error'] = \
            ud['error_message_list'][2]
    else:
        ud['command_option_list'] = \
            command_option_list
        ud['table_num_list'] = \
            table_num_list   
    return ud    

def com_analyser(ud): 
    # :1:と:2:の間をキー、:2:から次の:1:または改行・文字列末尾までを値として抽出
    pairs = re.findall(r":1:(.*?):2:(.*?)(?=:1:|\n|$)", ud["com"], re.DOTALL)
    
    # 前後の余分な空白を除去して辞書化
    ud['com'] = {k.strip(): v.strip() for k, v in pairs}
    
    return ud
        
def matching_handler(content,pattern):
    repatter = re.compile(pattern)
    result = repatter.match(content)
    return result
   

if __name__ == "__main__":
    # 修正後：自動リロード（reloader）をコード側で「絶対にオフ」にする

    #app.run(debug=True, use_reloader=False)
    
    print(database.__file__)
    print('korede owari')
    handler = Main_Handler()
    '''以下は、各々のトップページを表示するのに必要な
    コマンドデータを管理者用ページに作成する為の処理コード
    勿論これは管理者用のトップページに表示される'''
    ud ={'session':'start','lang':'en','i_name':'akira'}
    ud['select_area_data'] = '管理者用'
    ud['input_area_data'] = '''
    ":lang:<ja>\n"
    ":fnu:<1901102014011>\n"
    ":com::1:input_area_data"
    ":2::<br>"
    [初めに]<br>「前向きに生きる」という言い回しがあります。
    何時生まれたものか、私は知りませんが、恐らく遥か昔の事では
    ないでしょう。若い頃にはあまり聞いた記憶のない言葉ですから。
    おそらく比較的最近に生まれたもので、それ以来、多く
    の人が何となく納得し、共感し、受け入れているように見える、
    現代の金言かも知れません。しかしながらそれは、もしそうしなけ
    れば、生きて行くのが困難な状況で生きる人が少なくない事の、
    逆説的な表現ではないでしょうか？<br>
    このサイトは、自分を始めとする、現代を生きる人間、あるいは社会の
    状況を肯定的に捉えている人向きではありません。又、疑問、不安
    不満を抱えていても、出来るならそれに蓋をし胡麻化して楽に生きて
    行こうという志向の人向きでもありません。面倒でも、辛くても、
    どこかに問題があると思えば、それと向き合う中で、判断の糸口を
    見つけようという姿勢を評価する人向けです。
    "これはコマンド入力用のテキスト欄です。コマンド？、"
    "何故そんな面倒なものを入力しなければならないのか"
    "と思うかも知れませんが、それらは双方向的なプログラムを"
    "ユーザが動かす為には大なり小なり必要な操作です。<br>"    
    "このサイトのコマンドは、若干複雑な形をしていますが、"
    "やる事は、右のテキスト欄に記載されたテンプレートの中から、"
    "ニーズに合ったものを選択し、このテキスト欄にペーストし、"
    "幾つかの項目に入力するだけです。しかも、殆どの場合、"
    "面倒で分かりにくい数字の部分はテンプレートに書かれており"
    "ユーザに求められるのは平易な入力ですから、ご安心ください。"
    "<br>特に、左のセレクトタグ欄の２番目にある「ログイン」を"
    "選択し、Goボタンを押すと、関連するコマンドテンプレート"
    "が右の欄に現れます。それを見れば、容易なことが"
    "了解出来ると思います。"
    ":1:output_area_data:2: :lang:<ja en>:fnu:<01010201322>"
    ":com:<>:oth:<>"
    ":1:annouce_area_data:2: こんにちは。ようこそ、繋がりの唯物観へ。"
    "ここは、本文の手短な紹介、又はその案内をする場所です。ですから、"
    "此処を先ず見るようにして下さい。<br>"
    "このサイトは会員登録を求める会員制です。従って、このサイトについて"
    "予備知識を持つ事は、登録者にとって必須の要件と言って良いでしょう。"
    "その期待に十分応えるものかどうか分かりませんが、下に手短な紹介文"
    "載せています。是非、登録前にご一読下さい。"
    ":1:footer_area_data :2: "
    '''
    
    ":oth:<>\n"
)

    
    ud = handler.main_handler(ud)
    
    '''新しいウィンドウで開く
python + flaskでホームページの作成をしています。以前、geminiに聞いて、index.htmlファイルに以下のコードを書き込みました。
<div  text-align: right;>
<select name="select_area" id="select_area" size="9">
  {% for item in ol %}
    {# itemの内容が、viewsから渡したcurrent_selectと一致すればselectedを付与 #}
    <option value="{{ item }}" {% if item == current_select %}selected{% endif %}>
      {{ item }}
  {% endfor %}
</select>
このファイルを開くコマンドは、views.pyに書くのですが、それはmain_handlerファイルを介してol値を得ます。教えて欲しい事は、文字列Aや,Bを単にAやBと表すとして、A,B,C,D,E,Fを選択肢とするセレクトタグを、Aが選択された状態で、index.htmlで表示するには、main_handlerのolの定義をどう記述すれば良いか、です。
ol （リスト）の定義と、現在選択されている値（current_select）の渡し方について解説します。

結論：コードの書き方
main_handler 内で、ol に選択肢の文字列リストを代入し、current_select に初期選択させたい値（'A'） を指定して index.html へ渡します。

main_handler（または views.py）の記述例
Python
# main_handler 内の処理（関数やメソッド内）

# 1. 選択肢のリストを定義
ol = ['A', 'B', 'C', 'D', 'E', 'F']

# 2. 初期状態で選択しておきたい値を設定
current_select = 'A'

# 3. render_template で index.html に渡す
# （views.py から呼び出す際や render_template を使う箇所で指定します）
return render_template('index.html', ol=ol, current_select=current_select)
補足と注意点
1. Jinja2 テンプレートのタグ閉じ
提示いただいた index.html のコードで、<option> タグの閉じタグ（</option>）が抜けているため、以下のように補完しておくと HTML としてより安全です。

HTML
<select name="select_area" id="select_area" size="9">
  {% for item in ol %}
    {# itemの内容がcurrent_selectと一致すればselectedを付与 #}
    <option value="{{ item }}" {% if item == current_select %}selected{% endif %}>
      {{ item }}
    </option>
  {% endfor %}
</select>
2. 動的に選択状態を変えたい場合
もしユーザーの入力やリクエストに応じて選択状態を変えたい場合は、current_select の部分をリクエストパラメーター（例: request.args.get('select_area', 'A')）などから動的に取得するように記述します。
'''