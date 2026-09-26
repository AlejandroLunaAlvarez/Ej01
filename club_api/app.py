from flask import Flask
from club_api.src.routes.deportes import deportes_bp
from club_api.src.routes.reservas_route import reservas_bp
from club_api.src.routes.canchas import canchas_bp

app = Flask(__name__)

# Registro de Blueprints
app.register_blueprint(canchas_bp, url_prefix=None)
app.register_blueprint(deportes_bp, url_prefix=None)
app.register_blueprint(reservas_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)