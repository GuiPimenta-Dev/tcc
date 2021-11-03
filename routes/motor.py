from flask import Blueprint, jsonify
from flask_restx import Resource, Namespace, reqparse
from services.motor import MotorService
from app import logger
from utils import constants
import json

bp = Blueprint('motor', __name__, url_prefix=constants.API_ROUTE_PREFIX)
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


@nms.route('/motor')
class BaseMotor(Resource):
    @nms.expect(motor_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def post(self):
        args = motor_parser.parse_args()
        try:
            #TODO return only the arrow coordinates to front
            self.motor = MotorService(params=args)
            return str(self.motor.settings)

        except Exception as e:
            logger.info(str(e))
            raise
