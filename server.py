import sys
sys.path.append("e:\flask\.venv\.venv\Lib\site-packages")

from flask import Flask
from myapp import app

if __name__ == '__main__':
    app.run()