from flask import Blueprint
from flask_restx import Resource, Namespace, reqparse

from app import logger
from services.motor import MotorService
from utils.constants import MOTOR_ROUTE_PREFIX

bp = Blueprint('motor', __name__, url_prefix=MOTOR_ROUTE_PREFIX)
nms = Namespace('Motor')

motor_parser = reqparse.RequestParser(bundle_errors=True)
load_parser = motor_parser.copy()
voltage_parser = motor_parser.copy()
power_factor_parser = motor_parser.copy()


motor_parser.add_argument('Vt', required=False, type=float, location='json', default=208)
motor_parser.add_argument('S', required=False, type=float, location='json', default=45)
motor_parser.add_argument('Fp', required=False, type=float, location='json', default=0.85)
motor_parser.add_argument('lagging', required=False, type=bool, location='json', default=True)
motor_parser.add_argument('delta', required=False, type=bool, location='json', default=True)
motor_parser.add_argument('Xs', required=False, type=float, location='json', default=2.5)
motor_parser.add_argument('Ra', required=False, type=float, location='json', default=0)
motor_parser.add_argument('load', required=False, type=float, location='json', default=15)
motor_parser.add_argument('losses', required=False, type=float, location='json', default=2.5)

load_parser.add_argument('load', required=False, type=float, location='json', default=30)

voltage_parser.add_argument('Ea', required=False, type=float, location='json', default=227.5)

power_factor_parser.add_argument('Fp', required=False, type=float, location='json', default=1)


class BaseMotor(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_motor(self, args: dict):
        BaseMotor.motor = MotorService(params=args)


@nms.route('')
class Settings(BaseMotor):
    @nms.expect(motor_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def post(self):
        args = motor_parser.parse_args()
        try:
            self.create_motor(args=args)
            return self.motor.settings_coords

        except Exception as e:
            logger.info(str(e))
            raise


@nms.route('/load')
class Load(BaseMotor):
    @nms.expect(load_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def put(self):
        load = load_parser.parse_args()['load']
        try:
            return self.motor.update_load(load=load)

        except Exception as e:
            logger.info(str(e))
            raise


@nms.route('/voltage')
class Voltage(BaseMotor):
    @nms.expect(voltage_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def put(self):
        ea = voltage_parser.parse_args()['Ea']
        try:
            return self.motor.update_ea(voltage=ea)

        except Exception as e:
            logger.info(str(e))
            raise


@nms.route('/power_factor')
class PowerFactor(BaseMotor):
    @nms.expect(power_factor_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def put(self):
        fp = power_factor_parser.parse_args()['Fp']
        try:
            return self.motor.update_fp(power_factor=fp)

        except Exception as e:
            logger.info(str(e))
            raise
