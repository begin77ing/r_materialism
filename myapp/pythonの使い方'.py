'''ここではpythonの文法や使用例について調べた事を書く。'''
#1::商と余り
# 商と余りを個別に計算
a = 10
b = 3
quotient = a // b # 商: 3
remainder = a % b # 余り: 1
print(f"商: {quotient}, 余り: {remainder}")
# divmod関数で商と余りを同時に取得
a = 10
b = 3
quotient, remainder = divmod(a, b)
print(f"商: {quotient}, 余り: {remainder}")

#2::逆引き辞書keyとvalueの役割を逆にする
my_dict = {'a': 1, 'b': 2, 'c': 3}
# keyとvalueを反転させた辞書を作成
reversed_dict = {v: k for k, v in my_dict.items()}
# 普通の辞書アクセスと同じように逆引きが可能
print(reversed_dict[3])  # 出力: 'c'