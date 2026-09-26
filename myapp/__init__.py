import logging
from flask import Flask

app = Flask(__name__)
app.secret_key = 'error_handling_online20260711' 
# --- エラーログを保存する設定（ここに仕込みます） ---
logging.basicConfig(
    filename='error.log', 
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# views.py を読み込む（※一番下に書くのがFlaskの決まりです）
import myapp.views