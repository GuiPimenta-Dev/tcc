from flask import Blueprint
from flask_restx import Resource, Namespace, reqparse

from app import logger
from services.connected_generator import ConnectedGeneratorService
from utils.constants import CONNECTED_GENERATOR_ROUTE_PREFIX

bp = Blueprint('connected_generator', __name__, url_prefix=CONNECTED_GENERATOR_ROUTE_PREFIX)
nms = Namespace('Connected Generator')

connected_generator_parser = reqparse.RequestParser(bundle_errors=True)
load_parser = connected_generator_parser.copy()
voltage_parser = connected_generator_parser.copy()
power_factor_parser = connected_generator_parser.copy()


connected_generator_parser.add_argument('Vt', required=False, type=float, location='json', default=480)
connected_generator_parser.add_argument('Il', required=False, type=float, location='json', default=1200)
connected_generator_parser.add_argument('Fp', required=False, type=float, location='json', default=0.8)
connected_generator_parser.add_argument('Xs', required=False, type=float, location='json', default=0.1)
connected_generator_parser.add_argument('Ra', required=False, type=float, location='json', default=0.015)
connected_generator_parser.add_argument('losses', required=False, type=float, location='json', default=70)
connected_generator_parser.add_argument('lagging', required=False, type=bool, location='json', default='lagging')
connected_generator_parser.add_argument('delta', required=False, type=bool, location='json', default='star')

load_parser.add_argument('load', required=False, type=float, location='json', default=30)

voltage_parser.add_argument('Vt', required=False, type=float, location='json', default=227.5)

power_factor_parser.add_argument('Fp', required=False, type=float, location='json', default=1)


class BaseConnectedGenerator(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_connected_generator(self, args: dict):
        if args['lagging'] == 'lagging':
            args['lagging'] = True
        else:
            args['lagging'] = False

        if args['delta'] == 'delta':
            args['delta'] = True
        else:
            args['delta'] = False
        BaseConnectedGenerator.connected_generator = ConnectedGeneratorService(params=args)


@nms.route('')
class Settings(BaseConnectedGenerator):
    @nms.expect(connected_generator_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def post(self):
        args = connected_generator_parser.parse_args()
        try:
            self.create_connected_generator(args=args)
            return self.connected_generator.settings_coords

        except Exception as e:
            logger.info(str(e))
            raise


@nms.route('/load')
class Load(BaseConnectedGenerator):
    @nms.expect(load_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def put(self):
        load = load_parser.parse_args()['load']
        try:
            return self.connected_generator.update_load(load=load)

        except Exception as e:
            logger.info(str(e))
            raise


@nms.route('/voltage')
class Voltage(BaseConnectedGenerator):
    @nms.expect(voltage_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def put(self):
        vt = voltage_parser.parse_args()['Vt']
        try:
            return self.connected_generator.update_vt(voltage=vt)

        except Exception as e:
            logger.info(str(e))
            raise


@nms.route('/power_factor')
class PowerFactor(BaseConnectedGenerator):
    @nms.expect(power_factor_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def put(self):
        fp = power_factor_parser.parse_args()['Fp']
        try:
            return self.connected_generator.update_fp(power_factor=fp)

        except Exception as e:
            logger.info(str(e))
            raise
