from flask import Flask
#from flask_sqlalchemy import SQLAlchemy  # 追加
app = Flask(__name__)
app.config.from_object('myapp.config') # 追加
#db = SQLAlchemy(app)  # 追加
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db' # SQLiteの場合
#db = SQLAlchemy(app) # Flask-SQLAlchemyを初期化
#from .models import select_input  # 追加
#from .models import employee  # 追加
import myapp.views
# データベースとテーブルを作成
#with app.app_context(): # コンテキスト内でのみ実行
    #db.create_all()