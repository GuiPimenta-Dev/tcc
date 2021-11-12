from flask import Blueprint
from flask_restx import Resource, Namespace, reqparse

from app import logger
from services.isolated_generator import IsolatedGeneratorService
from utils.constants import ISOLATED_GENERATOR_ROUTE_PREFIX

bp = Blueprint('isolated_generator', __name__, url_prefix=ISOLATED_GENERATOR_ROUTE_PREFIX)
nms = Namespace('Isolated Generator')

isolated_generator_parser = reqparse.RequestParser(bundle_errors=True)
load_parser = isolated_generator_parser.copy()
voltage_parser = isolated_generator_parser.copy()
power_factor_parser = isolated_generator_parser.copy()

isolated_generator_parser.add_argument('Vt', required=False, type=float, location='json', default=480)
isolated_generator_parser.add_argument('Il', required=False, type=float, location='json', default=1200)
isolated_generator_parser.add_argument('Fp', required=False, type=float, location='json', default=0.8)
isolated_generator_parser.add_argument('Xs', required=False, type=float, location='json', default=0.1)
isolated_generator_parser.add_argument('Ra', required=False, type=float, location='json', default=0.015)
isolated_generator_parser.add_argument('losses', required=False, type=float, location='json', default=70)
isolated_generator_parser.add_argument('lagging', required=False, type=bool, location='json', default=True)
isolated_generator_parser.add_argument('delta', required=False, type=bool, location='json', default=False)

load_parser.add_argument('load', required=False, type=float, location='json', default=30)

voltage_parser.add_argument('Vt', required=False, type=float, location='json', default=227.5)

power_factor_parser.add_argument('Fp', required=False, type=float, location='json', default=1)


class BaseIsolatedGenerator(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_isolated_generator(self, args: dict):
        BaseIsolatedGenerator.isolated_generator = IsolatedGeneratorService(params=args)


@nms.route('')
class Settings(BaseIsolatedGenerator):
    @nms.expect(isolated_generator_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def post(self):
        args = isolated_generator_parser.parse_args()
        try:
            self.create_isolated_generator(args=args)
            return self.isolated_generator.settings_coords

        except Exception as e:
            logger.info(str(e))
            raise


@nms.route('/load')
class Load(BaseIsolatedGenerator):
    @nms.expect(load_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def put(self):
        load = load_parser.parse_args()['load']
        try:
            return self.isolated_generator.update_load(load=load)

        except Exception as e:
            logger.info(str(e))
            raise


@nms.route('/voltage')
class Voltage(BaseIsolatedGenerator):
    @nms.expect(voltage_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def put(self):
        vt = voltage_parser.parse_args()['Vt']
        try:
            return self.isolated_generator.update_vt(voltage=vt)

        except Exception as e:
            logger.info(str(e))
            raise


@nms.route('/power_factor')
class PowerFactor(BaseIsolatedGenerator):
    @nms.expect(power_factor_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def put(self):
        fp = power_factor_parser.parse_args()['Fp']
        try:
            return self.isolated_generator.update_fp(power_factor=fp)

        except Exception as e:
            logger.info(str(e))
            raise
