from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from utils import constants
from routes import motor, generator

app = Flask(__name__)
CORS(app)

app.register_blueprint(motor.bp)
app.register_blueprint(generator.bp)

api = Api(app, doc='/api/v1/docs', title='Simulador Fasorial de Máquinas Síncronas')
api.add_namespace(motor.nms, path=constants.API_ROUTE_PREFIX)
api.add_namespace(generator.nms, path=constants.API_ROUTE_PREFIX)
app.config['RESTX_ERROR_404_HELP'] = False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
