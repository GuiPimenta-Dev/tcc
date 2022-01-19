from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from utils.constants import (
    MOTOR_ROUTE_PREFIX,
    ISOLATED_GENERATOR_ROUTE_PREFIX,
    CONNECTED_GENERATOR_ROUTE_PREFIX,
    API_ROUTE_PREFIX,
)
from routes import motor, connected_generator, isolated_generator

app = Flask(__name__)
CORS(app)

api = Api(app, doc=f"{API_ROUTE_PREFIX}/docs", title="Syncronous Machine Phasor Simulator")
api.add_namespace(motor.nms, path=MOTOR_ROUTE_PREFIX)
api.add_namespace(connected_generator.nms, path=CONNECTED_GENERATOR_ROUTE_PREFIX)
api.add_namespace(isolated_generator.nms, path=ISOLATED_GENERATOR_ROUTE_PREFIX)
app.config["RESTX_ERROR_404_HELP"] = False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
