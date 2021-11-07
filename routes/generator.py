from flask import Blueprint
from flask_restx import Resource, Namespace, reqparse

from app import logger
from services.generator import GeneratorService
from utils.constants import GENERATOR_ROUTE_PREFIX

bp = Blueprint('generator', __name__, url_prefix=GENERATOR_ROUTE_PREFIX)
nms = Namespace('Generator')

generator_parser = reqparse.RequestParser(bundle_errors=True)
load_parser = generator_parser.copy()
voltage_parser = generator_parser.copy()
power_factor_parser = generator_parser.copy()

generator_parser.add_argument('VtN', required=False, type=float, location='json')
generator_parser.add_argument('SN', required=False, type=float, location='json')
generator_parser.add_argument('FpN', required=False, type=float, location='json')
generator_parser.add_argument('Vt', required=False, type=float, location='json')
generator_parser.add_argument('Ea', required=False, type=float, location='json', default=277.0)
generator_parser.add_argument('Ia', required=False, type=float, location='json')
generator_parser.add_argument('Il', required=False, type=float, location='json', default=60)
generator_parser.add_argument('S', required=False, type=float, location='json')
generator_parser.add_argument('Fp', required=False, type=float, location='json', default=0.8)
generator_parser.add_argument('lagging', required=False, type=bool, location='json', default=False)
generator_parser.add_argument('delta', required=False, type=bool, location='json', default=False)
generator_parser.add_argument('Xs', required=False, type=float, location='json', default=1)
generator_parser.add_argument('Ra', required=False, type=float, location='json', default=0)
generator_parser.add_argument('load', required=False, type=float, location='json')
generator_parser.add_argument('losses', required=False, type=float, location='json', default=2.5)

load_parser.add_argument('load', required=False, type=float, location='json', default=30)

voltage_parser.add_argument('Ea', required=False, type=float, location='json', default=227.5)

power_factor_parser.add_argument('Fp', required=False, type=float, location='json', default=1)


class BaseGenerator(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_generator(self, args: dict):
        BaseGenerator.generator = GeneratorService(params=args)


@nms.route('')
class Settings(BaseGenerator):
    @nms.expect(generator_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def post(self):
        args = generator_parser.parse_args()
        try:
            self.create_generator(args=args)
            return self.generator.settings_coords

        except Exception as e:
            logger.info(str(e))
            raise


@nms.route('/load')
class Load(BaseGenerator):
    @nms.expect(load_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def put(self):
        load = load_parser.parse_args()['load']
        try:
            return self.generator.update_load(load=load)

        except Exception as e:
            logger.info(str(e))
            raise


@nms.route('/voltage')
class Voltage(BaseGenerator):
    @nms.expect(voltage_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def put(self):
        ea = voltage_parser.parse_args()['Ea']
        try:
            return self.generator.update_ea(voltage=ea)

        except Exception as e:
            logger.info(str(e))
            raise


@nms.route('/power_factor')
class PowerFactor(BaseGenerator):
    @nms.expect(power_factor_parser)
    @nms.response(200, 'Success')
    @nms.response(400, 'Bad Request')
    def put(self):
        fp = power_factor_parser.parse_args()['Fp']
        try:
            return self.generator.update_fp(power_factor=fp)

        except Exception as e:
            logger.info(str(e))
            raise
