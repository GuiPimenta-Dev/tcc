from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from utils.constants import MOTOR_ROUTE_PREFIX,GENERATOR_ROUTE_PREFIX,API_ROUTE_PREFIX
from routes import motor, generator

app = Flask(__name__)
CORS(app)

app.register_blueprint(motor.bp)
app.register_blueprint(generator.bp)

api = Api(app, doc=f'{API_ROUTE_PREFIX}/docs', title='Simulador Fasorial de Máquinas Síncronas')
api.add_namespace(motor.nms, path=MOTOR_ROUTE_PREFIX)
api.add_namespace(generator.nms, path=GENERATOR_ROUTE_PREFIX)
app.config['RESTX_ERROR_404_HELP'] = False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
