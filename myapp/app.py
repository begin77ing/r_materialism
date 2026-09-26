from flask import Flask
import logging
from logging.handlers import RotatingFileHandler


# --- 【ここから】Flask用のエラーログ保存設定 ---
# 1. エラーを記録するファイル名と、ファイルの最大サイズを指定します
file_handler = RotatingFileHandler('error.log', maxBytes=10240, backupCount=1)
file_handler.setLevel(logging.ERROR)

# 2. ログの見た目（日時やエラー内容）を整えます
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(formatter)

# 3. Flask本体にこのログ設定を合体させます
app.logger.addHandler(file_handler)
# --- 【ここまで】 ---

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True, use_reloader=False)