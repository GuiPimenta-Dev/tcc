from flask import Blueprint
from flask_restx import Resource, Namespace, reqparse

from models.generator import GeneratorModel
from app import logger
from routes import dump_model, load_model
from services.isolated_generator import IsolatedGeneratorService
from utils.constants import ISOLATED_GENERATOR_ROUTE_PREFIX

bp = Blueprint("isolated_generator", __name__, url_prefix=ISOLATED_GENERATOR_ROUTE_PREFIX)
nms = Namespace("Isolated Generator")

isolated_generator_parser = reqparse.RequestParser(bundle_errors=True)
load_parser = isolated_generator_parser.copy()
voltage_parser = isolated_generator_parser.copy()
power_factor_parser = isolated_generator_parser.copy()

isolated_generator_parser.add_argument("Vt", required=False, type=float, location="json", default=480)
isolated_generator_parser.add_argument("VtN", required=False, type=float, location="json", default=600)
isolated_generator_parser.add_argument("Il", required=False, type=float, location="json", default=120)
isolated_generator_parser.add_argument("Fp", required=False, type=float, location="json", default=0.8)
isolated_generator_parser.add_argument("Xs", required=False, type=float, location="json", default=2.5)
isolated_generator_parser.add_argument("Ra", required=False, type=float, location="json", default=0.1)
isolated_generator_parser.add_argument("losses", required=False, type=float, location="json", default=70)
isolated_generator_parser.add_argument(
    "lead_lag",
    required=False,
    type=str,
    location="json",
    choices=["lead", "lag"],
    default="lag",
)
isolated_generator_parser.add_argument(
    "delta_star",
    required=False,
    type=str,
    location="json",
    choices=["delta", "star"],
    default="star",
)

load_parser.add_argument("load", required=False, type=float, location="json", default=30)

voltage_parser.add_argument("Ea", required=False, type=float, location="json", default=227.5)

power_factor_parser.add_argument("Fp", required=False, type=float, location="json", default=1)


@nms.route("")
class Settings(Resource):
    @nms.expect(isolated_generator_parser)
    @nms.response(200, "Success")
    @nms.response(400, "Bad Request")
    def post(self):
        args = isolated_generator_parser.parse_args()
        try:
            isolated_generator = IsolatedGeneratorService(model=GeneratorModel(**args))
            dump_model(model=isolated_generator, machine="isolated_generator")
            return isolated_generator.settings_coords

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
            isolated_generator = load_model(machine="isolated_generator")
            return isolated_generator.update_load(load=load)

        except Exception as e:
            logger.info(str(e))
            raise


@nms.route("/voltage")
class Voltage(Resource):
    @nms.expect(voltage_parser)
    @nms.response(200, "Success")
    @nms.response(400, "Bad Request")
    def put(self):
        ea = voltage_parser.parse_args()["Ea"]
        try:
            isolated_generator = load_model(machine="isolated_generator")
            return isolated_generator.update_ea(voltage=ea)

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
            isolated_generator = load_model(machine="isolated_generator")
            return isolated_generator.update_fp(power_factor=fp)

        except Exception as e:
            logger.info(str(e))
            raise
