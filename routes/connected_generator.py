from flask import Blueprint
from flask_restx import Resource, Namespace, reqparse
from models.generator import GeneratorModel

from app import logger
from routes import dump_model, load_model
from services.connected_generator import ConnectedGeneratorService
from utils.constants import CONNECTED_GENERATOR_ROUTE_PREFIX

bp = Blueprint("connected_generator", __name__, url_prefix=CONNECTED_GENERATOR_ROUTE_PREFIX)
nms = Namespace("Connected Generator")

connected_generator_parser = reqparse.RequestParser(bundle_errors=True)
load_parser = connected_generator_parser.copy()
voltage_parser = connected_generator_parser.copy()
power_factor_parser = connected_generator_parser.copy()

connected_generator_parser.add_argument("Vt", required=False, type=float, location="json", default=480)
connected_generator_parser.add_argument("VtN", required=False, type=float, location="json", default=600)
connected_generator_parser.add_argument("Il", required=False, type=float, location="json", default=120)
connected_generator_parser.add_argument("Fp", required=False, type=float, location="json", default=0.8)
connected_generator_parser.add_argument("Xs", required=False, type=float, location="json", default=2.5)
connected_generator_parser.add_argument("Ra", required=False, type=float, location="json", default=0.1)
connected_generator_parser.add_argument("losses", required=False, type=float, location="json", default=70)
connected_generator_parser.add_argument(
    "lead_lag",
    required=False,
    type=str,
    location="json",
    choices=["lead", "lag"],
    default="lag",
)
connected_generator_parser.add_argument(
    "delta_star",
    required=False,
    type=str,
    location="json",
    choices=["delta", "star"],
    default="delta",
)

load_parser.add_argument("load", required=False, type=float, location="json", default=30)

voltage_parser.add_argument("Ea", required=False, type=float, location="json", default=227.5)

power_factor_parser.add_argument("Fp", required=False, type=float, location="json", default=1)


@nms.route("")
class Settings(Resource):
    @nms.expect(connected_generator_parser)
    @nms.response(200, "Success")
    @nms.response(400, "Bad Request")
    def post(self):
        args = connected_generator_parser.parse_args()
        try:
            connected_generator = ConnectedGeneratorService(model=GeneratorModel(**args))
            dump_model(model=connected_generator, machine="connected_generator")
            return connected_generator.settings_coords

        except Exception as e:
            logger.info(str(e))
            raise


@nms.route("/load")
class Load(Resource):
    @nms.expect(load_parser)
    @nms.response(200, "Success")
    @nms.response(400, "Bad Request")
    def put(self):
        load = load_parser.parse_args()["load"]
        try:
            connected_generator = load_model(machine="connected_generator")
            return connected_generator.update_load(load=load)

        except Exception as e:
            logger.info(str(e))
            raise


@nms.route("/voltage")
class Voltage(Resource):
    @nms.expect(voltage_parser)
    @nms.response(200, "Success")
    @nms.response(400, "Bad Request")
    def put(self):
        Ea = voltage_parser.parse_args()["Ea"]
        try:
            connected_generator = load_model(machine="connected_generator")
            return connected_generator.update_ea(voltage=Ea)

        except Exception as e:
            logger.info(str(e))
            raise


@nms.route("/power_factor")
class PowerFactor(Resource):
    @nms.expect(power_factor_parser)
    @nms.response(200, "Success")
    @nms.response(400, "Bad Request")
    def put(self):
        fp = power_factor_parser.parse_args()["Fp"]
        try:
            connected_generator = load_model(machine="connected_generator")
            return connected_generator.update_fp(power_factor=fp)

        except Exception as e:
            logger.info(str(e))
            raise
