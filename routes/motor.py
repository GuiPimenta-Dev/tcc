import pickle

from flask import Blueprint
from flask_restx import Resource, Namespace, reqparse

from app import logger
from services.motor import MotorService
from utils.constants import MOTOR_ROUTE_PREFIX
from models.motor import MotorModel
from . import dump_model, load_model

bp = Blueprint("motor", __name__, url_prefix=MOTOR_ROUTE_PREFIX)
nms = Namespace("Motor")

motor_parser = reqparse.RequestParser(bundle_errors=True)
load_parser = motor_parser.copy()
voltage_parser = motor_parser.copy()
power_factor_parser = motor_parser.copy()

motor_parser.add_argument("Vt", required=False, type=float, location="json", default=208)
motor_parser.add_argument("VtN", required=False, type=float, location="json", default=308)
motor_parser.add_argument("Fp", required=False, type=float, location="json", default=0.8)
motor_parser.add_argument(
    "lead_lag",
    required=False,
    type=str,
    location="json",
    choices=["lead", "lag"],
    default="lead",
)
motor_parser.add_argument("Xs", required=False, type=float, location="json", default=2.5)
motor_parser.add_argument("Ra", required=False, type=float, location="json", default=0)
motor_parser.add_argument("kw_load", required=False, type=float, location="json", default=15)
motor_parser.add_argument("losses", required=False, type=float, location="json", default=2.5)

load_parser.add_argument("load", required=False, type=float, location="json", default=30)

voltage_parser.add_argument("Ea", required=False, type=float, location="json", default=227.5)

power_factor_parser.add_argument("Fp", required=False, type=float, location="json", default=1)


@nms.route("")
class Settings(Resource):
    @nms.expect(motor_parser)
    @nms.response(200, "Success")
    @nms.response(400, "Bad Request")
    def post(self):
        args = motor_parser.parse_args()
        try:
            motor = MotorService(model=MotorModel(**args))
            dump_model(model=motor, machine="motor")
            return motor.settings_coords

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
            motor = load_model(machine="motor")
            return motor.update_load(load=load)

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
            motor = load_model(machine="motor")
            return motor.update_ea(voltage=Ea)

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
            motor = load_model(machine="motor")
            return motor.update_fp(power_factor=fp)

        except Exception as e:
            logger.info(str(e))
            raise
