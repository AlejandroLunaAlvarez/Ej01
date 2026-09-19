from flask import Flask
from src.routes.canchas import canchas_bp

app = Flask(__name__)

app.register_blueprint(canchas_bp, url_prefix=None)

if __name__ == '__main__':
    app.run(Debug=True, port=5000)