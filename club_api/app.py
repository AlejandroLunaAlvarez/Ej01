from flask import Flask
from src.routes.deportes import deportes_bp

app = Flask(__name__)

# app.register_blueprint(canchas_bp, url_prefix=None)
app.register_blueprint(deportes_bp, url_prefix=None)


if __name__ == '__main__':
    app.run(debug=True, port=5000)