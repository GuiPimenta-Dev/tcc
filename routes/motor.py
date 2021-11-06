from flask import Blueprint, jsonify
from flask_restx import Resource, Namespace, reqparse
from services.motor import MotorService
from app import logger
from utils.constants import MOTOR_ROUTE_PREFIX

bp = Blueprint('motor', __name__, url_prefix=MOTOR_ROUTE_PREFIX)
nms = Namespace('Motor')

motor_parser = reqparse.RequestParser(bundle_errors=True)
motor_parser.add_argument('VtN', required=False, type=float, location='json')
motor_parser.add_argument('SN', required=False, type=float, location='json')
motor_parser.add_argument('FpN', required=False, type=float, location='json', default=0.8)
motor_parser.add_argument('Vt', required=False, type=float, location='json', default=208)
motor_parser.add_argument('Ia', required=False, type=float, location='json')
motor_parser.add_argument('S', required=False, type=float, location='json', default=45)
motor_parser.add_argument('Fp', required=False, type=float, location='json', default=0.8)
motor_parser.add_argument('lagging', required=False, type=bool, location='json', default=False)
motor_parser.add_argument('Xs', required=False, type=float, location='json', default=2.5)
motor_parser.add_argument('Ra', required=False, type=float, location='json', default=0)
motor_parser.add_argument('load', required=False, type=float, location='json', default=15)
motor_parser.add_argument('losses', required=False, type=float, location='json', default=2.5)


load_parser = reqparse.RequestParser(bundle_errors=True)
load_parser.add_argument('load', required=False, type=float, location='form', default=30)


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
            return self.motor.initial_coords

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
            #TODO Improove load method
            return self.motor.update_load(load=load)

        except Exception as e:
            logger.info(str(e))
            raise

